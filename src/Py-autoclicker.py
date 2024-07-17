import tkinter as tk
from tkinter import messagebox
import webbrowser
import keyboard
import os
import sys

from autoclicker import AutoClicker

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Py-AutoClicker")

        icon_path = os.path.join(os.path.dirname(__file__), "images", "py-autoclicker.png")

        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"[✘] Icon not founded here : {icon_path}")

        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=icon_path))

        #Default hotkey, you can modifiy it here
        self.start_stop_hotkey = "F6"

        interval_frame = tk.LabelFrame(self.root, text="Click Interval")
        interval_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.hours_entry = tk.Entry(interval_frame, width=5)
        self.hours_entry.insert(0, "0")
        self.hours_entry.grid(row=0, column=0, padx=5, pady=5)
        self.hours_label = tk.Label(interval_frame, text="Hours")
        self.hours_label.grid(row=0, column=1, padx=5, pady=5)

        self.minutes_entry = tk.Entry(interval_frame, width=5)
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.grid(row=0, column=2, padx=5, pady=5)
        self.minutes_label = tk.Label(interval_frame, text="Minutes")
        self.minutes_label.grid(row=0, column=3, padx=5, pady=5)

        self.seconds_entry = tk.Entry(interval_frame, width=5)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.grid(row=0, column=4, padx=5, pady=5)
        self.seconds_label = tk.Label(interval_frame, text="Seconds")
        self.seconds_label.grid(row=0, column=5, padx=5, pady=5)

        self.milliseconds_entry = tk.Entry(interval_frame, width=5)
        self.milliseconds_entry.insert(0, "100")
        self.milliseconds_entry.grid(row=0, column=6, padx=5, pady=5)
        self.milliseconds_label = tk.Label(interval_frame, text="Milliseconds")
        self.milliseconds_label.grid(row=0, column=7, padx=5, pady=5)


        options_frame = tk.LabelFrame(self.root, text="Click Options")
        options_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.button_var = tk.StringVar(self.root)
        self.button_var.set("left")
        self.button_label = tk.Label(options_frame, text="Mouse Button:")
        self.button_label.grid(row=0, column=0, padx=5, pady=5)
        self.button_option = tk.OptionMenu(options_frame, self.button_var, "left", "right", "middle")
        self.button_option.grid(row=0, column=1, padx=5, pady=5)

        self.click_type_var = tk.StringVar(self.root)
        self.click_type_var.set("single")
        self.click_type_label = tk.Label(options_frame, text="Click Type:")
        self.click_type_label.grid(row=1, column=0, padx=5, pady=5)
        self.click_type_option = tk.OptionMenu(options_frame, self.click_type_var, "single", "double")
        self.click_type_option.grid(row=1, column=1, padx=5, pady=5)

    
        repeat_frame = tk.LabelFrame(self.root, text="Click Repeat (Choose)")
        repeat_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.repeat_var = tk.StringVar(self.root)
        self.repeat_var.set("untilStopped")
        self.repeat_until_stopped = tk.Radiobutton(repeat_frame, text="Repeat until stopped", variable=self.repeat_var, value="untilStopped")
        self.repeat_until_stopped.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.repeat_times = tk.Radiobutton(repeat_frame, text="Repeat ... times", variable=self.repeat_var, value="times")
        self.repeat_times.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        self.repeat_times_label = tk.Label(repeat_frame, text="Repeat ... times:")
        self.repeat_times_label.grid(row=2, column=0, padx=5, pady=5)
        self.repeat_times_entry = tk.Entry(repeat_frame, width=5)
        self.repeat_times_entry.grid(row=2, column=1, padx=5, pady=5)


        cursor_frame = tk.LabelFrame(self.root, text="Cursor Position (Choose)")
        cursor_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.cursor_var = tk.StringVar(self.root)
        self.cursor_var.set("current")
        self.current_position = tk.Radiobutton(cursor_frame, text="Current position", variable=self.cursor_var, value="current")
        self.current_position.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.pick_location = tk.Radiobutton(cursor_frame, text="Pick location (x, y)", variable=self.cursor_var, value="pick")
        self.pick_location.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.x_entry = tk.Entry(cursor_frame, width=5, state=tk.DISABLED)
        self.x_entry.grid(row=1, column=1, padx=5, pady=5)
        self.y_entry = tk.Entry(cursor_frame, width=5, state=tk.DISABLED)
        self.y_entry.grid(row=1, column=2, padx=5, pady=5)

        action_frame = tk.Frame(self.root)
        action_frame.grid(row=4, column=0, padx=10, pady=10)

        self.start_btn = tk.Button(action_frame, text=f"Start ({self.start_stop_hotkey})", command=self.start_autoclicker)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        self.stop_btn = tk.Button(action_frame, text=f"Stop ({self.start_stop_hotkey})", command=self.stop_autoclicker, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)

        self.hotkey_settings_btn = tk.Button(action_frame, text="Hotkey Settings", command=self.hotkey_settings)
        self.hotkey_settings_btn.grid(row=0, column=2, padx=5, pady=5)

        self.help_btn = tk.Button(action_frame, text="Help (GitHub)", command=self.open_github)
        self.help_btn.grid(row=0, column=3, padx=5, pady=5)

        self.autoclicker = AutoClicker()
        

        self.pick_location.config(command=self.toggle_location_entries)
        self.current_position.config(command=self.toggle_location_entries)
        

        self.configure_hotkeys()
        
    def toggle_location_entries(self):
        state = tk.NORMAL if self.cursor_var.get() == "pick" else tk.DISABLED
        self.x_entry.config(state=state)
        self.y_entry.config(state=state)
        
    def start_autoclicker(self):
        try:
            interval = (
                int(self.hours_entry.get()) * 3600000 +
                int(self.minutes_entry.get()) * 60000 +
                int(self.seconds_entry.get()) * 1000 +
                int(self.milliseconds_entry.get())
            )
        except ValueError:
            messagebox.showerror("Input Error", "[✘] Please enter valid numbers for the click interval.")
            return
        
        button = self.button_var.get()
        click_type = self.click_type_var.get()
        
        if self.repeat_var.get() == "times":
            try:
                repeat = int(self.repeat_times_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "[✘] Please enter a valid number for repeat times.")
                return
        else:
            repeat = None
        
        if self.cursor_var.get() == "pick":
            try:
                x = int(self.x_entry.get())
                y = int(self.y_entry.get())
                position = (x, y)
            except ValueError:
                messagebox.showerror("Input Error", "[✘] Please enter valid numbers for the cursor position.")
                return
        else:
            position = None
        
        self.autoclicker.start_clicking(interval, button, click_type, repeat, position)
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        print("[✔] AutoClicker started.")

    def stop_autoclicker(self):
        self.autoclicker.stop_clicking()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        print("[✔] AutoClicker stopped.")

    def toggle_clicker(self):
        if self.autoclicker.running:
            self.stop_autoclicker()
        else:
            self.start_autoclicker()

    def hotkey_settings(self):
        messagebox.showinfo("Hotkey Settings", "[i] Press any key after hitting 'OK' to set the new hotkey.")
        new_hotkey = keyboard.read_event(suppress=False).name
        if new_hotkey:

            keyboard.unhook_all_hotkeys()
            self.start_stop_hotkey = new_hotkey
            self.configure_hotkeys()
            self.start_btn.config(text=f"Start ({self.start_stop_hotkey})")
            self.stop_btn.config(text=f"Stop ({self.start_stop_hotkey})")
            print(f"[✔] New hotkey set: {self.start_stop_hotkey}")

    def configure_hotkeys(self):
        keyboard.add_hotkey(self.start_stop_hotkey, self.toggle_clicker)
        print(f"[✔] Hotkey configured: {self.start_stop_hotkey}")

    def open_github(self):
        webbrowser.open_new("https://github.com/douxxu/Py-autoclicker")
        print("[✔] GitHub page opened.")

if __name__ == "__main__":
    if sys.platform in ["linux", "darwin"] and os.geteuid() != 0:
        messagebox.showerror("Permission Error", "This application must be run as root.")
        sys.exit(1)

    root = tk.Tk()
    app = AutoClickerApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.stop_autoclicker()
        root.destroy()
        print("\n[✘] Application stopped by user.")
        print("Thanks for using Py-autoclicker !")