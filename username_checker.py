import requests
import random
import string
import os
import threading
from colorama import Fore, Style, init

# Initialize color output
init()

# Ensure the valid username file exists
if not os.path.exists("valid_username.txt"):
    open("valid_username.txt", "w").close()

# Discord Webhook URL (replace with your webhook)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1226527204423241791/sSa3dSPW-vWmp9iuWxVYdPxG89M6G_HcRVjCERAg9FDzshyadePxvB5sErD-GYXXN5_Y"

# Character sets
character = string.ascii_letters + string.digits
lower = string.ascii_lowercase
upper = string.ascii_uppercase
digits = string.digits

# User input for username length and type
username_length = int(input("How long should the username be? : "))
username_type = input(
    "What type of username do you want?\n"
    "[1] | All characters\n"
    "[2] | Only letters\n"
    "[3] | Only lowercase\n"
    "[4] | Only uppercase\n"
    "[5] | Only digits\n"
    "Answer: "
)

# Define character selection based on user choice
if username_type == "1":
    selected_chars = character
elif username_type == "2":
    selected_chars = string.ascii_letters
elif username_type == "3":
    selected_chars = lower
elif username_type == "4":
    selected_chars = upper
elif username_type == "5":
    selected_chars = digits
else:
    print(Fore.RED + "Invalid choice, using all characters." + Style.RESET_ALL)
    selected_chars = character

# Use a session for faster requests
session = requests.Session()

# Buffer for bulk writing to file
valid_usernames = []
buffer_lock = threading.Lock()  # Prevent multiple threads from writing at the same time

# Counter to limit "TAKEN" prints
taken_counter = 0
taken_lock = threading.Lock()

# Function to generate a random username quickly
def generate_username(length):
    return ''.join(selected_chars[b % len(selected_chars)] for b in os.urandom(length))

# Function to send a Discord notification
def send_discord_notification(username):
    try:
        payload = {"content": f"✅ **Valid Roblox Username Found!** 🎉\n`{username}`"}
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        pass  # Ignore errors to avoid slowdowns

# Function to check username availability
def check_username():
    global valid_usernames, taken_counter
    while True:
        username = generate_username(username_length)
        url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"

        try:
            response = session.get(url, timeout=3)
            response.raise_for_status()
            response_data = response.json()

            code = response_data.get("code")
            
            if code == 0:  # Available username
                print(Fore.GREEN + f"[VALID] | {username}" + Style.RESET_ALL)
                send_discord_notification(username)  # Send to Discord
                with buffer_lock:
                    valid_usernames.append(f"{username} | {len(username)}\n")

                    # Write in bulk every 10 usernames to reduce file I/O overhead
                    if len(valid_usernames) >= 10:
                        with open("valid_username.txt", "a") as file:
                            file.writelines(valid_usernames)
                        valid_usernames.clear()
            
            elif code == 1:  # Username is taken
                with taken_lock:
                    taken_counter += 1
                    if taken_counter % 10 == 0:  # Print only 1 out of every 10 taken usernames
                        print(Fore.RED + f"[TAKEN] | {username}" + Style.RESET_ALL)
            
            elif code == 2:  # Username is censored (filtered by Roblox)
                print(Fore.YELLOW + f"[CENSORED] | {username}" + Style.RESET_ALL)

        except requests.exceptions.RequestException:
            pass  # Ignore failed requests for maximum speed

# Limit to 10 threads
num_threads = 10
# Start multi-threaded checking
if __name__ == "__main__":
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=check_username)
        thread.daemon = True  # Allows threads to close when main program stops
        thread.start()
        threads.append(thread)

    # Keep the main thread alive to let worker threads run
    for thread in threads:
        thread.join()
