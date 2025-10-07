import matplotlib.pyplot as plt
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

# Convert to DataFrame
df = pd.DataFrame(data)

# Create heatmap: Time vs Port
pivot = df.pivot_table(index=df["Time"].dt.strftime("%H:%M"), columns="Port", aggfunc="count", fill_value=0)
plt.figure(figsize=(10, 6))
plt.title("Honeypot Interaction Heatmap")
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5)
plt.xlabel("Port")
plt.ylabel("Time")
plt.tight_layout()
plt.show()
