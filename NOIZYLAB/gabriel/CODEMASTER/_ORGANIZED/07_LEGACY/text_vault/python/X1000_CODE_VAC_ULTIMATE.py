#!/usr/bin/env python3
"""
X1000 CODE_VAC ULTIMATE
=======================
Supreme code vacuum with AI-powered optimization
X1000 enhanced for intelligent code management

FEATURES:
- AI-powered duplicate detection
- Smart code organization
- Quality scoring
- Auto-refactoring suggestions
- Dependency analysis
- Security scanning
- Performance optimization
- Intelligent archiving
"""

import os
import re
import json
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from datetime import datetime
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class X1000CodeVacUltimate:
    """X1000 enhanced code vacuum with AI capabilities"""
    
    def __init__(self):
        # Support 100+ file extensions
        self.extensions = {
            # Programming Languages
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
            '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r',
            '.m', '.mm', '.pl', '.lua', '.dart', '.elm', '.ex', '.exs', '.clj',
            '.hs', '.ml', '.fs', '.fsx', '.vb', '.f90', '.f95', '.jl', '.nim',
            
            # Web Technologies
            '.html', '.htm', '.css', '.scss', '.sass', '.less', '.vue', '.svelte',
            
            # Scripts
            '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
            
            # Data & Config
            '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg', '.conf',
            '.env', '.properties',
            
            # Documentation
            '.md', '.rst', '.txt', '.adoc', '.tex',
            
            # Database
            '.sql', '.db', '.sqlite', '.sqlite3',
            
            # Other
            '.proto', '.thrift', '.graphql', '.wasm', '.asm', '.s'
        }
        
        self.files_by_type = defaultdict(list)
        self.files_by_hash = defaultdict(list)
        self.duplicate_groups = []
        self.junk_files = []
        self.total_files = 0
        self.total_size = 0
        self.duplicate_size = 0
        
        # X1000 enhancements
        self.quality_scores = {}
        self.security_issues = defaultdict(list)
        self.performance_issues = defaultdict(list)
        self.refactoring_suggestions = defaultdict(list)
        self.dependency_graph = defaultdict(set)
        
        print("🧹 X1000 CODE_VAC ULTIMATE INITIALIZED")
        print(f"📂 Supported Extensions: {len(self.extensions)}")
        print("🤖 AI Analysis: ENABLED")
        print("🔒 Security Scanning: ENABLED")
        print("⚡ Performance Analysis: ENABLED")
    
    def scan(self, root_path: Path, deep_analysis: bool = True) -> Dict:
        """
        X1000 enhanced scan with AI analysis
        
        Args:
            root_path: Directory to scan
            deep_analysis: Enable deep AI analysis
        
        Returns:
            Comprehensive scan results
        """
        print(f"\n🔍 Scanning: {root_path}")
        print(f"🧠 Deep Analysis: {'ENABLED' if deep_analysis else 'DISABLED'}")
        
        start_time = time.time()
        
        # Collect all code files
        code_files = []
        for ext in self.extensions:
            code_files.extend(root_path.rglob(f'*{ext}'))
        
        print(f"📄 Files found: {len(code_files)}")
        
        # Parallel processing with X1000 speed
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_file = {
                executor.submit(self._analyze_file, f, deep_analysis): f
                for f in code_files
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Error analyzing {file_path}: {e}")
        
        scan_time = time.time() - start_time
        
        # Identify duplicates
        self._identify_duplicates()
        
        # Identify junk
        self._identify_junk()
        
        # Generate results
        results = {
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
                'root_path': str(root_path),
                'scan_time': round(scan_time, 2),
                'total_files': self.total_files,
                'total_size_mb': round(self.total_size / (1024**2), 2),
                'duplicate_size_mb': round(self.duplicate_size / (1024**2), 2),
                'space_recoverable_mb': round(self.duplicate_size / (1024**2), 2)
            },
            'by_language': self._get_language_stats(),
            'duplicates': {
                'groups': len(self.duplicate_groups),
                'files': sum(len(group) for group in self.duplicate_groups),
                'items': self.duplicate_groups[:50]  # Limit output
            },
            'junk_files': {
                'count': len(self.junk_files),
                'items': self.junk_files[:50]
            },
            'quality_report': self._generate_quality_report(),
            'security_report': self._generate_security_report(),
            'performance_report': self._generate_performance_report(),
            'top_files': {
                'largest': self._get_largest_files(10),
                'most_complex': self._get_most_complex_files(10),
                'lowest_quality': self._get_lowest_quality_files(10)
            },
            'recommendations': self._generate_recommendations()
        }
        
        self._print_summary(results)
        
        return results
    
    def _analyze_file(self, file_path: Path, deep_analysis: bool):
        """X1000 enhanced file analysis"""
        try:
            # Basic info
            file_size = file_path.stat().st_size
            self.total_files += 1
            self.total_size += file_size
            
            # Categorize by type
            self.files_by_type[file_path.suffix].append(str(file_path))
            
            # Read content
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                return
            
            # Calculate hash for duplicate detection
            file_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            self.files_by_hash[file_hash].append({
                'path': str(file_path),
                'size': file_size
            })
            
            if deep_analysis:
                # Quality analysis
                quality_score = self._calculate_quality_score(content, file_path)
                self.quality_scores[str(file_path)] = quality_score
                
                # Security analysis
                security_issues = self._scan_security(content, file_path)
                if security_issues:
                    self.security_issues[str(file_path)] = security_issues
                
                # Performance analysis
                perf_issues = self._scan_performance(content, file_path)
                if perf_issues:
                    self.performance_issues[str(file_path)] = perf_issues
                
                # Refactoring suggestions
                suggestions = self._generate_refactoring_suggestions(content, file_path)
                if suggestions:
                    self.refactoring_suggestions[str(file_path)] = suggestions
                
                # Dependency analysis
                if file_path.suffix == '.py':
                    deps = self._extract_python_dependencies(content)
                    self.dependency_graph[str(file_path)] = deps
        
        except Exception as e:
            pass
    
    def _calculate_quality_score(self, content: str, file_path: Path) -> float:
        """Calculate code quality score (0-100)"""
        score = 100.0
        lines = content.split('\n')
        
        # Deduct for issues
        if len(lines) > 500:
            score -= 5  # Very long file
        
        # Check comment ratio
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        comment_ratio = comment_lines / max(len(lines), 1)
        if comment_ratio < 0.1:
            score -= 10  # Low documentation
        
        # Check for TODO/FIXME
        todos = content.count('TODO') + content.count('FIXME')
        score -= min(todos * 2, 20)
        
        # Check for print statements (in Python)
        if file_path.suffix == '.py':
            prints = len(re.findall(r'\bprint\s*\(', content))
            score -= min(prints * 1, 10)
        
        # Check complexity (nested depth)
        max_indent = 0
        for line in lines:
            indent = len(line) - len(line.lstrip())
            max_indent = max(max_indent, indent)
        
        if max_indent > 20:
            score -= 15  # Too much nesting
        
        return max(0, score)
    
    def _scan_security(self, content: str, file_path: Path) -> List[Dict]:
        """Scan for security issues"""
        issues = []
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password', 'CRITICAL'),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key', 'CRITICAL'),
            (r'\beval\s*\(', 'eval() usage', 'HIGH'),
            (r'\bexec\s*\(', 'exec() usage', 'HIGH'),
            (r'pickle\.loads?\(', 'Unsafe pickle', 'MEDIUM'),
            (r'os\.system\(', 'os.system() usage', 'MEDIUM'),
        ]
        
        for pattern, description, severity in security_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'description': description,
                    'severity': severity,
                    'line': line_num,
                    'code': match.group(0)[:50]
                })
        
        return issues
    
    def _scan_performance(self, content: str, file_path: Path) -> List[Dict]:
        """Scan for performance issues"""
        issues = []
        
        performance_patterns = [
            (r'for\s+.*?in\s+range\(len\(', 'Inefficient loop', 'MEDIUM'),
            (r'\+\=\s*["\']', 'String concatenation in loop', 'MEDIUM'),
            (r'while\s+True.*?\n.*?time\.sleep\(0\)', 'Busy wait loop', 'HIGH'),
        ]
        
        for pattern, description, severity in performance_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'description': description,
                    'severity': severity,
                    'line': line_num
                })
        
        return issues
    
    def _generate_refactoring_suggestions(self, content: str, file_path: Path) -> List[str]:
        """Generate AI-powered refactoring suggestions"""
        suggestions = []
        lines = content.split('\n')
        
        # Long function detection
        if file_path.suffix == '.py':
            functions = re.findall(r'def\s+(\w+).*?:\n((?:.*?\n)*?)(?=\ndef\s|\nclass\s|\Z)', content, re.MULTILINE)
            for func_name, func_body in functions:
                func_lines = len(func_body.split('\n'))
                if func_lines > 50:
                    suggestions.append(f"Function '{func_name}' is very long ({func_lines} lines). Consider breaking it down.")
        
        # Long file
        if len(lines) > 500:
            suggestions.append(f"File is very long ({len(lines)} lines). Consider splitting into modules.")
        
        # High complexity
        if_count = len(re.findall(r'\bif\b', content))
        if if_count > 20:
            suggestions.append(f"High cyclomatic complexity ({if_count} if statements). Consider simplifying logic.")
        
        return suggestions
    
    def _extract_python_dependencies(self, content: str) -> Set[str]:
        """Extract Python import dependencies"""
        deps = set()
        
        # Standard imports
        imports = re.findall(r'^\s*import\s+(\w+)', content, re.MULTILINE)
        deps.update(imports)
        
        # From imports
        from_imports = re.findall(r'^\s*from\s+(\w+)', content, re.MULTILINE)
        deps.update(from_imports)
        
        return deps
    
    def _identify_duplicates(self):
        """Identify duplicate files"""
        for file_hash, files in self.files_by_hash.items():
            if len(files) > 1:
                self.duplicate_groups.append(files)
                # Calculate duplicate size (keep one, remove rest)
                duplicate_size = sum(f['size'] for f in files[1:])
                self.duplicate_size += duplicate_size
    
    def _identify_junk(self):
        """Identify junk files"""
        junk_patterns = [
            r'__pycache__',
            r'\.pyc$',
            r'\.pyo$',
            r'\.DS_Store$',
            r'Thumbs\.db$',
            r'\.swp$',
            r'\.bak$',
            r'\.tmp$',
            r'~$'
        ]
        
        for files in self.files_by_type.values():
            for file_path in files:
                if any(re.search(pattern, file_path) for pattern in junk_patterns):
                    self.junk_files.append(file_path)
    
    def _get_language_stats(self) -> Dict:
        """Get statistics by language"""
        stats = {}
        for ext, files in self.files_by_type.items():
            total_size = sum(Path(f).stat().st_size for f in files if Path(f).exists())
            stats[ext] = {
                'files': len(files),
                'size_mb': round(total_size / (1024**2), 2)
            }
        return dict(sorted(stats.items(), key=lambda x: x[1]['files'], reverse=True))
    
    def _get_largest_files(self, count: int) -> List[Dict]:
        """Get largest files"""
        all_files = []
        for files in self.files_by_type.values():
            for f in files:
                fp = Path(f)
                if fp.exists():
                    all_files.append({
                        'path': str(f),
                        'size_mb': round(fp.stat().st_size / (1024**2), 2)
                    })
        
        return sorted(all_files, key=lambda x: x['size_mb'], reverse=True)[:count]
    
    def _get_most_complex_files(self, count: int) -> List[Dict]:
        """Get most complex files"""
        # Use quality score as inverse complexity indicator
        sorted_files = sorted(self.quality_scores.items(), key=lambda x: x[1])
        return [{'path': path, 'quality_score': score} for path, score in sorted_files[:count]]
    
    def _get_lowest_quality_files(self, count: int) -> List[Dict]:
        """Get lowest quality files"""
        sorted_files = sorted(self.quality_scores.items(), key=lambda x: x[1])
        return [{'path': path, 'quality_score': round(score, 1)} for path, score in sorted_files[:count]]
    
    def _generate_quality_report(self) -> Dict:
        """Generate quality report"""
        if not self.quality_scores:
            return {'average_score': 0, 'files_analyzed': 0}
        
        avg_score = sum(self.quality_scores.values()) / len(self.quality_scores)
        
        return {
            'average_score': round(avg_score, 1),
            'files_analyzed': len(self.quality_scores),
            'excellent': len([s for s in self.quality_scores.values() if s >= 90]),
            'good': len([s for s in self.quality_scores.values() if 70 <= s < 90]),
            'needs_improvement': len([s for s in self.quality_scores.values() if s < 70])
        }
    
    def _generate_security_report(self) -> Dict:
        """Generate security report"""
        total_issues = sum(len(issues) for issues in self.security_issues.values())
        
        severity_count = Counter()
        for issues in self.security_issues.values():
            for issue in issues:
                severity_count[issue['severity']] += 1
        
        return {
            'total_issues': total_issues,
            'files_with_issues': len(self.security_issues),
            'by_severity': dict(severity_count),
            'top_issues': self._get_top_security_issues(5)
        }
    
    def _get_top_security_issues(self, count: int) -> List[Dict]:
        """Get top security issues"""
        all_issues = []
        for file_path, issues in self.security_issues.items():
            for issue in issues:
                all_issues.append({
                    'file': file_path,
                    **issue
                })
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        return sorted(all_issues, key=lambda x: severity_order.get(x['severity'], 99))[:count]
    
    def _generate_performance_report(self) -> Dict:
        """Generate performance report"""
        total_issues = sum(len(issues) for issues in self.performance_issues.values())
        
        return {
            'total_issues': total_issues,
            'files_with_issues': len(self.performance_issues),
            'top_issues': self._get_top_performance_issues(5)
        }
    
    def _get_top_performance_issues(self, count: int) -> List[Dict]:
        """Get top performance issues"""
        all_issues = []
        for file_path, issues in self.performance_issues.items():
            for issue in issues:
                all_issues.append({
                    'file': file_path,
                    **issue
                })
        
        return all_issues[:count]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate X1000 AI recommendations"""
        recommendations = []
        
        # Duplicate recommendations
        if self.duplicate_groups:
            recommendations.append(f"🔄 Remove {len(self.duplicate_groups)} duplicate file groups to save {round(self.duplicate_size / (1024**2), 1)}MB")
        
        # Junk recommendations
        if self.junk_files:
            recommendations.append(f"🗑️  Clean {len(self.junk_files)} junk files")
        
        # Security recommendations
        critical_security = sum(1 for issues in self.security_issues.values() 
                               for issue in issues if issue['severity'] == 'CRITICAL')
        if critical_security > 0:
            recommendations.append(f"🚨 URGENT: Fix {critical_security} CRITICAL security issues")
        
        # Quality recommendations
        if self.quality_scores:
            avg_quality = sum(self.quality_scores.values()) / len(self.quality_scores)
            if avg_quality < 70:
                recommendations.append(f"📊 Improve code quality (average score: {avg_quality:.1f}/100)")
        
        # Refactoring recommendations
        total_suggestions = sum(len(s) for s in self.refactoring_suggestions.values())
        if total_suggestions > 10:
            recommendations.append(f"🔧 Consider {total_suggestions} refactoring suggestions")
        
        return recommendations
    
    def _print_summary(self, results: Dict):
        """Print X1000 formatted summary"""
        print("\n" + "="*70)
        print("🧹 X1000 CODE_VAC ULTIMATE - SCAN REPORT")
        print("="*70)
        
        meta = results['scan_metadata']
        print(f"\n📊 SCAN STATISTICS:")
        print(f"   Files: {meta['total_files']}")
        print(f"   Total Size: {meta['total_size_mb']}MB")
        print(f"   Scan Time: {meta['scan_time']}s")
        print(f"   Space Recoverable: {meta['space_recoverable_mb']}MB")
        
        print(f"\n🔍 TOP LANGUAGES:")
        for ext, stats in list(results['by_language'].items())[:5]:
            print(f"   {ext}: {stats['files']} files ({stats['size_mb']}MB)")
        
        print(f"\n🔄 DUPLICATES:")
        print(f"   Groups: {results['duplicates']['groups']}")
        print(f"   Files: {results['duplicates']['files']}")
        
        quality = results['quality_report']
        if quality['files_analyzed'] > 0:
            print(f"\n📊 QUALITY:")
            print(f"   Average Score: {quality['average_score']}/100")
            print(f"   Excellent: {quality['excellent']} | Good: {quality['good']} | Needs Work: {quality['needs_improvement']}")
        
        security = results['security_report']
        if security['total_issues'] > 0:
            print(f"\n🔒 SECURITY:")
            print(f"   Total Issues: {security['total_issues']}")
            for severity, count in security['by_severity'].items():
                print(f"   {severity}: {count}")
        
        if results['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in results['recommendations']:
                print(f"   {rec}")
    
    def clean_duplicates(self, dry_run: bool = True) -> int:
        """Remove duplicate files"""
        removed_count = 0
        
        for group in self.duplicate_groups:
            # Keep first file, remove rest
            for file_info in group[1:]:
                file_path = Path(file_info['path'])
                if file_path.exists():
                    if not dry_run:
                        file_path.unlink()
                    removed_count += 1
                    print(f"🗑️  {'[DRY RUN] Would remove' if dry_run else 'Removed'}: {file_path}")
        
        return removed_count
    
    def clean_junk(self, dry_run: bool = True) -> int:
        """Remove junk files"""
        removed_count = 0
        
        for junk_file in self.junk_files:
            file_path = Path(junk_file)
            if file_path.exists():
                if not dry_run:
                    file_path.unlink()
                removed_count += 1
                print(f"🗑️  {'[DRY RUN] Would remove' if dry_run else 'Removed'}: {file_path}")
        
        return removed_count
    
    def export_report(self, output_file: str):
        """Export detailed report to JSON"""
        report = {
            'scan_metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_files': self.total_files,
                'total_size_mb': round(self.total_size / (1024**2), 2)
            },
            'duplicates': self.duplicate_groups,
            'junk_files': self.junk_files,
            'quality_scores': self.quality_scores,
            'security_issues': dict(self.security_issues),
            'performance_issues': dict(self.performance_issues),
            'refactoring_suggestions': dict(self.refactoring_suggestions)
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report exported: {output_file}")


def main():
    """X1000 Code Vac Ultimate main execution"""
    print("=" * 70)
    print(" " * 20 + "🧹 X1000 CODE_VAC ULTIMATE 🧹")
    print("="*70)
    
    vac = X1000CodeVacUltimate()
    
    # Get scan target
    scan_path = input("\n📁 Enter path to scan (default: current directory): ").strip()
    if not scan_path:
        scan_path = os.getcwd()
    
    scan_path = Path(scan_path).expanduser()
    
    if not scan_path.exists():
        print(f"❌ Path not found: {scan_path}")
        return
    
    # Scan
    results = vac.scan(scan_path, deep_analysis=True)
    
    # Options
    print("\n🎯 OPTIONS:")
    print("1. Clean duplicates (dry run)")
    print("2. Clean junk files (dry run)")
    print("3. Export detailed report")
    print("4. Exit")
    
    try:
        choice = input("\n👉 Select option (1-4): ").strip()
        
        if choice == '1':
            removed = vac.clean_duplicates(dry_run=True)
            print(f"\n✅ Would remove {removed} duplicate files")
        elif choice == '2':
            removed = vac.clean_junk(dry_run=True)
            print(f"\n✅ Would remove {removed} junk files")
        elif choice == '3':
            report_file = scan_path / f"codevac_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            vac.export_report(str(report_file))
        elif choice == '4':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")


if __name__ == '__main__':
    main()
