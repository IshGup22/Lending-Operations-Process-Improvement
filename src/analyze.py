"""Analyze synthetic operational cases; calculate a transparent what-if scenario."""
from pathlib import Path
import json, sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'synthetic_loan_operations.csv'
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)
PREVENTABLE={'Missing documentation','Source mismatch','Duplicate submission'}
# Illustrative, explicitly assumed prevention fraction from upstream validation.
PREVENTION_RATE=.45
# A prevented exception avoids ONLY the exception-specific review minutes, conservatively not all effort.
AVOIDABLE_REVIEW_MINUTES=24

def analyze():
    df=pd.read_csv(DATA,parse_dates=['created_date'])
    required={'case_id','created_date','segment','team','exception_flag','root_cause','review_minutes','sla_breached','processing_hours'}
    assert required.issubset(df.columns)
    assert len(df)==25000 and df.case_id.is_unique
    assert df['exception_flag'].isin([0,1]).all()
    eligible=(df.exception_flag.eq(1)&df.root_cause.isin(PREVENTABLE))
    prevented=eligible.sum()*PREVENTION_RATE
    saved_minutes=prevented*AVOIDABLE_REVIEW_MINUTES
    total_review=df.review_minutes.sum()
    summary={
        'dataset':'Synthetic loan operations; not actual TD or bank customer data',
        'cases':len(df),'exceptions':int(df.exception_flag.sum()),
        'exception_rate':round(df.exception_flag.mean()*100,2),
        'first_pass_rate':round(df.first_pass_flag.mean()*100,2),
        'sla_breach_rate':round(df.sla_breached.mean()*100,2),
        'median_processing_hours':round(float(df.processing_hours.median()),1),
        'total_review_hours':round(total_review/60,1),
        'eligible_exceptions':int(eligible.sum()),
        'scenario_prevention_assumption_pct':round(PREVENTION_RATE*100,1),
        'scenario_avoidable_minutes_per_prevented_exception':AVOIDABLE_REVIEW_MINUTES,
        'scenario_prevented_exceptions_est':round(prevented),
        'scenario_review_hours_saved_est':round(saved_minutes/60,1),
        'scenario_review_effort_reduction_pct':round(saved_minutes/total_review*100,1),
    }
    (OUT/'metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    df['month']=df.created_date.dt.strftime('%Y-%m')
    df['avoidable_flag']=eligible.astype(int)
    groups=df.groupby(['month','segment','team'],observed=True).agg(
        cases=('case_id','count'), exceptions=('exception_flag','sum'),sla_breaches=('sla_breached','sum'),
        review_minutes=('review_minutes','sum'),eligible=('avoidable_flag','sum'),
        processing_hours_sum=('processing_hours','sum')
    ).reset_index()
    groups.to_json(OUT/'dashboard_aggregates.json',orient='records',indent=2)
    df.groupby('root_cause',observed=True).agg(cases=('case_id','count'),review_minutes=('review_minutes','sum')).reset_index().to_csv(OUT/'root_causes.csv',index=False)
    # An actual SQL query is executed against the exact data and output compared to pandas results.
    con=sqlite3.connect(':memory:');df.to_sql('cases',con,index=False)
    sql=(ROOT/'sql'/'01_baseline_kpis.sql').read_text(encoding='utf-8')
    sql_results=pd.read_sql_query(sql,con)
    assert int(sql_results.loc[0,'cases'])==summary['cases']
    assert int(sql_results.loc[0,'exceptions'])==summary['exceptions']
    con.close()
    return summary
if __name__=='__main__':
    print(json.dumps(analyze(),indent=2))
