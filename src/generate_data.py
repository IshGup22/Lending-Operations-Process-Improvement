"""Reproducible, synthetic loan-operations case data. No real customer information."""
from pathlib import Path
import csv, random, datetime
ROOT=Path(__file__).resolve().parents[1]
SEED=20261121
N=25000
SEGMENTS=['Retail','SME','Auto','Mortgage']
TEAMS=['North','Central','East','West']
CAUSES=['Missing documentation','Source mismatch','Duplicate submission','Manual approval','System validation','None']
HEADERS=['case_id','created_date','segment','team','amount_cad','risk_tier','exception_flag','root_cause','first_pass_flag','rework_flag','processing_hours','sla_hours','sla_breached','review_minutes','status']

def generate():
    rng=random.Random(SEED)
    start=datetime.date(2026,1,1)
    rows=[]
    for i in range(N):
        date=start+datetime.timedelta(days=rng.randrange(304))
        segment=rng.choices(SEGMENTS,weights=[.42,.25,.2,.13])[0]
        team=rng.choice(TEAMS)
        risk=rng.choices(['Low','Medium','High'],weights=[.52,.35,.13])[0]
        amount=round(rng.lognormvariate(9.3 if segment=='Retail' else 10.5, .85),2)
        # Higher exception likelihood for SME and more complex cases, with specific repeat causes.
        p=.13 + (.095 if segment=='SME' else .04 if segment=='Mortgage' else 0)+(.065 if risk=='High' else .025 if risk=='Medium' else 0)+(.028 if team=='East' else 0)
        exc=int(rng.random()<p)
        if exc:
            cause=rng.choices(CAUSES[:-1],weights=[.29,.25,.18,.16,.12])[0]
        else: cause='None'
        rework=int(exc and rng.random() < (.72 if cause in ['Missing documentation','Source mismatch','Duplicate submission'] else .48))
        # Processing time is a mix of baseline throughput + delays + heterogeneity.
        base={'Retail':11,'SME':17,'Auto':12,'Mortgage':20}[segment]
        lag={'None':0,'Missing documentation':15,'Source mismatch':11,'Duplicate submission':8,'Manual approval':19,'System validation':7}[cause]
        hours=round(max(1.1, rng.gauss(base+lag+ (5 if rework else 0), 4.8)),1)
        sla=24 if segment in ['Retail','Auto'] else 36
        review=round(max(3, rng.gauss(13+ (24 if exc else 0)+(11 if rework else 0), 5)),1)
        rows.append([f'CASE-{i+1:06}',date.isoformat(),segment,team,amount,risk,exc,cause,int(not exc),rework,hours,sla,int(hours>sla),review,'Resolved' if rng.random()<.94 else 'Open'])
    path=ROOT/'data'/'synthetic_loan_operations.csv'
    path.parent.mkdir(exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(HEADERS);w.writerows(rows)
    print(f'Generated {len(rows):,} synthetic cases at {path}')
if __name__=='__main__':generate()
