import tkinter as tk
import time

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")
        master.geometry("300x250")
        master.attributes('-topmost', True)  # Make the window always on top

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

        self.update_timers()

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

        self.display_timers(expired_timers)

        self.master.after(1000, self.update_timers)

    def display_timers(self, expired_timers):
        # Clear existing display
        for widget in self.timer_display_frame.winfo_children():
            widget.destroy()

        # Display remaining timers
        for i, end_time in enumerate(self.timers):
            remaining_time = end_time - time.time()
            if remaining_time > 0:
                mins, secs = divmod(int(remaining_time), 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                timer_label = tk.Label(self.timer_display_frame, text=timer_str)
                timer_label.grid(row=i, column=0, sticky=tk.W)
                clear_button = tk.Button(self.timer_display_frame, text="Clear", command=lambda index=i: self.clear_timer(index))
                clear_button.grid(row=i, column=1, sticky=tk.W)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
