import time
import random

usernames = ["admin", "root", "user", "test"]
passwords = ["123456", "password", "letmein", "admin123"]

def simulate_brute_force():
    for i in range(20):
        username = random.choice(usernames)
        password = random.choice(passwords)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Failed login attempt: {username} / {password}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate delay

if __name__ == "__main__":
    simulate_brute_force()
