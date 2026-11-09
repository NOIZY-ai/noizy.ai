#!/usr/bin/env python3
"""
GABRIEL UNIFIED SYSTEM OPTIMIZER X2000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Advanced system optimization and performance tuning
GORUNFREE!! UPGRADE & IMPROVE!!
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class SystemOptimizer:
    """Advanced system optimization engine"""

    def __init__(self):
        self.name = "GABRIEL System Optimizer X2000"
        self.version = "2.0.0-GORUNFREE"
        self.optimizations = []
        self.stats = {
            'before': {},
            'after': {},
            'improvements': []
        }

    def print_banner(self):
        """Display optimizer banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ⚡ GABRIEL SYSTEM OPTIMIZER X2000 ⚡                  ║
║                                                          ║
║     UPGRADE & IMPROVE!! GORUNFREE!!                      ║
║                                                          ║
║     Version: {self.version:^42} ║
║     Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^45} ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banner)

    def analyze_disk_space(self) -> Dict[str, Any]:
        """Analyze disk space usage"""
        print("\n💾 ANALYZING DISK SPACE...")

        try:
            # Get disk usage
            df = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)

            # Get directory sizes
            du = subprocess.run(
                ['du', '-sh', '*'],
                capture_output=True,
                text=True,
                cwd='.'
            )

            analysis = {
                'disk_usage': df.stdout,
                'directory_sizes': du.stdout,
                'timestamp': datetime.now().isoformat()
            }

            print("   ✅ Disk analysis complete")
            return analysis

        except Exception as e:
            print(f"   ⚠️  Error analyzing disk: {e}")
            return {}

    def find_large_files(self, min_size_mb: int = 100) -> List[Dict[str, Any]]:
        """Find large files that might need cleanup"""
        print(f"\n🔍 FINDING FILES LARGER THAN {min_size_mb}MB...")

        try:
            # Find large files
            find_cmd = [
                'find', '.',
                '-type', 'f',
                '-size', f'+{min_size_mb}M',
                '-not', '-path', '*/.*'
            ]

            result = subprocess.run(find_cmd, capture_output=True, text=True)

            large_files = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        size = Path(line).stat().st_size
                        large_files.append({
                            'path': line,
                            'size': size,
                            'size_mb': size / (1024 * 1024)
                        })
                    except:
                        continue

            large_files.sort(key=lambda x: x['size'], reverse=True)

            print(f"   ✅ Found {len(large_files)} large files")
            for f in large_files[:5]:
                print(f"      {f['size_mb']:.1f}MB - {f['path']}")

            return large_files

        except Exception as e:
            print(f"   ⚠️  Error finding large files: {e}")
            return []

    def optimize_git_repos(self) -> Dict[str, Any]:
        """Optimize git repositories"""
        print("\n🔧 OPTIMIZING GIT REPOSITORIES...")

        optimizations = {
            'repos_found': 0,
            'repos_optimized': 0,
            'space_saved': 0
        }

        try:
            # Find all .git directories
            find_git = subprocess.run(
                ['find', '.', '-type', 'd', '-name', '.git'],
                capture_output=True,
                text=True
            )

            git_dirs = [d for d in find_git.stdout.strip().split('\n') if d]
            optimizations['repos_found'] = len(git_dirs)

            for git_dir in git_dirs[:10]:  # Limit to first 10
                repo_path = Path(git_dir).parent
                print(f"   🔧 Optimizing: {repo_path}")

                try:
                    # Git garbage collection
                    subprocess.run(
                        ['git', 'gc', '--auto'],
                        cwd=repo_path,
                        capture_output=True,
                        timeout=30
                    )
                    optimizations['repos_optimized'] += 1

                except Exception as e:
                    print(f"      ⚠️  Failed: {e}")

            print(f"   ✅ Optimized {optimizations['repos_optimized']} repositories")

        except Exception as e:
            print(f"   ⚠️  Error optimizing git repos: {e}")

        return optimizations

    def check_system_updates(self) -> Dict[str, Any]:
        """Check for available system updates"""
        print("\n📦 CHECKING FOR UPDATES...")

        updates = {
            'homebrew': [],
            'python_packages': []
        }

        try:
            # Check Homebrew updates
            if subprocess.run(['which', 'brew'], capture_output=True).returncode == 0:
                print("   🍺 Checking Homebrew...")
                outdated = subprocess.run(
                    ['brew', 'outdated'],
                    capture_output=True,
                    text=True
                )
                updates['homebrew'] = outdated.stdout.strip().split('\n')

            # Check pip updates
            print("   🐍 Checking Python packages...")
            pip_list = subprocess.run(
                ['pip3', 'list', '--outdated'],
                capture_output=True,
                text=True
            )
            updates['python_packages'] = pip_list.stdout.strip().split('\n')

            print(f"   ✅ Found {len(updates['homebrew'])} Homebrew updates")
            print(f"   ✅ Found {len(updates['python_packages'])} Python package updates")

        except Exception as e:
            print(f"   ⚠️  Error checking updates: {e}")

        return updates

    def generate_optimization_report(self) -> str:
        """Generate optimization recommendations"""
        print("\n📊 GENERATING OPTIMIZATION REPORT...")

        report = f"""
╔══════════════════════════════════════════════════════════╗
║           GABRIEL OPTIMIZATION REPORT                    ║
╚══════════════════════════════════════════════════════════╝

⚡ OPTIMIZATION RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Regular Maintenance Tasks:
   1. Run 'git gc' in large repositories
   2. Clear package manager caches
   3. Remove old log files
   4. Archive unused projects

💡 Performance Tips:
   1. Keep system updated
   2. Monitor disk space regularly
   3. Close unused applications
   4. Use SSD for active projects

🚀 Quick Wins:
   1. Empty trash regularly
   2. Clear browser caches
   3. Uninstall unused applications
   4. Disable startup items

╔══════════════════════════════════════════════════════════╗
║        OPTIMIZATION COMPLETE - GORUNFREE!!               ║
╚══════════════════════════════════════════════════════════╝
"""

        return report

    def run_optimization(self):
        """Run complete optimization analysis"""
        self.print_banner()

        # Run analyses
        self.analyze_disk_space()
        self.find_large_files()
        self.optimize_git_repos()
        self.check_system_updates()

        # Generate report
        report = self.generate_optimization_report()
        print(report)

        # Save results
        self.save_results()

    def save_results(self, output_dir: str = "GABRIEL_UNIFIED/reports"):
        """Save optimization results"""
        print("\n💾 SAVING OPTIMIZATION RESULTS...")

        try:
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/optimization_{timestamp}.json"

            with open(filename, 'w') as f:
                json.dump(self.stats, f, indent=2, default=str)

            print(f"   ✅ Results saved to: {filename}")

        except Exception as e:
            print(f"   ⚠️  Error saving results: {e}")


def main():
    """Main execution"""
    optimizer = SystemOptimizer()

    try:
        optimizer.run_optimization()

        print("\n🚀 SYSTEM OPTIMIZER - COMPLETE!")
        print("   GORUNFREE!! UPGRADE & IMPROVE!!\n")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Optimization interrupted by user")
        return 1

    except Exception as e:
        print(f"\n\n❌ Error during optimization: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
