"""Standard library tests for data integrity, model assumptions and reproducibility."""
import csv,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ROOT/'outputs'/'metrics.json').exists():
            subprocess.run([sys.executable,str(ROOT/'src'/'run_pipeline.py')],check=True)
        with (ROOT/'data'/'synthetic_loan_operations.csv').open(encoding='utf-8') as f:
            cls.rows=list(csv.DictReader(f))
        cls.m=json.loads((ROOT/'outputs'/'metrics.json').read_text())
    def test_no_real_identifiers_or_duplicates(self):
        self.assertEqual(len(self.rows),25000)
        self.assertEqual(len({r['case_id'] for r in self.rows}),25000)
        self.assertEqual(set(self.rows[0]),{'case_id','created_date','segment','team','amount_cad','risk_tier','exception_flag','root_cause','first_pass_flag','rework_flag','processing_hours','sla_hours','sla_breached','review_minutes','status'})
    def test_exception_consistency(self):
        self.assertTrue(all((r['root_cause']=='None')==(r['exception_flag']=='0') for r in self.rows))
        self.assertTrue(all(int(r['first_pass_flag'])+int(r['exception_flag'])==1 for r in self.rows))
    def test_metrics_reconcile(self):
        self.assertEqual(sum(int(r['exception_flag']) for r in self.rows),self.m['exceptions'])
        self.assertEqual(round(sum(int(r['sla_breached']) for r in self.rows)/25000*100,2), self.m['sla_breach_rate'])
    def test_scenario_math(self):
        expected=sum(r['root_cause'] in {'Missing documentation','Source mismatch','Duplicate submission'} for r in self.rows if r['exception_flag']=='1')
        self.assertEqual(expected,self.m['eligible_exceptions'])
        self.assertAlmostEqual(expected*.45*24/60,self.m['scenario_review_hours_saved_est'],places=1)
    def test_aggregates_reconcile(self):
        a=json.loads((ROOT/'outputs'/'dashboard_aggregates.json').read_text())
        self.assertEqual(sum(r['cases'] for r in a),25000)
        self.assertEqual(sum(r['exceptions'] for r in a),self.m['exceptions'])
    def test_dashboard_is_standalone(self):
        html=(ROOT/'dashboard'/'index.html').read_text(encoding='utf-8')
        self.assertIn('Plotly',html)
        self.assertIn('MODELED, NOT REALIZED',html)
        self.assertIn('const A=',html)
if __name__=='__main__':unittest.main()
