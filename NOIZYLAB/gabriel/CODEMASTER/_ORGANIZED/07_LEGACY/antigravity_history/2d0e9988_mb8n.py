#!/usr/bin/env python3
# 🎤 LIFELUV ENGR - TACTILE ASSISTANCE SYSTEM
# Version 2.1 (Upgraded with MEMCELL by CB_01)
# 
# Purpose: Complete Hands-Free Control for Music Production & Memory
# Specs: Voice Commands, DAW Integration, Macro Automation, MEMCELL Integration

import time
import sys
import threading
import json
import os
import datetime

# Integrate MEMCELL
from MEMCELL_CORE import MemCellCore

# --- MOCK / IMPORT HANDLING ---
try:
    import speech_recognition as sr
    import pyttsx3
    import pyautogui
    SIMULATION_MODE = False
    print("✅ Hardware Drivers Loaded")
except ImportError:
    SIMULATION_MODE = True
    print("⚠️  Drivers missing. Running in SIMULATION MODE.")

# --- CONFIGURATION ---
CONFIG = {
    "name": "CB_01",
    "trigger_word": "cb",
    "daw": "Logic Pro X",
    "auto_save_interval": 300, # 5 mins
    "voice_speed": 175
}

class TactileSystem:
    def __init__(self):
        self.listening = False
        self.engine = None
        self.recognizer = None
        self.mic = None
        self.brain = MemCellCore()  # Connect to MEMCELL
        
        if not SIMULATION_MODE:
            self.init_hardware()
            
    def init_hardware(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 250) # GOD MODE SPEED (Fast)
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone()
        except:
            print("Audio Hardware Initialization Failed.")
            SIMULATION_MODE = True

    def speak(self, text):
        # GOD MODE: Concise logging, Zero Latency
        print(f"🔥 CB_01: {text}")
        if not SIMULATION_MODE and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def execute_command(self, command):
        cmd = command.lower()
        print(f"🎤 Heard: '{cmd}'")
        
        # --- MEMORY COMMANDS (MEMCELL) ---
        if "remember" in cmd or "save memory" in cmd:
            content = cmd.replace("remember", "").replace("save memory", "").strip()
            if content:
                self.brain.add_memory(content, "Voice Note", "Tactile")
                self.speak("Memory stored in MemCell.")
            else:
                self.speak("What should I remember?")
                
        elif "recall" in cmd or "search memory" in cmd:
             query = cmd.replace("recall", "").replace("search memory", "").strip()
             results = self.brain.search_memories(query)
             if results:
                 self.speak(f"Found {len(results)} memories.")
                 self.speak(f"Most recent: {results[-1]['content']}")
             else:
                 self.speak("No matching memories found.")

        # --- DAW COMMANDS ---
        elif "new project" in cmd:
            self.speak("Creating new project in Logic Pro.")
            if not SIMULATION_MODE: pyautogui.hotkey('cmd', 'n')
            
        elif "arm track" in cmd:
            self.speak("Track armed. Ready to record.")
            if not SIMULATION_MODE: pyautogui.hotkey('r')
            
        elif "play" in cmd or "stop" in cmd:
            if not SIMULATION_MODE: pyautogui.press('space')
            self.speak("Transport toggled.")
            
        elif "save project" in cmd:
            if not SIMULATION_MODE: pyautogui.hotkey('cmd', 's')
            self.speak("Project saved.")
            self.brain.add_memory("Project Saved", "Workflow", "DAW") # Log to memory

        # --- SYSTEM COMMANDS ---
        elif "start session" in cmd:
            self.speak("Opening Creative Suite.")
            self.brain.add_memory("Started Creative Session", "Session", "LifeLuv")
            
        elif "exit" in cmd:
            self.speak("Saving database. Goodnight.")
            self.brain.save_db()
            return False
            
        else:
            self.speak("Command not recognized.")
            
        return True

    def listen_loop(self):
        self.speak(f"Tactile System Online. MEMCELL Active.")
        self.listening = True
        
        if SIMULATION_MODE:
            while self.listening:
                cmd = input(f"\n({CONFIG['trigger_word']}) > ")
                if not self.execute_command(cmd):
                    break
        else:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.listening:
                    try:
                        print("\nListening...")
                        audio = self.recognizer.listen(source)
                        cmd = self.recognizer.recognize_google(audio)
                        if not self.execute_command(cmd):
                            break
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError:
                        self.speak("Network error.")
                        break

if __name__ == "__main__":
    print("\n🎹 TACTILE ASSISTANCE SYSTEM v2.1 (MEMCELL ENABLED) 🎹")
    print("-----------------------------------------------------")
    if len(sys.argv) > 1 and sys.argv[1] == "listen":
        sys = TactileSystem()
        sys.listen_loop()
    else:
        print("Usage: python3 TACTILE_ASSISTANCE_SYSTEM.py listen")
        print("\nNew MEMCELL Commands:")
        print("- 'Remember [idea]'")
        print("- 'Recall [topic]'")
