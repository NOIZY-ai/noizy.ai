#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import random
import math
import os

# --- THEATRICS & CONFIG ---
Gabriel_Theme = {
    "bg": "#050505",          # Darker Matrix
    "fg": "#00ff41",          # Matrix Green
    "grid": "#003b00",        # Dark Grid
    "accent": "#ff3333",      # Red for critical
    "font_main": ("Courier New", 12),
    "font_header": ("Courier New", 24, "bold"),
    "font_small": ("Menlo", 10),
    "refresh_rate": 33        # ~30 FPS
}

class GabrielVoice:
    """Handles the 'Gabriel Voice' Stream using System TTS."""
    def __init__(self):
        self.queue = []
        self.active = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def speak(self, text):
        self.queue.append(text)

    def _worker(self):
        while self.active:
            if self.queue:
                text = self.queue.pop(0)
                # Use macOS 'say'. 'Alex' is a good breathless/natural voice if available, else default.
                subprocess.run(["say", "-v", "Alex", text])
            time.sleep(0.5)

class GabrielControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GABRIEL :: OMEGA INTERFACE")
        self.geometry("800x600")
        self.configure(bg=Gabriel_Theme["bg"])
        self.resizable(True, True) # Scalable

        self.voice_engine = GabrielVoice()
        
        self.setup_ui()
        self.voice_engine.speak("Gabriel Uplink Established. System Online.")
        
        self.anim_frame = 0
        self.animate_stream() # Start 30FPS loop

    def setup_ui(self):
        # Main Layout: Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Visualizer expands

        # 1. Header Frame
        self.header_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        self.lbl_title = tk.Label(self.header_frame, text="⚡️ GABRIEL OMEGA ⚡️", 
                                  bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["fg"], 
                                  font=Gabriel_Theme["font_header"])
        self.lbl_title.pack(side="top")
        
        self.lbl_stats = tk.Label(self.header_frame, text="STREAM: 44.1kHz / 16-bit PCM | FPS: 30 | LATENCY: 0.2ms",
                                  bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["accent"],
                                  font=Gabriel_Theme["font_small"])
        self.lbl_stats.pack(side="top")

        # 2. Visualizer Canvas (Scalable)
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        
        # 3. Terminal Output
        self.term_text = tk.Text(self, bg="#111", fg="white", height=8,
                                 font=Gabriel_Theme["font_small"], state="disabled", 
                                 bd=1, relief="sunken")
        self.term_text.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        # 4. Controls
        self.btn_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.btn_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=20)
        self.btn_frame.pack_propagate(False)
        
        self.create_btn("RUN MIRACLE", self.run_miracle)
        self.create_btn("AI CORE", self.launch_ai)
        self.create_btn("VOICE TEST", lambda: self.voice_engine.speak("Voice stream nominal."))
        self.create_btn("DISCONNECT", self.destroy, color=Gabriel_Theme["accent"])

    def create_btn(self, text, command, color=None):
        fg_col = color if color else Gabriel_Theme["fg"]
        btn = tk.Button(self.btn_frame, text=f"[{text}]", command=command,
                        bg="#222", fg=fg_col, highlightbackground=Gabriel_Theme["bg"],
                        font=Gabriel_Theme["font_main"], bd=1)
        btn.pack(side="left", padx=10, expand=True, fill="x")

    def animate_stream(self):
        """Draws a 30FPS sine-wave visualization of the 'Audio Stream'."""
        self.canvas.delete("all")
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        mid_h = h / 2
        
        # Draw Mesh/Grid
        for i in range(0, w, 50):
            self.canvas.create_line(i, 0, i, h, fill=Gabriel_Theme["grid"], width=1)
        for i in range(0, h, 50):
            self.canvas.create_line(0, i, w, i, fill=Gabriel_Theme["grid"], width=1)

        # Draw "Voice" Waveform
        points = []
        phase = self.anim_frame * 0.2
        for x in range(0, w, 5):
            # Combined sine waves for "organic" look
            y = mid_h + (math.sin(x * 0.02 + phase) * 50) + \
                        (math.sin(x * 0.05 - phase*2) * 20) + \
                        (random.randint(-5, 5)) # Noise
            points.append(x)
            points.append(y)
        
        if len(points) > 2:
            self.canvas.create_line(points, fill=Gabriel_Theme["fg"], width=2, smooth=True)

        # Beat indicator
        if self.anim_frame % 20 < 10:
             self.canvas.create_oval(w-30, 10, w-10, 30, fill=Gabriel_Theme["accent"], outline="")

        self.anim_frame += 1
        self.after(Gabriel_Theme["refresh_rate"], self.animate_stream)

    def log(self, msg):
        self.term_text.configure(state="normal")
        self.term_text.insert("end", f"> {msg}\n")
        self.term_text.see("end")
        self.term_text.configure(state="disabled")

    def run_miracle(self):
        self.log("Executing Miracle Protocol...")
        self.voice_engine.speak("Miracle Protocol initiated.")
        threading.Thread(target=self._run_cmd, args=(["python3", os.path.expanduser("~/NOIZYLAB/GABRIEL/tools/miracle_setup.py")],)).start()

    def launch_ai(self):
        self.log("Opening AI Neural Interfaces...")
        self.voice_engine.speak("Connecting to Artificial Intelligence Core.")
        subprocess.Popen(["open", "https://copilot.microsoft.com"])

    def _run_cmd(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.term_text.after(0, self.log, line.strip())
        process.wait()
        if process.returncode == 0:
            self.term_text.after(0, self.log, "SUCCESS.")
            self.voice_engine.speak("Task complete.")
        else:
            self.term_text.after(0, self.log, "FAILURE.")
            self.voice_engine.speak("Error detected.")

if __name__ == "__main__":
    app = GabrielControl()
    app.mainloop()
