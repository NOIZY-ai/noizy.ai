#!/usr/bin/env python3
# ==============================================================================
# 📊 TURBO TELEMETRY
# ==============================================================================
# "Measure Everything. Optimize Everything."
# Tracks p50/p95 latency for Voice, Cortex, and Tool calls.

import time
import json
import statistics
from pathlib import Path

# CONFIG
LOG_FILE = Path(__file__).parent.parent / "Logs" / "telemetry.json"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

class Telemetry:
    def __init__(self):
        self.events = {}
        self.history = self._load_history()
        
    def _load_history(self):
        try:
            if LOG_FILE.exists():
                with open(LOG_FILE, 'r') as f:
                    return json.load(f)
        except: pass
        return {"voice": [], "cortex": [], "router": [], "tools": []}
        
    def start(self, event_name):
        self.events[event_name] = time.time()
        
    def stop(self, event_name, category="general"):
        if event_name not in self.events: return
        
        duration_ms = (time.time() - self.events[event_name]) * 1000
        print(f"   ⏱️ {event_name}: {duration_ms:.2f}ms")
        
        if category in self.history:
            self.history[category].append(duration_ms)
            # Keep history bounded (last 1000 events)
            if len(self.history[category]) > 1000:
                self.history[category].pop(0)
            self._save()
            
    def _save(self):
        try:
            with open(LOG_FILE, 'w') as f:
                json.dump(self.history, f)
        except: pass
        
    def get_stats(self, category):
        data = self.history.get(category, [])
        if not data: return {"p50": 0, "p95": 0, "count": 0}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        p50 = sorted_data[int(n * 0.5)]
        p95 = sorted_data[int(n * 0.95)]
        
        return {"p50": p50, "p95": p95, "count": n}

    def report(self):
        print("\n📊 LATENCY REPORT (ms)")
        print("-----------------------")
        for cat in self.history:
            stats = self.get_stats(cat)
            print(f"   • {cat.upper()}: p50={stats['p50']:.1f}, p95={stats['p95']:.1f} (n={stats['count']})")
        print("-----------------------\n")

# Global Instance
telemetry = Telemetry()
