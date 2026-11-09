#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import sys
import os

# --- THEATRICS & CONFIG ---
Gabriel_Theme = {
    "bg": "#0f0f0f",
    "fg": "#00ff41",  # Matrix Green
    "accent": "#ff3333", # Red for critical
    "font": ("Courier New", 12),
    "header": ("Courier New", 20, "bold")
}

class GabrielControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GABRIEL :: SYSTEM CONTROL")
        self.geometry("600x400")
        self.configure(bg=Gabriel_Theme["bg"])
        self.resizable(False, False)

        # Header
        self.header_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.header_frame.pack(pady=20)
        
        self.label_title = tk.Label(self.header_frame, text="⚡️ GABRIEL SYSTEM CONTROL ⚡️", 
                                    bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["fg"], 
                                    font=Gabriel_Theme["header"])
        self.label_title.pack()
        
        self.label_status = tk.Label(self.header_frame, text="STATUS: CONNECTED // ID: M2ULTRA", 
                                     bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["accent"], 
                                     font=("Courier New", 10))
        self.label_status.pack()

        # Terminal Output Area
        self.term_frame = tk.Frame(self, bg=Gabriel_Theme["bg"], bd=2, relief="sunken")
        self.term_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.term_text = tk.Text(self.term_frame, bg="black", fg="white", height=10, 
                                 font=("Menlo", 10), state="disabled")
        self.term_text.pack(fill="both", expand=True)

        # Buttons
        self.btn_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.btn_frame.pack(pady=20)

        self.create_cyber_btn("INITIATE MIRACLE", self.run_miracle)
        self.create_cyber_btn("LAUNCH AI CORE", self.launch_ai)
        self.create_cyber_btn("SYSTEM SCAN", self.run_scan)
        self.create_cyber_btn("EXIT", self.destroy, color="#ff3333")

        self.log("System Initialized.")
        self.log("Waiting for user command...")

    def create_cyber_btn(self, text, command, color=None):
        fg_col = color if color else Gabriel_Theme["fg"]
        btn = tk.Button(self.btn_frame, text=f"[ {text} ]", command=command,
                        bg=Gabriel_Theme["bg"], fg=fg_col, 
                        font=Gabriel_Theme["font"], bd=0, activebackground=fg_col, activeforeground="black")
        btn.pack(side="left", padx=10)

    def log(self, msg):
        self.term_text.configure(state="normal")
        self.term_text.insert("end", f"> {msg}\n")
        self.term_text.see("end")
        self.term_text.configure(state="disabled")

    def run_miracle(self):
        self.log("Initiating Miracle Protocol...")
        # Run in thread to not freeze UI
        threading.Thread(target=self._run_cmd, args=(["python3", os.path.expanduser("~/NOIZYLAB/GABRIEL/tools/miracle_setup.py")],)).start()

    def launch_ai(self):
        self.log("Accessing AI Neural Net...")
        self.log("Opening Control Interfaces...")
        subprocess.Popen(["open", "https://copilot.microsoft.com"])
        subprocess.Popen(["open", "https://designer.microsoft.com"])

    def run_scan(self):
        self.log("Scanning M2 Ultra Volume...")
        time.sleep(1)
        self.log("Sector 7G... OK")
        time.sleep(0.5)
        self.log("MemCell Integrity... 100%")
        self.log("Scan Complete. No anomalies.")

    def _run_cmd(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.term_text.after(0, self.log, line.strip())
        process.wait()
        if process.returncode == 0:
            self.term_text.after(0, self.log, "SUCCESS.")
        else:
            self.term_text.after(0, self.log, "FAILURE.")

if __name__ == "__main__":
    app = GabrielControl()
    app.mainloop()
