#!/usr/bin/env python3
"""
GIT ACTIVITY MONITOR - Real-time repo intelligence
Shows what you've actually been working on
"""
import os
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict
import json

class GitMonitor:
    def __init__(self, repo_paths):
        self.repos = repo_paths if isinstance(repo_paths, list) else [repo_paths]

    def run_git(self, repo, cmd):
        """Run git command in repo"""
        try:
            result = subprocess.run(
                ['git'] + cmd,
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None

    def get_recent_commits(self, repo, days=7):
        """Get commits from last N days"""
        since = datetime.now() - timedelta(days=days)
        since_str = since.strftime('%Y-%m-%d')

        # Get commit log
        log = self.run_git(repo, [
            'log',
            f'--since={since_str}',
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=iso'
        ])

        if not log:
            return []

        commits = []
        for line in log.split('\n'):
            if not line:
                continue
            parts = line.split('|', 4)
            if len(parts) == 5:
                commits.append({
                    'hash': parts[0][:8],
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3],
                    'message': parts[4]
                })

        return commits

    def get_file_changes(self, repo, commit_hash):
        """Get files changed in commit"""
        stats = self.run_git(repo, [
            'show',
            '--stat',
            '--format=',
            commit_hash
        ])

        if not stats:
            return []

        files = []
        for line in stats.split('\n'):
            if '|' in line:
                file = line.split('|')[0].strip()
                if file:
                    files.append(file)

        return files

    def get_current_branch(self, repo):
        """Get current branch"""
        return self.run_git(repo, ['branch', '--show-current'])

    def get_uncommitted_changes(self, repo):
        """Get uncommitted changes"""
        status = self.run_git(repo, ['status', '--porcelain'])
        if not status:
            return []

        changes = []
        for line in status.split('\n'):
            if len(line) > 3:
                status_code = line[:2].strip()
                file = line[3:].strip()
                changes.append({
                    'status': status_code,
                    'file': file
                })

        return changes

    def analyze_activity(self, days=7):
        """Full activity analysis"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'repos': [],
            'summary': {
                'total_commits': 0,
                'total_files_changed': 0,
                'total_uncommitted': 0,
                'active_repos': 0
            }
        }

        for repo in self.repos:
            if not os.path.exists(os.path.join(repo, '.git')):
                continue

            print(f"📊 Analyzing {os.path.basename(repo)}...")

            commits = self.get_recent_commits(repo, days)
            uncommitted = self.get_uncommitted_changes(repo)
            branch = self.get_current_branch(repo)

            # File frequency analysis
            file_freq = defaultdict(int)
            for commit in commits:
                files = self.get_file_changes(repo, commit['hash'])
                for f in files:
                    file_freq[f] += 1

            # Sort by frequency
            hot_files = sorted(file_freq.items(), key=lambda x: x[1], reverse=True)[:10]

            repo_data = {
                'path': repo,
                'name': os.path.basename(repo),
                'branch': branch,
                'commits': commits,
                'uncommitted': uncommitted,
                'hot_files': [{'file': f, 'changes': c} for f, c in hot_files],
                'stats': {
                    'commits': len(commits),
                    'uncommitted_files': len(uncommitted),
                    'unique_files_touched': len(file_freq)
                }
            }

            report['repos'].append(repo_data)

            # Update summary
            if commits or uncommitted:
                report['summary']['active_repos'] += 1
            report['summary']['total_commits'] += len(commits)
            report['summary']['total_uncommitted'] += len(uncommitted)
            report['summary']['total_files_changed'] += len(file_freq)

        return report

    def print_report(self, report):
        """Print human-readable report"""
        print("\n" + "="*70)
        print(f"  GIT ACTIVITY REPORT - Last 7 Days")
        print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")

        # Summary
        s = report['summary']
        print(f"📊 SUMMARY:")
        print(f"   Active Repos: {s['active_repos']}")
        print(f"   Total Commits: {s['total_commits']}")
        print(f"   Files Changed: {s['total_files_changed']}")
        print(f"   Uncommitted Files: {s['total_uncommitted']}")
        print()

        # Per-repo details
        for repo in report['repos']:
            if not repo['commits'] and not repo['uncommitted']:
                continue

            print(f"📁 {repo['name']}")
            print(f"   Branch: {repo['branch']}")
            print(f"   Path: {repo['path']}")
            print()

            # Recent commits
            if repo['commits']:
                print(f"   📝 RECENT COMMITS ({len(repo['commits'])}):")
                for commit in repo['commits'][:5]:
                    date = commit['date'][:10]
                    print(f"      {commit['hash']} {date} - {commit['message'][:60]}")
                if len(repo['commits']) > 5:
                    print(f"      ... and {len(repo['commits']) - 5} more")
                print()

            # Hot files
            if repo['hot_files']:
                print(f"   🔥 HOT FILES (Most Changed):")
                for item in repo['hot_files'][:5]:
                    print(f"      {item['changes']:3}× {item['file']}")
                print()

            # Uncommitted
            if repo['uncommitted']:
                print(f"   ⚠️  UNCOMMITTED CHANGES ({len(repo['uncommitted'])}):")
                for change in repo['uncommitted'][:10]:
                    status_map = {
                        'M': 'Modified',
                        'A': 'Added',
                        'D': 'Deleted',
                        '??': 'Untracked'
                    }
                    status = status_map.get(change['status'], change['status'])
                    print(f"      [{status:9}] {change['file']}")
                if len(repo['uncommitted']) > 10:
                    print(f"      ... and {len(repo['uncommitted']) - 10} more")
                print()

        print("="*70)
        print("✅ ANALYSIS COMPLETE")
        print("="*70 + "\n")

if __name__ == '__main__':
    import sys

    # Auto-detect git repos in common locations
    search_paths = [
        '/Users/m2ultra/NOIZYLAB',
        '/Users/m2ultra/noizylab'
    ]

    repos = []
    for search in search_paths:
        if os.path.exists(search):
            for item in os.listdir(search):
                item_path = os.path.join(search, item)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, '.git')):
                    repos.append(item_path)

    if not repos:
        print("❌ No git repositories found")
        sys.exit(1)

    print(f"🔍 Found {len(repos)} git repositories\n")

    monitor = GitMonitor(repos)
    report = monitor.analyze_activity(days=7)
    monitor.print_report(report)

    # Save JSON
    output_file = 'git_activity_report.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"📄 Full report saved: {output_file}")
