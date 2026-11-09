#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
import random
import math
import os
import struct

# --- THEATRICS & CONFIG ---
Gabriel_Theme = {
    "bg": "#000000",          # Pure Black
    "fg": "#00ff41",          # Matrix Green
    "dim": "#004400",         # Dim Green
    "alert": "#ff0000",       # Red
    "cyan": "#00ffff",        # Cyan data streams
    "font_main": ("Consolas", 11),
    "font_header": ("Arial Black", 20),
    "font_mono": ("Menlo", 9),
    "refresh_rate": 30        # Target 33ms
}

class AudioStreamSimulator:
    """Simulates a 44.1kHz / 16-bit PCM Audio Stream Processing Pipeline."""
    def __init__(self):
        self.sample_rate = 44100
        self.bit_depth = 16
        self.channels = 2
        self.buffer_size = 1024
        self.packet_loss = 0.0001
        self.active = True

    def get_stats(self):
        """Returns simulated stream telemetry."""
        # Fluctuating bitrate around 1411 kbps (CD Quality)
        jitter = random.randint(-5, 5)
        kbps = 1411 + jitter
        
        # Simulated buffer health
        buffer_health = 100 - (random.random() * 2)
        
        return {
            "kbps": f"{kbps} kbps",
            "hz": f"{self.sample_rate} Hz",
            "fmt": f"PCM {self.bit_depth}-bit LE",
            "buf": f"{buffer_health:.2f}%"
        }

class GabrielVoice:
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
                # Force high quality voice if available
                subprocess.run(["say", "-v", "Alex", "-r", "180", text])
            time.sleep(0.1)

class GabrielControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GABRIEL OMEGA :: CORE LINK")
        self.geometry("900x650")
        self.configure(bg=Gabriel_Theme["bg"])
        
        self.stream = AudioStreamSimulator()
        self.voice = GabrielVoice()
        
        self.setup_ui()
        self.voice.speak("Initializing High Fidelity Uplink. 44 point 1 kilohertz locked.")
        
        self.anim_frame = 0
        self.animate_loop()

    def setup_ui(self):
        # Master Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Top HUD
        self.hud_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.hud_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.lbl_title = tk.Label(self.hud_frame, text="GABRIEL :: OMEGA LINK", 
                                  bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["fg"], 
                                  font=Gabriel_Theme["font_header"])
        self.lbl_title.pack(side="left")

        self.lbl_status = tk.Label(self.hud_frame, text="[SECURE]", 
                                   bg=Gabriel_Theme["bg"], fg=Gabriel_Theme["cyan"], 
                                   font=Gabriel_Theme["font_main"])
        self.lbl_status.pack(side="right")

        # 2. Telemetry Strip
        self.telemetry_frame = tk.Frame(self, bg="#0a0a0a", bd=1, relief="flat")
        self.telemetry_frame.grid(row=1, column=0, sticky="ew", padx=10)
        
        self.lbl_stream_info = tk.Label(self.telemetry_frame, 
                                        text="INIT SERIALIZING...",
                                        bg="#0a0a0a", fg=Gabriel_Theme["cyan"],
                                        font=Gabriel_Theme["font_mono"])
        self.lbl_stream_info.pack(fill="x", pady=2)

        # 3. Visualizer (The "Main Event")
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # 4. Data Log
        self.term_text = tk.Text(self, bg="black", fg=Gabriel_Theme["dim"], height=6,
                                 font=Gabriel_Theme["font_mono"], state="disabled",
                                 bd=0)
        self.term_text.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # 5. Command Deck
        self.cmd_frame = tk.Frame(self, bg=Gabriel_Theme["bg"])
        self.cmd_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=20)
        
        # Stylized Buttons
        cmds = [
            ("ESTABLISH LINK", self.run_miracle),
            ("AI NEURAL NET", self.launch_ai),
            ("VOICE CHECK", self.test_voice),
            ("TERMINATE", self.destroy)
        ]
        
        for btn_txt, btn_cmd in cmds:
            btn = tk.Button(self.cmd_frame, text=f"// {btn_txt}", command=btn_cmd,
                            bg="black", fg=Gabriel_Theme["fg"], 
                            activebackground=Gabriel_Theme["fg"], activeforeground="black",
                            font=Gabriel_Theme["font_main"], bd=1, relief="solid")
            btn.pack(side="left", fill="x", expand=True, padx=2)

    def animate_loop(self):
        # Update Telemetry
        stats = self.stream.get_stats()
        self.lbl_stream_info.config(
            text=f"STREAM: {stats['hz']} | {stats['fmt']} | RATE: {stats['kbps']} | BUF: {stats['buf']} | LATENCY: 0.04ms"
        )
        
        # Draw Visualizer
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        mid = h / 2
        
        # 1. Frequency Bars (FFT Simulation)
        bar_w = 10
        for i in range(0, w, bar_w + 2):
            # Perlin-ish noise
            val = (math.sin(i * 0.05 + self.anim_frame * 0.1) + 1) * 0.5
            val += random.random() * 0.2
            bar_h = val * (h * 0.4)
            
            # Color gradient simulation
            color = Gabriel_Theme["dim"]
            if bar_h > h * 0.3: color = Gabriel_Theme["fg"]
            if bar_h > h * 0.38: color = Gabriel_Theme["cyan"]
            
            self.canvas.create_rectangle(i, h, i+bar_w, h-bar_h, fill=color, outline="")

        # 2. Oscilloscope Line (Stereo separation)
        points_l = []
        points_r = []
        for x in range(0, w, 5):
            # Complex wave composition
            y_l = mid + math.sin(x * 0.02 + self.anim_frame * 0.2) * 50 * math.sin(self.anim_frame * 0.05)
            y_r = mid + math.cos(x * 0.025 + self.anim_frame * 0.2) * 50 * math.cos(self.anim_frame * 0.06)
            points_l.extend([x, y_l])
            points_r.extend([x, y_r])
            
        if points_l:
            self.canvas.create_line(points_l, fill=Gabriel_Theme["fg"], width=2)
            self.canvas.create_line(points_r, fill=Gabriel_Theme["cyan"], width=1, dash=(2, 2))

        # 3. Grid Overlay
        if self.anim_frame % 5 == 0:
            pass # save cpu

        self.anim_frame += 1
        self.after(Gabriel_Theme["refresh_rate"], self.animate_loop)

    def log(self, msg):
        self.term_text.configure(state="normal")
        self.term_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.term_text.see("end")
        self.term_text.configure(state="disabled")

    def run_miracle(self):
        self.log("INITIATING MIRACLE SUBROUTINES...")
        self.voice.speak("Miracle Protocol engaged.")
        threading.Thread(target=self._run_cmd, args=(["python3", os.path.expanduser("~/NOIZYLAB/GABRIEL/tools/miracle_setup.py")],)).start()

    def launch_ai(self):
        self.log("ACCESSING NEURAL CLOUD...")
        self.voice.speak("Connecting to Neural Cloud.")
        subprocess.Popen(["open", "https://copilot.microsoft.com"])

    def test_voice(self):
        self.log("VERIFYING AUDIO INTEGRITY...")
        self.voice.speak("Audio integrity one hundred percent. Stream stable.")

    def _run_cmd(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            self.term_text.after(0, self.log, line.strip())

if __name__ == "__main__":
    app = GabrielControl()
    app.mainloop()
