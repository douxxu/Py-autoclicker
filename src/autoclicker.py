import time
import threading
import pyautogui

class AutoClicker:
    def __init__(self):
        self.running = False
        self.thread = None

    def start_clicking(self, interval, button, click_type="single", repeat=None, position=None):
        self.running = True
        self.thread = threading.Thread(target=self._clicker, args=(interval, button, click_type, repeat, position))
        self.thread.start()
        print("[✔] AutoClicker started.")

    def _clicker(self, interval, button, click_type, repeat, position):
        pyautogui.FAILSAFE = False
        click_count = 0
        while self.running:
            if position:
                pyautogui.moveTo(position)
            if click_type == "double":
                pyautogui.doubleClick(button=button)
                print(f"[i] Double-clicked with {button} button.")
            else:
                pyautogui.click(button=button)
                print(f"[i] Single-clicked with {button} button.")
            click_count += 1
            if repeat and click_count >= repeat:
                break
            time.sleep(interval / 1000.0)
        self.running = False
        print("[✔] AutoClicker stopped.")

    def stop_clicking(self):
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None
            print("[✔] AutoClicker thread joined.")
