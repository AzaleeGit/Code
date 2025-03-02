import requests
import random
import string
import threading
import time

# Roblox API for checking username availability
ROBLOX_USERNAME_CHECK_URL = "https://auth.roblox.com/v1/usernames/validate"

# Replace with your actual Discord Webhook URL (if you want notifications)
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

NUM_THREADS = 5  # Number of threads to use for checking
running = False  # Global flag to control checking

# Function to generate random usernames
def generate_username(length=5, use_digits=True):
    characters = string.ascii_lowercase
    if use_digits:
        characters += string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to check username availability
def check_username_status(username, session):
    payload = {"username": username, "context": "Signup"}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = session.post(ROBLOX_USERNAME_CHECK_URL, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            code = data.get("code", -1)

            if code == 0:
                return "✅ Available"
            elif code == 1:
                return "❌ Taken"
            elif code == 2:
                return "🚫 Censored"
            elif code == 3:
                return "⚠ Invalid"
        return "⚠ Unknown Error"
    except requests.exceptions.RequestException:
        return "❌ Network Error"

# Function to send a Discord notification
def send_discord_notification(username):
    payload = {"content": f"🔥 Available Roblox Username Found: **{username}**"}
    headers = {"Content-Type": "application/json"}

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        pass  # Ignore errors if Discord webhook fails

# Background function to check usernames
def check_usernames(length, use_digits):
    session = requests.Session()
    checked = 0
    found = 0
    while running:
        username = generate_username(length, use_digits)
        status = check_username_status(username, session)
        checked += 1

        # Log the status
        print(f"{username} → {status}")

        if status == "✅ Available":
            found += 1
            with open("available_usernames.txt", "a") as file:
                file.write(username + "\n")
            send_discord_notification(username)

        # Report checked and found usernames
        print(f"Checked: {checked}, Found: {found}")

        time.sleep(0.2)  # Prevent IP ban

# Function to start the checker
def start_checker(length, use_digits):
    global running
    if not running:
        running = True
        print("🚀 Starting username checker...")
        for _ in range(NUM_THREADS):
            thread = threading.Thread(target=check_usernames, args=(length, use_digits), daemon=True)
            thread.start()

# Function to stop the checker
def stop_checker():
    global running
    running = False
    print("🛑 Stopping username checker...")

# Main program
def main():
    print("Welcome to the Roblox Username Checker!")
    
    # Get the length of the username from user input
    try:
        length = int(input("Enter the length of the username: "))
    except ValueError:
        print("Invalid input! Using default length of 5.")
        length = 5

    # Ask if digits should be included in the username
    use_digits_input = input("Include digits in the username? (y/n): ").lower()
    use_digits = use_digits_input == 'y'

    # Start the username checking process
    start_checker(length, use_digits)

    try:
        while True:
            # Keep the program running, check periodically
            time.sleep(1)
    except KeyboardInterrupt:
        stop_checker()

if __name__ == "__main__":
    main()
