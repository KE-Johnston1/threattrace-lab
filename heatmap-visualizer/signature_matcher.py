import re

# Load log file
with open("mock-honeypot.log", "r") as file:
    lines = file.readlines()

# Define simple tool signatures (expandable)
signatures = {
    "Nmap": r"port 22|port 80|port 443",
    "Masscan": r"Connection from .* to port \d{1,5}",
    "Brute Force": r"Connection from .* to port 22"
}

# Scan logs
for tool, pattern in signatures.items():
    print(f"\nChecking for {tool} signature:")
    for line in lines:
        if re.search(pattern, line):
            print(f"  Match: {line.strip()}")
