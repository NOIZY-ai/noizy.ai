"""
GABRIEL Scripts Module
MC96DIGIUNIVERSE AI LIFELUV

Automation and task execution scripts.
"""

from pathlib import Path
import subprocess
from typing import List, Optional, Callable
from dataclasses import dataclass


@dataclass
class ScriptResult:
    """Result of a script execution"""
    success: bool
    output: str
    exit_code: int
    script_name: str


class ScriptRunner:
    """Execute and manage Gabriel scripts"""

    def __init__(self, scripts_dir: Optional[Path] = None):
        self.scripts_dir = scripts_dir or (Path.home() / "GABRIEL_UNIFIED" / "scripts")
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def run(self, script_name: str, args: List[str] = None, timeout: int = 60) -> ScriptResult:
        """Run a script by name"""
        script_path = self.scripts_dir / script_name

        if not script_path.exists():
            return ScriptResult(
                success=False,
                output=f"Script not found: {script_name}",
                exit_code=-1,
                script_name=script_name
            )

        try:
            cmd = [str(script_path)] + (args or [])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return ScriptResult(
                success=result.returncode == 0,
                output=result.stdout + result.stderr,
                exit_code=result.returncode,
                script_name=script_name
            )
        except subprocess.TimeoutExpired:
            return ScriptResult(
                success=False,
                output="Script timed out",
                exit_code=-2,
                script_name=script_name
            )
        except Exception as e:
            return ScriptResult(
                success=False,
                output=str(e),
                exit_code=-3,
                script_name=script_name
            )

    def list_scripts(self) -> List[str]:
        """List available scripts"""
        scripts = []
        for ext in ['*.sh', '*.py', '*.swift']:
            scripts.extend([p.name for p in self.scripts_dir.glob(ext)])
        return sorted(scripts)

    def create_script(self, name: str, content: str, executable: bool = True) -> Path:
        """Create a new script"""
        script_path = self.scripts_dir / name
        script_path.write_text(content)
        if executable:
            script_path.chmod(0o755)
        return script_path


# Default runner
runner = ScriptRunner()
