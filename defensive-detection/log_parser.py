from collections import Counter
from datetime import datetime

def parse_log(file_path):
    attempts = []
    timeline = []

    with open(file_path, "r") as log:
        for line in log:
            if "Failed login attempt" in line:
                parts = line.strip().split(": ")[-1]
                username = parts.split(" / ")[0]
                attempts.append(username)

                # Extract timestamp
                timestamp_str = line.split("]")[0].strip("[")
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                timeline.append(timestamp.strftime("%Y-%m-%d %H:%M"))

    user_count = Counter(attempts)
    time_count = Counter(timeline)

    print("Suspicious usernames:")
    for user, freq in user_count.items():
        if freq >= 3:
            print(f"- {user}: {freq} failed attempts")

    print("\nActivity timeline:")
    for time, freq in sorted(time_count.items()):
        print(f"{time}: {freq} attempts")

if __name__ == "__main__":
    parse_log("../offensive-simulation/brute_force.log")

