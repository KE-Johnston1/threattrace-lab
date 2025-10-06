from collections import Counter

def parse_log(file_path):
    attempts = []

    with open(file_path, "r") as log:
        for line in log:
            if "Failed login attempt" in line:
                parts = line.strip().split(": ")[-1]
                username = parts.split(" / ")[0]
                attempts.append(username)

    count = Counter(attempts)
    print("Suspicious activity report:")
    for user, freq in count.items():
        if freq >= 3:
            print(f"⚠️ {user} failed {freq} times")

if __name__ == "__main__":
    parse_log("../offensive-simulation/brute_force.log")
