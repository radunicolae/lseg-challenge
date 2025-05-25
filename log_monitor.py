import csv
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

# Thresholds
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

def parse_logs(file_path):
    """
    Parses the CSV log file and returns a dictionary of job entries keyed by PID.
    Each entry includes the start time, end time, and job description.
    """
    jobs = defaultdict(dict)
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4:
                continue  # Skip malformed rows
            timestamp_str, job_desc, event, pid = map(str.strip, row)
            timestamp = datetime.strptime(timestamp_str, "%H:%M:%S")
            if event == 'START':
                jobs[pid]['start'] = timestamp
                jobs[pid]['desc'] = job_desc
            elif event == 'END':
                jobs[pid]['end'] = timestamp
    return jobs

def analyze_jobs(jobs):
    """
    Analyzes each job and includes it in the report with status.
    Categorizes as WARNING, ERROR, OK, or INCOMPLETE based on duration.
    """
    report = []
    for pid, info in jobs.items():
        start = info.get('start')
        end = info.get('end')
        if start and end:
            duration = end - start
            if duration > ERROR_THRESHOLD:
                level = 'ERROR'
            elif duration > WARNING_THRESHOLD:
                level = 'WARNING'
            else:
                level = 'OK'
        else:
            duration = None
            level = 'INCOMPLETE'

        report.append({
            'pid': pid,
            'desc': info.get('desc', 'Unknown'),
            'start': start,
            'end': end,
            'duration': duration,
            'level': level
        })
    return report

def print_report(report):
    """
    Prints the job report, filtering out OK jobs.
    """
    for entry in sorted(report, key=lambda x: x['start'] or datetime.min):
        if entry['level'] == 'OK':
            continue
        start = entry['start'].time() if entry['start'] else 'N/A'
        end = entry['end'].time() if entry['end'] else 'N/A'
        duration = entry['duration'] if entry['duration'] else 'N/A'
        print(f"[{entry['level']}] PID {entry['pid']} ({entry['desc']}): "
              f"Started at {start}, Ended at {end}, Duration: {duration}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Monitoring Tool")
    parser.add_argument("logfile", help="Path to the log file")
    args = parser.parse_args()

    job_records = parse_logs(args.logfile)
    report_data = analyze_jobs(job_records)

    print_report(report_data)
