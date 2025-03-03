import requests
import random
import string
import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from colorama import init

# Initialize colorama
init()

# Ensure the valid_username.txt file exists
if not os.path.exists("valid_username.txt"):
    with open("valid_username.txt", "w") as file:
        file.write("")  # Create an empty file

# Discord Webhook URL (replace with your webhook)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1226527204423241791/sSa3dSPW-vWmp9iuWxVYdPxG89M6G_HcRVjCERAg9FDzshyadePxvB5sErD-GYXXN5_Y"

# Character sets
char_sets = {
    "All Characters": string.ascii_letters + string.digits,
    "Only Letters": string.ascii_letters,
    "Only Lowercase": string.ascii_lowercase,
    "Only Uppercase": string.ascii_uppercase,
    "Only Digits": string.digits
}

# Use a session for faster requests
session = requests.Session()

# Buffer for bulk writing to file
valid_usernames = []
buffer_lock = threading.Lock()

# Counter to limit "TAKEN" prints
taken_counter = 0
taken_lock = threading.Lock()

# GUI Class
class UsernameCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Username Checker")
        self.root.geometry("500x400")

        # Username Length
        ttk.Label(root, text="Username Length:").pack(pady=5)
        self.username_length = tk.IntVar(value=5)
        ttk.Entry(root, textvariable=self.username_length, width=10).pack()

        # Username Type Dropdown
        ttk.Label(root, text="Username Type:").pack(pady=5)
        self.username_type = tk.StringVar(value="All Characters")
        ttk.Combobox(root, textvariable=self.username_type, values=list(char_sets.keys()), state="readonly").pack()

        # Start/Stop Buttons
        self.start_button = ttk.Button(root, text="Start", command=self.start_checker)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_checker, state="disabled")
        self.stop_button.pack()

        # Result Output Box
        self.output_box = scrolledtext.ScrolledText(root, width=60, height=15, state="normal", font=("Courier", 10))
        self.output_box.pack(pady=10)
        self.output_box.tag_config("valid", foreground="green")
        self.output_box.tag_config("taken", foreground="red")
        self.output_box.tag_config("censored", foreground="orange")

        self.stop_event = threading.Event()  # Event to stop threads
        self.threads = []  # Store threads

    def log_message(self, message, tag="normal"):
        """ Logs messages in the GUI output box with colors. """
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, message + "\n", tag)
        self.output_box.config(state="disabled")
        self.output_box.yview(tk.END)  # Auto-scroll

    def send_discord_notification(self, username):
        """ Sends a notification to Discord. """
        try:
            payload = {"content": f"✅ **Valid Roblox Username Found!** 🎉\n`{username}`"}
            requests.post(DISCORD_WEBHOOK, json=payload, timeout=5)
        except requests.exceptions.RequestException:
            pass

    def generate_username(self, length):
        """ Generates a random username. """
        selected_chars = char_sets[self.username_type.get()]
        return ''.join(selected_chars[b % len(selected_chars)] for b in os.urandom(length))

    def check_username(self):
        """ Checks if a username is available. """
        global valid_usernames, taken_counter
        while not self.stop_event.is_set():  # Instead of while True, check stop event
            username = self.generate_username(self.username_length.get())
            url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"

            try:
                response = session.get(url, timeout=3)
                response.raise_for_status()
                response_data = response.json()

                code = response_data.get("code")
                
                if code == 0:  # Available
                    self.log_message(f"[VALID] | {username}", "valid")
                    self.send_discord_notification(username)
                    with buffer_lock:
                        valid_usernames.append(f"{username} | {len(username)}\n")
                        if len(valid_usernames) >= 10:
                            with open("valid_username.txt", "a") as file:
                                file.writelines(valid_usernames)
                            valid_usernames.clear()

                elif code == 1:  # Taken
                    with taken_lock:
                        taken_counter += 1
                        if taken_counter % 10 == 0:  # Reduce spam
                            self.log_message(f"[TAKEN] | {username}", "taken")

                elif code == 2:  # Censored
                    self.log_message(f"[CENSORED] | {username}", "censored")

            except requests.exceptions.RequestException:
                pass

    def start_checker(self):
        """ Starts the username checking process in a separate thread. """
        self.stop_event.clear()  # Reset stop event
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.threads = []
        for _ in range(10):  # 10 threads for speed
            thread = threading.Thread(target=self.check_username)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_checker(self):
        """ Stops the username checking process. """
        self.stop_event.set()  # Signal threads to stop

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        # Wait for threads to stop safely
        for thread in self.threads:
            thread.join(timeout=1)  # Give threads a chance to exit safely

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = UsernameCheckerApp(root)
    root.mainloop()
