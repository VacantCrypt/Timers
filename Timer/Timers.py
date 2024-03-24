import tkinter as tk
import time

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Timer App")
        master.geometry("300x200")
        master.attributes('-topmost', True)  # Make the window always on top

        self.timers = []

        self.button = tk.Button(master, text="Add Timer (7 mins 15 seconds)", command=self.add_timer)
        self.button.pack()

        self.timer_display = tk.Label(master, text="Timers:")
        self.timer_display.pack()

        self.update_timers()

    def add_timer(self):
        end_time = time.time() + (7 * 60) +15  # 7 minutes from now
        self.timers.append(end_time)

    def update_timers(self):
        current_time = time.time()
        expired_timers = []

        timer_texts = []

        for end_time in self.timers:
            remaining_time = end_time - current_time
            if remaining_time <= 0:
                expired_timers.append(end_time)
            else:
                mins, secs = divmod(int(remaining_time), 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                timer_texts.append(timer_str)
        
        self.timer_display.config(text="Timers:\n" + "\n".join(timer_texts))
        
        for expired_timer in expired_timers:
            self.timers.remove(expired_timer)

        self.master.after(1000, self.update_timers)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
