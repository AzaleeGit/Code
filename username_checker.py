import aiohttp
import asyncio
import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.label import Label

# Roblox API for checking username availability
ROBLOX_USERNAME_CHECK_URL = "https://auth.roblox.com/v1/usernames/validate"
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

NUM_TASKS = 10  # Number of usernames checked at the same time
running = False
total_checked = 0
available_count = 0

# Default settings
username_length = 5  # Default length
include_digits = True  # Default: include numbers


# Generate a random username based on user settings
def generate_username():
    characters = string.ascii_lowercase
    if include_digits:
        characters += string.digits
    return ''.join(random.choice(characters) for _ in range(username_length))


# Async function to check username availability
async def check_username_status(username, session):
    global total_checked, available_count
    payload = {"username": username, "context": "Signup"}
    headers = {"User-Agent": "Brave/120.0.0.0 Chrome/120.0.0.0 Safari/537.36"}

    try:
        async with session.post(ROBLOX_USERNAME_CHECK_URL, json=payload, headers=headers, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                code = data.get("code", -1)

                if code == 0:
                    available_count += 1
                    await send_discord_notification(username)
                    with open("available_usernames.txt", "a") as file:
                        file.write(username + "\n")
                    return f"✅ {username} is Available!"
                elif code == 1:
                    return f"❌ {username} is Taken"
                elif code == 2:
                    return f"🚫 {username} is Censored"
                elif code == 3:
                    return f"⚠ Invalid Username"
            return f"⚠ Unknown Error {response.status}"
    except asyncio.TimeoutError:
        return f"❌ Timeout Error ({username})"
    except Exception as e:
        return f"❌ Network Error ({username})"


# Async function to send a Discord notification
async def send_discord_notification(username):
    payload = {"content": f"🔥 Available Roblox Username Found: **{username}**"}
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers, timeout=5):
            pass  # Ignore errors


# Async task to run multiple username checks in parallel
async def run_username_checks(log_function):
    global running, total_checked

    async with aiohttp.ClientSession() as session:
        while running:
            usernames = [generate_username() for _ in range(NUM_TASKS)]  # Batch checking
            tasks = [check_username_status(username, session) for username in usernames]
            results = await asyncio.gather(*tasks)

            total_checked += len(usernames)

            # ✅ Update UI safely using Kivy's main thread
            for result in results:
                Clock.schedule_once(lambda dt: log_function(f"{result} | Checked: {total_checked}, Found: {available_count}"))

            await asyncio.sleep(0.5)  # Adjust this to avoid rate limits


# Kivy UI
class UsernameCheckerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.log_box = TextInput(readonly=True, size_hint=(1, 0.6))

        scroll_view = ScrollView(size_hint=(1, 0.6), do_scroll_x=False, do_scroll_y=True, bar_width=10)
        scroll_view.add_widget(self.log_box)
        self.layout.add_widget(scroll_view)

        # Username length slider
        length_layout = BoxLayout(size_hint=(1, 0.1))
        self.length_label = Label(text="Username Length: 5", size_hint=(0.4, 1))
        self.length_slider = Slider(min=3, max=10, value=5, step=1, size_hint=(0.6, 1))
        self.length_slider.bind(value=self.update_length)
        length_layout.add_widget(self.length_label)
        length_layout.add_widget(self.length_slider)
        self.layout.add_widget(length_layout)

        # Toggle button for including digits
        self.toggle_button = ToggleButton(text="Include Digits: ON", state="down", size_hint=(1, 0.1))
        self.toggle_button.bind(on_press=self.toggle_digits)
        self.layout.add_widget(self.toggle_button)

        button_layout = BoxLayout(size_hint=(1, 0.2))

        self.start_button = Button(text="Start", background_color=(0, 1, 0, 1))
        self.start_button.bind(on_press=self.start_checker)
        button_layout.add_widget(self.start_button)

        self.stop_button = Button(text="Stop", background_color=(1, 0, 0, 1))
        self.stop_button.bind(on_press=self.stop_checker)
        button_layout.add_widget(self.stop_button)

        self.layout.add_widget(button_layout)
        return self.layout

    def log_message(self, message):
        """ ✅ Safe UI update using Kivy main thread """
        self.log_box.text += message + "\n"

    def start_checker(self, instance):
        global running
        if not running:
            running = True
            self.log_message(f"🚀 Starting username checker... Length: {username_length}, Digits: {'ON' if include_digits else 'OFF'}")
            asyncio.create_task(run_username_checks(self.log_message))  # ✅ Run async function in background

    def stop_checker(self, instance):
        global running
        running = False
        self.log_message("🛑 Stopping username checker...")

    def update_length(self, instance, value):
        global username_length
        username_length = int(value)
        self.length_label.text = f"Username Length: {username_length}"

    def toggle_digits(self, instance):
        global include_digits
        include_digits = not include_digits
        self.toggle_button.text = f"Include Digits: {'ON' if include_digits else 'OFF'}"


# Run the Kivy App
if __name__ == "__main__":
    UsernameCheckerApp().run()
