#!/usr/bin/python3
import sys
import signal

# Initialize metrics
total_file_size = 0
status_codes = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
valid_status_codes = [200, 301, 400, 401, 403, 404, 405, 500]
line_count = 0

def print_stats():
    """Function to print the computed metrics"""
    print(f"File size: {total_file_size}")
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print(f"{code}: {status_codes[code]}")

def handle_interrupt(sig, frame):
    """Signal handler for keyboard interruption (CTRL + C)"""
    print_stats()
    sys.exit(0)

# Register the signal handler for keyboard interruption
signal.signal(signal.SIGINT, handle_interrupt)

try:
    for line in sys.stdin:
        try:
            parts = line.split()
            # Validate the line format
            if len(parts) < 7 or parts[2] != '"GET' or parts[3] != '/projects/260' or parts[4] != 'HTTP/1.1"':
                continue
            # Extract the status code and file size
            status_code = int(parts[-2])
            file_size = int(parts[-1])
            
            # Update total file size
            total_file_size += file_size

            # Update the status code count if valid
            if status_code in valid_status_codes:
                status_codes[status_code] += 1

            line_count += 1

            # Print stats after every 10 lines
            if line_count % 10 == 0:
                print_stats()

        except (ValueError, IndexError):
            # Ignore lines with invalid format
            continue

except KeyboardInterrupt:
    # Handle CTRL + C gracefully
    print_stats()
    sys.exit(0)
