import pandas as pd
import re
from datetime import datetime

# Load log file
with open("mock-honeypot.log", "r") as file:
    lines = file.readlines()

# Parse log entries
data = []
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) Connection from ([\d\.]+) to port (\d+)"
for line in lines:
    match = re.search(pattern, line)
    if match:
        timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        ip = match.group(2)
        port = int(match.group(3))
        data.append({"Time": timestamp, "IP": ip, "Port": port})

df = pd.DataFrame(data)

# Detect anomalies: IPs with >2 hits
ip_counts = df["IP"].value_counts()
anomalies = ip_counts[ip_counts > 2]

print("Anomalous IPs with high activity:")
print(anomalies)
