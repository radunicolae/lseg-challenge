# Log Monitoring Tool

This script analyzes a CSV-formatted log file containing job start and end entries. It calculates the duration of each job and reports any that exceed predefined time thresholds.

## Features

- Parses log entries to track job durations.
- Reports jobs as:
  - `WARNING` if duration > 5 minutes
  - `ERROR` if duration > 10 minutes
  - `INCOMPLETE` if either START or END is missing
- Ignores jobs that complete in under 5 minutes.

## Usage

### Run the script

```bash
python log_monitor.py path/to/logs.log
```

### Example

```bash
python log_monitor.py logs.log
```

Output will display only jobs with warnings, errors, or incomplete data.

## Log File Format

CSV format with the following structure:

```
HH:MM:SS, job description, START|END, PID
```

Example:

```
11:35:23,scheduled task 032, START,37980
11:35:56,scheduled task 032, END,37980
```

## Requirements

- Python 3.x

No external libraries required.

## Running Tests

A test suite is included in `test_logger.py` to validate the main functions.

### To run the tests:

Ensure you are in the same directory as `log_monitor.py` and `test_logger.py`, then run:

```bash
python -m unittest test_logger.py
```