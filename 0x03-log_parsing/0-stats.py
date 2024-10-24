#!/usr/bin/python3
"""
Log parsing script that reads from stdin and computes metrics.
"""
import sys
import signal


def print_statistics(total_file_size, status_code_count):
    """
    Prints the file size and the count of status codes.
    """
    print("File size: {}".format(total_file_size))
    for code in sorted(status_code_count.keys()):
        if status_code_count[code] > 0:
            print("{}: {}".format(code, status_code_count[code]))


def process_line(line, total_file_size, status_code_count):
    """
    Processes a single line of input to update file size and status codes.
    """
    try:
        parts = line.split()
        if len(parts) < 7:
            return total_file_size  # Skip malformed line

        file_size = int(parts[-1])
        status_code = parts[-2]

        total_file_size += file_size

        if status_code in status_code_count:
            status_code_count[status_code] += 1

    except (ValueError, IndexError):
        pass  # Ignore lines with formatting issues

    return total_file_size


def signal_handler(sig, frame):
    """
    Signal handler for keyboard interruption (CTRL + C).
    """
    print_statistics(total_file_size, status_code_count)
    sys.exit(0)


# Main execution
if __name__ == "__main__":
    total_file_size = 0
    status_code_count = {
        "200": 0, "301": 0, "400": 0, "401": 0,
        "403": 0, "404": 0, "405": 0, "500": 0
    }
    line_count = 0

    # Set up signal handler for graceful exit on keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    try:
        for line in sys.stdin:
            total_file_size = process_line(line.strip(), total_file_size, status_code_count)
            line_count += 1

            if line_count % 10 == 0:
                print_statistics(total_file_size, status_code_count)

    except KeyboardInterrupt:
        print_statistics(total_file_size, status_code_count)
        raise

    # Print final statistics after EOF
    print_statistics(total_file_size, status_code_count)
