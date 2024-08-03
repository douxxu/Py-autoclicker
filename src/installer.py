import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
import platform
import subprocess
import sys

class AutoClickerInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Py-AutoClicker Installer")

        self.icon_path = os.path.join(os.path.dirname(__file__), "images", "py-autoclicker.png")

        self.label = tk.Label(self.root, text="Click Install to install Py-AutoClicker")
        self.label.pack(pady=20)

        self.install_btn = tk.Button(self.root, text="Install", command=self.install)
        self.install_btn.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def install(self):

        if platform.system() == "Linux" and os.geteuid() != 0:
            messagebox.showerror("Permission Error", "This installer must be run with root privileges (sudo).")
            return

        install_dir = filedialog.askdirectory(title="Choose Installation Directory")
        if not install_dir:
            return

        install_dir = os.path.join(install_dir, "py-autoclicker")
        os.makedirs(install_dir, exist_ok=True)

        current_dir = os.path.dirname(__file__)
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isfile(item_path) and item != os.path.basename(__file__):
                shutil.copy(item_path, install_dir)
            elif os.path.isdir(item_path) and item != "__pycache__":
                shutil.copytree(item_path, os.path.join(install_dir, item))

        icon_dest = os.path.join(install_dir, "py-autoclicker.png")
        shutil.copy(self.icon_path, icon_dest)

        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "-r", os.path.join(install_dir, "requirements.txt")])
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Installation Error", f"Failed to install Python packages: {e}")
            return

        if platform.system() == "Windows":
            script_name = "Py-autoclicker.bat"
            script_content = f'@echo off\npython "{os.path.join(install_dir, "Py-autoclicker.py")}"'
            script_path = os.path.join(install_dir, script_name)
            with open(script_path, "w") as f:
                f.write(script_content)
        else:
            script_name = "Py-autoclicker.sh"
            script_content = f'#!/bin/bash\nsudo python3 "{os.path.join(install_dir, "Py-autoclicker.py")}"'
            script_path = os.path.join(install_dir, script_name)
            with open(script_path, "w") as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)

        if platform.system() == "Linux":
            desktop_file_content = f"""[Desktop Entry]
Name=Py-AutoClicker
Exec={script_path}
Icon={icon_dest}
Terminal=false
Type=Application
Categories=Utility;
"""
            desktop_path = "/usr/share/applications/py-autoclicker.desktop"

            desktop_dir = os.path.dirname(desktop_path)

            if not os.path.exists(desktop_dir):
                try:
                    os.makedirs(desktop_dir)
                except OSError as e:
                    print(f"Error creating directory {desktop_dir}: {e}")
                    raise

            try:
                with open(desktop_path, "w") as f:
                    f.write(desktop_file_content)
                print(f"Desktop file created at {desktop_path}")
            except IOError as e:
                print(f"Error writing desktop file {desktop_path}: {e}")
                raise

        if platform.system() == "Windows":
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "Py-AutoClicker.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = script_path
            shortcut.IconLocation = icon_dest
            shortcut.save()

        messagebox.showinfo("Installation Successful", "Py-AutoClicker has been installed successfully.")
        self.root.destroy()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit installation?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerInstaller(root)
    root.mainloop()
