import unittest
from datetime import datetime, timedelta
from collections import defaultdict
from log_monitor import parse_logs, analyze_jobs

class TestLogMonitor(unittest.TestCase):

    def setUp(self):
        self.sample_data = defaultdict(dict)
        self.sample_data['10001']['start'] = datetime.strptime('12:00:00', '%H:%M:%S')
        self.sample_data['10001']['end'] = datetime.strptime('12:06:00', '%H:%M:%S')
        self.sample_data['10001']['desc'] = 'test job 1'

        self.sample_data['10002']['start'] = datetime.strptime('12:10:00', '%H:%M:%S')
        self.sample_data['10002']['end'] = datetime.strptime('12:22:00', '%H:%M:%S')
        self.sample_data['10002']['desc'] = 'test job 2'

        self.sample_data['10003']['start'] = datetime.strptime('12:30:00', '%H:%M:%S')
        self.sample_data['10003']['desc'] = 'test job 3'

    def test_analyze_jobs(self):
        report = analyze_jobs(self.sample_data)
        self.assertEqual(len(report), 3)

        job1 = next(r for r in report if r['pid'] == '10001')
        self.assertEqual(job1['level'], 'WARNING')

        job2 = next(r for r in report if r['pid'] == '10002')
        self.assertEqual(job2['level'], 'ERROR')

        job3 = next(r for r in report if r['pid'] == '10003')
        self.assertEqual(job3['level'], 'INCOMPLETE')

    def test_parse_logs(self):
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp_file.write("""12:00:00,test job,START,20001
12:10:00,test job,END,20001""")
        temp_file.close()

        jobs = parse_logs(temp_file.name)
        self.assertIn('20001', jobs)
        self.assertIn('start', jobs['20001'])
        self.assertIn('end', jobs['20001'])
        self.assertEqual(jobs['20001']['desc'], 'test job')

if __name__ == '__main__':
    unittest.main()