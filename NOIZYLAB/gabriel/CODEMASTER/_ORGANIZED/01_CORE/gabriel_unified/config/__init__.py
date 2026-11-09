"""
GABRIEL Configuration Module
MC96DIGIUNIVERSE AI LIFELUV
"""

import json
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GabrielConfig:
    """Main configuration class for GABRIEL system"""

    # Core settings
    home_dir: Path = field(default_factory=lambda: Path.home() / "GABRIEL_UNIFIED")
    energy_level: str = "∞ INFINITE"
    god_mode: bool = True
    strict_mode: bool = True

    # Voice settings
    voice_name: str = "Oliver"
    voice_rate: int = 175

    # Server settings
    server_port: int = 5174
    server_host: str = "localhost"

    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None

    def __post_init__(self):
        self.log_file = self.home_dir / "logs" / "gabriel.log"

    def to_dict(self) -> dict:
        return {
            "home_dir": str(self.home_dir),
            "energy_level": self.energy_level,
            "god_mode": self.god_mode,
            "strict_mode": self.strict_mode,
            "voice_name": self.voice_name,
            "voice_rate": self.voice_rate,
            "server_port": self.server_port,
            "server_host": self.server_host,
            "log_level": self.log_level,
            "log_file": str(self.log_file) if self.log_file else None
        }

    def save(self, path: Optional[Path] = None) -> None:
        save_path = path or (self.home_dir / "config" / "gabriel.json")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'GabrielConfig':
        with open(path) as f:
            data = json.load(f)
        return cls(
            home_dir=Path(data.get("home_dir", Path.home() / "GABRIEL_UNIFIED")),
            energy_level=data.get("energy_level", "∞ INFINITE"),
            god_mode=data.get("god_mode", True),
            strict_mode=data.get("strict_mode", True),
            voice_name=data.get("voice_name", "Oliver"),
            voice_rate=data.get("voice_rate", 175),
            server_port=data.get("server_port", 5174),
            server_host=data.get("server_host", "localhost"),
            log_level=data.get("log_level", "INFO")
        )


# Default configuration instance
default_config = GabrielConfig()

def get_config() -> GabrielConfig:
    """Get the current configuration"""
    config_path = Path.home() / "GABRIEL_UNIFIED" / "config" / "gabriel.json"
    if config_path.exists():
        return GabrielConfig.load(config_path)
    return default_config
