"""
GABRIEL TOOLS MODULE
- Desktop Control (pyautogui)
- Network Control (netmiko/D-Link)
"""

import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("GABRIEL_TOOLS")

# --- DESKTOP CONTROL ---

class ComputerTool:
    def __init__(self):
        try:
            import pyautogui
            # FAILSAFE: Slam mouse to corner to kill
            pyautogui.FAILSAFE = True 
            self.pg = pyautogui
            self.width, self.height = pyautogui.size()
            self._available = True
            logger.info(f"🖥️  DESKTOP CONTROL ACTIVE ({self.width}x{self.height})")
        except ImportError:
            self._available = False
            logger.warning("🖥️  DESKTOP CONTROL UNAVAILABLE (pyautogui missing)")

    def execute(self, action: str, params: Dict[str, Any] = {}) -> str:
        if not self._available:
            return "Error: Computer tool unavailable"
            
        try:
            if action == "mouse_move":
                x = params.get("x")
                y = params.get("y")
                self.pg.moveTo(x, y, duration=0.2)
                return f"Moved to {x}, {y}"
                
            elif action == "mouse_click":
                x = params.get("x")
                y = params.get("y")
                if x and y:
                    self.pg.click(x, y)
                else:
                    self.pg.click()
                return "Clicked"
                
            elif action == "type":
                text = params.get("text", "")
                self.pg.write(text, interval=0.01)
                return f"Typed: {text}"
                
            elif action == "press":
                key = params.get("key", "")
                self.pg.press(key)
                return f"Pressed: {key}"
                
            elif action == "scroll":
                amount = params.get("amount", 0)
                self.pg.scroll(amount)
                return f"Scrolled {amount}"
            
            elif action == "screenshot":
                path = "screenshot.png"
                self.pg.screenshot(path)
                return f"Screenshot saved to {path}"
                
            return f"Unknown action: {action}"
            
        except Exception as e:
            logger.error(f"Desktop Error: {e}")
            return f"Error: {e}"

# --- NETWORK CONTROL ---

class NetworkTool:
    def __init__(self):
        self._available = False
        try:
            import netmiko
            self._available = True
            logger.info("🔌 NETWORK CONTROL ENABLED")
        except ImportError:
            logger.warning("🔌 NETWORK CONTROL UNAVAILABLE (netmiko missing)")
            
    def execute_command(self, ip: str, command: str, device_type: str = "dlink_ds", username: str = "admin") -> str:
        if not self._available:
            return "Error: Network tool unavailable"
            
        from netmiko import ConnectHandler
        
        # In a real scenario, use SSH keys or secure vault
        password = os.environ.get("SWITCH_PASSWORD", "admin") 
        
        device = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }
        
        try:
            logger.info(f"Connecting to {ip}...")
            with ConnectHandler(**device) as net_connect:
                output = net_connect.send_command(command)
                return output
        except Exception as e:
            logger.error(f"Network Error: {e}")
            return f"Network Error: {e}"
