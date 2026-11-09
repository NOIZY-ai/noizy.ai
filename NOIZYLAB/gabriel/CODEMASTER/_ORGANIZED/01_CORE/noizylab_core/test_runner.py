#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TEST RUNNER v1.0                                          ║
║                    GORUNFREE VERIFICATION                                    ║
║                                                                              ║
║  Run tests, validate code, generate reports. Zero latency testing.          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


@dataclass
class TestResult:
    """Result of a single test"""
    name: str
    passed: bool
    duration_ms: float
    output: str = ""
    error: str = ""


@dataclass
class TestReport:
    """Complete test run report"""
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    duration_ms: float = 0
    results: list[TestResult] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.passed / self.total) * 100
    
    def summary(self) -> str:
        emoji = "✅" if self.failed == 0 else "❌"
        return f"{emoji} {self.passed}/{self.total} passed ({self.success_rate:.1f}%) in {self.duration_ms:.0f}ms"


class TestRunner:
    """
    Universal Test Runner
    
    Run Python, JavaScript, and shell tests.
    Generate reports and integrate with CI.
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def run_python_tests(self, path: Optional[Path] = None) -> TestReport:
        """Run Python tests with pytest"""
        path = path or self.base_path
        start = time.time()
        
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(path), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        duration = (time.time() - start) * 1000
        
        # Parse output
        output = result.stdout + result.stderr
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        
        report = TestReport(
            total=passed + failed,
            passed=passed,
            failed=failed,
            duration_ms=duration,
            results=[TestResult(
                name="pytest",
                passed=(result.returncode == 0),
                duration_ms=duration,
                output=result.stdout,
                error=result.stderr
            )]
        )
        
        return report
    
    def run_python_syntax(self, path: Optional[Path] = None) -> TestReport:
        """Check Python syntax for all files"""
        path = path or self.base_path
        start = time.time()
        
        results = []
        py_files = list(path.rglob("*.py"))
        
        for py_file in py_files:
            if "__pycache__" in str(py_file) or ".venv" in str(py_file):
                continue
            
            file_start = time.time()
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True
            )
            file_duration = (time.time() - file_start) * 1000
            
            results.append(TestResult(
                name=str(py_file.relative_to(path)),
                passed=(result.returncode == 0),
                duration_ms=file_duration,
                error=result.stderr if result.returncode != 0 else ""
            ))
        
        duration = (time.time() - start) * 1000
        passed = sum(1 for r in results if r.passed)
        
        return TestReport(
            total=len(results),
            passed=passed,
            failed=len(results) - passed,
            duration_ms=duration,
            results=results
        )
    
    def run_imports(self, modules: list[str]) -> TestReport:
        """Test that modules can be imported"""
        start = time.time()
        results = []
        
        for module in modules:
            mod_start = time.time()
            try:
                __import__(module)
                results.append(TestResult(
                    name=module,
                    passed=True,
                    duration_ms=(time.time() - mod_start) * 1000
                ))
            except Exception as e:
                results.append(TestResult(
                    name=module,
                    passed=False,
                    duration_ms=(time.time() - mod_start) * 1000,
                    error=str(e)
                ))
        
        duration = (time.time() - start) * 1000
        passed = sum(1 for r in results if r.passed)
        
        return TestReport(
            total=len(results),
            passed=passed,
            failed=len(results) - passed,
            duration_ms=duration,
            results=results
        )
    
    def run_shell(self, script: Path) -> TestResult:
        """Run a shell script test"""
        start = time.time()
        
        result = subprocess.run(
            ["bash", str(script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        duration = (time.time() - start) * 1000
        
        return TestResult(
            name=script.name,
            passed=(result.returncode == 0),
            duration_ms=duration,
            output=result.stdout,
            error=result.stderr
        )
    
    def run_all(self) -> TestReport:
        """Run all tests"""
        start = time.time()
        all_results = []
        
        # Python syntax
        print("🔍 Checking Python syntax...")
        syntax_report = self.run_python_syntax()
        all_results.extend(syntax_report.results)
        print(f"   {syntax_report.summary()}")
        
        # Python imports (NOIZYLAB modules)
        print("📦 Testing imports...")
        modules = [
            "core.agents",
            "core.router",
            "core.generators",
            "core.dreamchamber",
            "core.knowledge_graph",
            "core.memcell",
            "core.slack_bridge",
            "core.turbo_dispatcher",
            "core.async_engine",
            "core.github_webhook",
        ]
        import_report = self.run_imports(modules)
        all_results.extend(import_report.results)
        print(f"   {import_report.summary()}")
        
        duration = (time.time() - start) * 1000
        passed = sum(1 for r in all_results if r.passed)
        
        return TestReport(
            total=len(all_results),
            passed=passed,
            failed=len(all_results) - passed,
            duration_ms=duration,
            results=all_results
        )
    
    def generate_report(self, report: TestReport, output: Optional[Path] = None) -> str:
        """Generate markdown test report"""
        md = f"""# Test Report

**Generated:** {report.timestamp}
**Status:** {"✅ PASSING" if report.failed == 0 else "❌ FAILING"}

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {report.total} |
| Passed | {report.passed} |
| Failed | {report.failed} |
| Success Rate | {report.success_rate:.1f}% |
| Duration | {report.duration_ms:.0f}ms |

## Results

"""
        for result in report.results:
            emoji = "✅" if result.passed else "❌"
            md += f"- {emoji} `{result.name}` ({result.duration_ms:.0f}ms)\n"
            if result.error:
                md += f"  - Error: `{result.error[:100]}`\n"
        
        md += "\n---\n*Generated by TEST RUNNER | GORUNFREE x1000*\n"
        
        if output:
            output.write_text(md)
            print(f"📄 Report saved: {output}")
        
        return md


# Factory
def create_runner(path: Optional[str] = None) -> TestRunner:
    """Create a TestRunner"""
    return TestRunner(Path(path) if path else None)


__all__ = ['TestResult', 'TestReport', 'TestRunner', 'create_runner']


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              TEST RUNNER v1.0                                ║")
    print("║              GORUNFREE VERIFICATION                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    runner = create_runner(".")
    report = runner.run_all()
    
    print()
    print(f"📊 FINAL: {report.summary()}")
