from datetime import datetime

def build_timeline(file_path):
    timeline = []

    with open(file_path, "r") as log:
        for line in log:
            if "Failed login attempt" in line:
                timestamp_str = line.split("]")[0].strip("[")
                username = line.strip().split(": ")[-1].split(" / ")[0]
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                timeline.append((timestamp, username))

    timeline.sort()
    print("Incident Timeline:")
    for entry in timeline:
        print(f"{entry[0]} - Failed login by '{entry[1]}'")

if __name__ == "__main__":
    build_timeline("../offensive-simulation/brute_force.log")
