
import tkinter as tk
import time
from tkinter import filedialog
import winsound
import os
import keyboard
import ctypes
import sys

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")
        master.geometry("300x250")
        master.attributes('-topmost', True)  # Make the window always on top

        # Overlay transparent canvas with light gray background
        self.canvas = tk.Canvas(master, bg="light gray", highlightthickness=0)  # Use light gray background color
        self.canvas.place(relwidth=1, relheight=1)

        # Check if the configuration file exists
        self.config_file_path = "timersconfig.txt"
        if not os.path.exists(self.config_file_path):
            # If the file doesn't exist, create it with default settings
            self.create_default_config()

        # Load configuration settings
        self.load_config()

        self.timers = []

        self.button_715 = tk.Button(master, text="7:15", command=lambda: self.add_timer(7, 15))
        self.button_715.grid(row=0, column=0, sticky=tk.W)

        self.button_710 = tk.Button(master, text="7:10", command=lambda: self.add_timer(7, 10))
        self.button_710.grid(row=0, column=1, sticky=tk.W)

        self.button_7 = tk.Button(master, text="7:00", command=lambda: self.add_timer(7, 0))
        self.button_7.grid(row=0, column=2, sticky=tk.W)

        self.sort_button = tk.Button(master, text="Sort Timers", command=self.sort_timers)
        self.sort_button.grid(row=0, column=3, sticky=tk.W)

        self.custom_frame = tk.Frame(master)
        self.custom_frame.grid(row=1, columnspan=4)

        self.minutes_label = tk.Label(self.custom_frame, text="M:")
        self.minutes_label.grid(row=0, column=0, sticky=tk.W)

        self.minutes = tk.Entry(self.custom_frame, width=3)
        self.minutes.grid(row=0, column=1)

        self.seconds_label = tk.Label(self.custom_frame, text="S:")
        self.seconds_label.grid(row=0, column=2, sticky=tk.W)

        self.seconds = tk.Entry(self.custom_frame, width=3)
        self.seconds.grid(row=0, column=3)

        self.add_button = tk.Button(self.custom_frame, text="Add", command=self.add_custom_timer)
        self.add_button.grid(row=0, column=4)

        self.timer_display_frame = tk.Frame(master)
        self.timer_display_frame.grid(row=2, columnspan=4, sticky=tk.W)

        self.select_sound_button = tk.Button(master, text="Select Sound", command=self.select_sound_file)
        self.select_sound_button.grid(row=1, column=4, columnspan=4)

        self.update_timers()

    def select_sound_file(self):
        self.sound_file_path = filedialog.askopenfilename(filetypes=[("Sound files", "*.wav")])
        # Write the sound file path to the configuration file
        with open(self.config_file_path, 'r+') as config_file:
            lines = config_file.readlines()
            config_file.seek(0)
            for line in lines:
                if line.startswith("Sound File Path"):
                    config_file.write(f"Sound File Path: {self.sound_file_path}\n")
                else:
                    config_file.write(line)

        # Set up sound
        self.setup_sound()

    def load_config(self):
        # Load configuration from the file
        self.sound_file_path = ""
        self.background_color = "light gray"  # Default background color
        with open(self.config_file_path, 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                if line.startswith("Sound File Path"):
                    self.sound_file_path = line.split(':', 1)[1].strip()  # Extract the path part after the colon
                elif line.startswith("Background Color"):
                    self.background_color = line.split(':', 1)[1].strip()  # Extract the background color
                elif line.startswith("Hot Key for timer"):
                    index = int(line.split(':')[0][-1]) - 1  # Extract index from the line
                    hotkey = line.split(':')[1].strip()  # Extract hotkey from the line
                    # Bind hotkey to add_timer method with appropriate arguments
                    keyboard.add_hotkey(hotkey, self.handle_hotkey, args=(index,))
                elif line.startswith("Hot Key for Sort"):
                    hotkey = line.split(':')[1].strip()
                    keyboard.add_hotkey(hotkey, self.sort_timers)

        if self.sound_file_path:
            self.setup_sound()

        # Apply background color to the canvas
        self.canvas.config(bg=self.background_color)

    def handle_hotkey(self, index):
        if index == 0:
            self.add_timer(7, 15)
        elif index == 1:
            self.add_timer(7, 10)
        elif index == 2:
            self.add_timer(7, 0)

    def setup_sound(self):
        # Set up sound file from the configuration
        if os.path.exists(self.sound_file_path):
            winsound.PlaySound(None, winsound.SND_FILENAME)  # Stop any currently playing sound
            winsound.PlaySound(self.sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def create_default_config(self):
        # Create a default configuration file with default settings
        with open(self.config_file_path, 'w') as config_file:
            config_file.write("# Default Timer Configuration\n")
            config_file.write("Hot Key Setting\n")
            config_file.write("Hot Key for timer 1: ctrl+1\n")
            config_file.write("Hot Key for timer 2: ctrl+2\n")
            config_file.write("Hot Key for timer 3: ctrl+3\n")
            config_file.write("Hot Key for Sort: ctrl+4\n")
            config_file.write("Sound File Path:\n")
            config_file.write("Background Color: light gray\n")  # Default background color

    def add_timer(self, minutes, seconds):
        end_time = time.time() + (minutes * 60) + seconds
        self.timers.append(end_time)

    def add_custom_timer(self):
        minutes = int(self.minutes.get())
        seconds = int(self.seconds.get())
        self.add_timer(minutes, seconds)

    def sort_timers(self):
        self.timers.sort()

    def clear_timer(self, timer_index):
        if 0 <= timer_index < len(self.timers):
            del self.timers[timer_index]

    def update_timers(self):
        current_time = time.time()
        expired_timers = []

        for end_time in self.timers:
            remaining_time = end_time - current_time
            if remaining_time <= 0:
                expired_timers.append(end_time)

        for expired_timer in expired_timers:
            self.timers.remove(expired_timer)
            self.play_sound()  # Play sound when timer hits 0

        self.display_timers(expired_timers)

        self.master.after(1000, self.update_timers)

    def display_timers(self, expired_timers):
        # Clear existing display
        for widget in self.timer_display_frame.winfo_children():
            widget.destroy()

        # Set background color of the timer display frame
        self.timer_display_frame.config(bg=self.background_color)

        # Display remaining timers
        for i, end_time in enumerate(self.timers):
            remaining_time = end_time - time.time()
            if remaining_time > 0:
                mins, secs = divmod(int(remaining_time), 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                timer_label = tk.Label(self.timer_display_frame, text=timer_str)
                timer_label.grid(row=i, column=0, sticky=tk.W)
                clear_button = tk.Button(self.timer_display_frame, text="Clear",
                                         command=lambda index=i: self.clear_timer(index))
                clear_button.grid(row=i, column=1, sticky=tk.W)

    def play_sound(self):
        if self.sound_file_path and os.path.exists(self.sound_file_path):
            winsound.PlaySound(None, winsound.SND_FILENAME)  # Stop any currently playing sound
            winsound.PlaySound(self.sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TimerApp(root)
        root.mainloop()
    except Exception as e:
        # Redirect standard output and error streams to a file
        sys.stdout = open("output.txt", "w")
        sys.stderr = open("error.txt", "w")
        print("An error occurred:", e)
        input("Press Enter to exit...")
