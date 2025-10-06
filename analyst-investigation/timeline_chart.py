import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

def build_chart(file_path):
    timeline = []

    with open(file_path, "r") as log:
        for line in log:
            if "Failed login attempt" in line:
                timestamp_str = line.split("]")[0].strip("[")
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                timeline.append(timestamp.strftime("%Y-%m-%d %H:%M"))

    count = Counter(timeline)
    times = sorted(count.keys())
    attempts = [count[t] for t in times]

    plt.figure(figsize=(10, 5))
    plt.plot(times, attempts, marker='o', linestyle='-', color='red')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Time")
    plt.ylabel("Failed Login Attempts")
    plt.title("SSH Brute Force Timeline")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    build_chart("../offensive-simulation/brute_force.log")

