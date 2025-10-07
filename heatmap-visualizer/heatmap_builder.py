import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import argparse
import re
from datetime import datetime

# CLI setup
parser = argparse.ArgumentParser(description="Generate honeypot heatmap from log file.")
parser.add_argument("--log", type=str, default="mock-honeypot.log", help="Path to honeypot log file")
parser.add_argument("--filter-port", type=int, help="Only include entries for this port")
parser.add_argument("--save", type=str, help="Path to save heatmap image (e.g. heatmap.png)")
args = parser.parse_args()

# Load log file
with open(args.log, "r") as file:
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
        if args.filter_port and port != args.filter_port:
            continue
        data.append({"Time": timestamp, "IP": ip, "Port": port})

df = pd.DataFrame(data)

# Create heatmap
pivot = df.pivot_table(index=df["Time"].dt.strftime("%H:%M"), columns="Port", aggfunc="count", fill_value=0)
plt.figure(figsize=(10, 6))
plt.title("Honeypot Interaction Heatmap")
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5)
plt.xlabel("Port")
plt.ylabel("Time")
plt.tight_layout()

if args.save:
    plt.savefig(args.save)
    print(f"Heatmap saved to {args.save}")
else:
    plt.show()

