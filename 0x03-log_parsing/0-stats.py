#!/usr/bin/python3
'''A script that reads stdin line by line and computes metrics.'''

import sys
import re

def print_statistics(total_file_size, status_codes_stats):
    '''Prints the accumulated statistics of the HTTP request log.'''
    print(f"File size: {total_file_size}")
    for code in sorted(status_codes_stats):
        if status_codes_stats[code] > 0:
            print(f"{code}: {status_codes_stats[code]}")

def update_metrics(line, total_file_size, status_codes_stats):
    '''Extracts metrics from the line and updates statistics.'''
    log_fmt = r'(?P<ip>\S+) - \[.*?\] "GET /projects/260 HTTP/1.1" (?P<status_code>\d{3}) (?P<file_size>\d+)'
    match = re.match(log_fmt, line)
    
    if match:
        file_size = int(match.group('file_size'))
        status_code = match.group('status_code')
        total_file_size += file_size
        if status_code in status_codes_stats:
            status_codes_stats[status_code] += 1
    
    return total_file_size

def run():
    '''Starts the log parser.'''
    total_file_size = 0
    status_codes_stats = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    
    line_num = 0

    try:
        for line in sys.stdin:
            total_file_size = update_metrics(line.strip(), total_file_size, status_codes_stats)
            line_num += 1

            if line_num % 10 == 0:
                print_statistics(total_file_size, status_codes_stats)

    except (KeyboardInterrupt, EOFError):
        print_statistics(total_file_size, status_codes_stats)
        sys.exit(0)

if __name__ == '__main__':
    run()
