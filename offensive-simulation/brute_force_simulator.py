import time
import random

usernames = ["admin", "root", "user", "test"]
passwords = ["123456", "password", "letmein", "admin123"]

def simulate_brute_force():
    for i in range(20):
        username = random.choice(usernames)
        password = random.choice(passwords)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("brute_force.log", "a") as log_file:
            log_file.write(f"[{timestamp}] Failed login attempt: {username} / {password}\n")
        time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    simulate_brute_force()

