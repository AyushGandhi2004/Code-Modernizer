# log_parser_legacy.py
# Python 2.x log analyzer

import re

def parse_log_line(line):
    pattern = r"(\d{4}-\d{2}-\d{2})\s+(\w+)\s+(.*)"
    match = re.match(pattern, line)
    if match:
        return match.groups()
    return None

def analyze_log(file_path):
    errors = 0
    warnings = 0
    info = 0

    try:
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            parsed = parse_log_line(line)
            if parsed:
                date, level, message = parsed
                if level == "ERROR":
                    errors += 1
                elif level == "WARNING":
                    warnings += 1
                elif level == "INFO":
                    info += 1

        print "Log Summary:"
        print "Errors:", errors
        print "Warnings:", warnings
        print "Info:", info

    except Exception, e:
        print "Failed to analyze log:", e

def main():
    file_path = raw_input("Enter log file path: ")
    analyze_log(file_path)

if __name__ == "__main__":
    main()
