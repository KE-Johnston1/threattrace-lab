from collections import Counter
from datetime import datetime

def extract_iocs(file_path):
    usernames = []
    timestamps = []

    with open(file_path, "r") as log:
        for line in log:
            if "Failed login attempt" in line:
                # Extract username
                parts = line.strip().split(": ")[-1]
                username = parts.split(" / ")[0]
                usernames.append(username)

                # Extract timestamp
                timestamp_str = line.split("]")[0].strip("[")
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(timestamp.strftime("%Y-%m-%d %H:%M:%S"))

    user_count = Counter(usernames)
    print("Extracted IOCs:")
    print("\nUsernames:")
    for user, freq in user_count.items():
        print(f"- {user} ({freq} attempts)")

    print("\nTimestamps:")
    for ts in timestamps:
        print(f"- {ts}")

if __name__ == "__main__":
    extract_iocs("../offensive-simulation/brute_force.log")
