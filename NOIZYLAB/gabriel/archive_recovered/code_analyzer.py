#!/usr/bin/env python3
"""
GABRIEL Code Analyzer - REAL static analysis using AST
Provides actual code metrics, not marketing fluff
"""
import ast
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

class CodeAnalyzer:
    """Real code analysis with AST parsing"""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'base_path': str(self.base_path),
            'files': {},
            'summary': {},
            'dependencies': defaultdict(list),
            'functions': [],
            'classes': [],
            'complexity': {},
            'issues': []
        }

        # File extensions to analyze
        self.python_exts = {'.py'}
        self.js_exts = {'.js', '.jsx', '.ts', '.tsx'}
        self.all_code_exts = self.python_exts | self.js_exts | {'.go', '.rs', '.c', '.cpp', '.h', '.java', '.swift'}

        # Directories to skip
        self.skip_dirs = {'node_modules', 'venv', '.venv', '__pycache__', '.git', 'dist', 'build', '.next'}

    def analyze_python_file(self, filepath: Path) -> dict:
        """Deep analysis of Python file using AST"""
        result = {
            'path': str(filepath),
            'language': 'python',
            'lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity': 0,
            'issues': []
        }

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            result['lines'] = len(lines)

            # Count line types
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    result['blank_lines'] += 1
                elif stripped.startswith('#'):
                    result['comment_lines'] += 1
                else:
                    result['code_lines'] += 1

            # Parse AST
            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    # Extract functions
                    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                        func_info = {
                            'name': node.name,
                            'file': str(filepath.relative_to(self.base_path)),
                            'line': node.lineno,
                            'args': len(node.args.args),
                            'complexity': self._calculate_complexity(node),
                            'docstring': ast.get_docstring(node) is not None,
                            'async': isinstance(node, ast.AsyncFunctionDef)
                        }
                        result['functions'].append(func_info)
                        result['complexity'] += func_info['complexity']

                        # Flag high complexity
                        if func_info['complexity'] > 10:
                            result['issues'].append({
                                'type': 'high_complexity',
                                'message': f"Function '{node.name}' has complexity {func_info['complexity']}",
                                'line': node.lineno
                            })

                    # Extract classes
                    elif isinstance(node, ast.ClassDef):
                        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                        class_info = {
                            'name': node.name,
                            'file': str(filepath.relative_to(self.base_path)),
                            'line': node.lineno,
                            'methods': methods,
                            'method_count': len(methods),
                            'docstring': ast.get_docstring(node) is not None
                        }
                        result['classes'].append(class_info)

                    # Extract imports
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            result['imports'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            result['imports'].append(node.module)

            except SyntaxError as e:
                result['issues'].append({
                    'type': 'syntax_error',
                    'message': str(e),
                    'line': e.lineno
                })

        except Exception as e:
            result['issues'].append({
                'type': 'read_error',
                'message': str(e)
            })

        return result

    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Control flow statements add complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.Assert):
                complexity += 1

        return complexity

    def analyze_js_file(self, filepath: Path) -> dict:
        """Basic analysis of JavaScript/TypeScript file"""
        result = {
            'path': str(filepath),
            'language': 'javascript' if filepath.suffix in {'.js', '.jsx'} else 'typescript',
            'lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': [],
            'classes': [],
            'imports': [],
            'exports': [],
            'complexity': 0,
            'issues': []
        }

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            result['lines'] = len(lines)

            in_multiline_comment = False

            for i, line in enumerate(lines, 1):
                stripped = line.strip()

                if not stripped:
                    result['blank_lines'] += 1
                    continue

                # Handle multiline comments
                if '/*' in stripped:
                    in_multiline_comment = True
                if '*/' in stripped:
                    in_multiline_comment = False
                    result['comment_lines'] += 1
                    continue

                if in_multiline_comment or stripped.startswith('//'):
                    result['comment_lines'] += 1
                else:
                    result['code_lines'] += 1

                # Extract functions (regex-based)
                func_match = re.search(r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[^=])\s*=>|(\w+)\s*\([^)]*\)\s*{)', stripped)
                if func_match:
                    name = func_match.group(1) or func_match.group(2) or func_match.group(3)
                    if name and name not in ['if', 'for', 'while', 'switch', 'catch']:
                        result['functions'].append({
                            'name': name,
                            'file': str(filepath.relative_to(self.base_path)),
                            'line': i
                        })

                # Extract classes
                class_match = re.search(r'class\s+(\w+)', stripped)
                if class_match:
                    result['classes'].append({
                        'name': class_match.group(1),
                        'file': str(filepath.relative_to(self.base_path)),
                        'line': i
                    })

                # Extract imports
                import_match = re.search(r"(?:import|require)\s*\(?['\"]([^'\"]+)['\"]", stripped)
                if import_match:
                    result['imports'].append(import_match.group(1))

                # Extract exports
                if 'export ' in stripped:
                    result['exports'].append(i)

                # Estimate complexity
                if any(kw in stripped for kw in ['if ', 'else ', 'for ', 'while ', 'switch ', 'catch ', '&&', '||', '?']):
                    result['complexity'] += 1

        except Exception as e:
            result['issues'].append({
                'type': 'read_error',
                'message': str(e)
            })

        return result

    def analyze_generic_file(self, filepath: Path) -> dict:
        """Basic line counting for other languages"""
        result = {
            'path': str(filepath),
            'language': filepath.suffix.lstrip('.'),
            'lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'issues': []
        }

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            result['lines'] = len(lines)

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    result['blank_lines'] += 1
                elif stripped.startswith(('#', '//', '--', ';', '*')):
                    result['comment_lines'] += 1
                else:
                    result['code_lines'] += 1

        except Exception as e:
            result['issues'].append({
                'type': 'read_error',
                'message': str(e)
            })

        return result

    def analyze_file(self, filepath: Path) -> dict:
        """Route to appropriate analyzer based on file type"""
        if filepath.suffix in self.python_exts:
            return self.analyze_python_file(filepath)
        elif filepath.suffix in self.js_exts:
            return self.analyze_js_file(filepath)
        elif filepath.suffix in self.all_code_exts:
            return self.analyze_generic_file(filepath)
        return None

    def scan(self, max_workers: int = 8) -> dict:
        """Scan entire codebase with parallel processing"""
        files_to_analyze = []

        # Collect files
        for root, dirs, files in os.walk(self.base_path):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs and not d.startswith('.')]

            for file in files:
                filepath = Path(root) / file
                if filepath.suffix in self.all_code_exts:
                    files_to_analyze.append(filepath)

        print(f"Analyzing {len(files_to_analyze)} code files...")

        # Parallel analysis
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.analyze_file, f): f for f in files_to_analyze}

            for future in as_completed(futures):
                filepath = futures[future]
                try:
                    result = future.result()
                    if result:
                        rel_path = str(filepath.relative_to(self.base_path))
                        self.results['files'][rel_path] = result

                        # Aggregate functions and classes
                        self.results['functions'].extend(result.get('functions', []))
                        self.results['classes'].extend(result.get('classes', []))
                        self.results['issues'].extend(result.get('issues', []))

                        # Track dependencies
                        for imp in result.get('imports', []):
                            self.results['dependencies'][imp].append(rel_path)

                except Exception as e:
                    print(f"Error analyzing {filepath}: {e}")

        # Generate summary
        self._generate_summary()

        return self.results

    def _generate_summary(self):
        """Generate analysis summary"""
        total_lines = 0
        total_code = 0
        total_comments = 0
        total_blank = 0
        total_complexity = 0
        lang_stats = defaultdict(lambda: {'files': 0, 'lines': 0, 'code_lines': 0})

        for filepath, data in self.results['files'].items():
            lang = data.get('language', 'unknown')
            lang_stats[lang]['files'] += 1
            lang_stats[lang]['lines'] += data.get('lines', 0)
            lang_stats[lang]['code_lines'] += data.get('code_lines', 0)

            total_lines += data.get('lines', 0)
            total_code += data.get('code_lines', 0)
            total_comments += data.get('comment_lines', 0)
            total_blank += data.get('blank_lines', 0)
            total_complexity += data.get('complexity', 0)

        # Find most complex functions
        sorted_funcs = sorted(
            [f for f in self.results['functions'] if f.get('complexity', 0) > 0],
            key=lambda x: x.get('complexity', 0),
            reverse=True
        )[:20]

        # Find most imported modules
        sorted_deps = sorted(
            self.results['dependencies'].items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:20]

        self.results['summary'] = {
            'total_files': len(self.results['files']),
            'total_lines': total_lines,
            'code_lines': total_code,
            'comment_lines': total_comments,
            'blank_lines': total_blank,
            'total_functions': len(self.results['functions']),
            'total_classes': len(self.results['classes']),
            'total_complexity': total_complexity,
            'avg_complexity': total_complexity / len(self.results['functions']) if self.results['functions'] else 0,
            'total_issues': len(self.results['issues']),
            'languages': dict(lang_stats),
            'most_complex_functions': sorted_funcs,
            'most_used_imports': [(k, len(v)) for k, v in sorted_deps],
            'comment_ratio': (total_comments / total_code * 100) if total_code > 0 else 0
        }

    def get_report(self) -> str:
        """Generate human-readable report"""
        s = self.results['summary']

        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                 GABRIEL CODE ANALYSIS REPORT                     ║
║                    Real Metrics, No Fluff                        ║
╚══════════════════════════════════════════════════════════════════╝

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Files Analyzed:    {s['total_files']:,}
  Total Lines:       {s['total_lines']:,}
  Code Lines:        {s['code_lines']:,}
  Comment Lines:     {s['comment_lines']:,}
  Blank Lines:       {s['blank_lines']:,}
  Comment Ratio:     {s['comment_ratio']:.1f}%

📦 CODE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Functions:         {s['total_functions']:,}
  Classes:           {s['total_classes']:,}
  Total Complexity:  {s['total_complexity']:,}
  Avg Complexity:    {s['avg_complexity']:.2f}
  Issues Found:      {s['total_issues']:,}

🔤 LANGUAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        for lang, stats in sorted(s['languages'].items(), key=lambda x: -x[1]['code_lines']):
            report += f"\n  {lang:12} {stats['files']:>6} files  {stats['code_lines']:>8,} lines"

        report += """

⚡ MOST COMPLEX FUNCTIONS (Top 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        for func in s['most_complex_functions'][:10]:
            report += f"\n  {func['complexity']:>3}  {func['name']:<30} {func['file']}:{func['line']}"

        report += """

📚 MOST USED IMPORTS (Top 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        for module, count in s['most_used_imports'][:10]:
            report += f"\n  {count:>4}x  {module}"

        if s['total_issues'] > 0:
            report += """

⚠️  ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
            for issue in self.results['issues'][:10]:
                report += f"\n  [{issue['type']}] {issue['message']}"

        report += "\n"
        return report


def main():
    if len(sys.argv) < 2:
        target = "/Users/m2ultra/NOIZYLAB/GABRIEL"
    else:
        target = sys.argv[1]

    analyzer = CodeAnalyzer(target)
    results = analyzer.scan()

    # Print report
    print(analyzer.get_report())

    # Save JSON
    output_path = Path(target) / 'code_analysis.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"📄 Full report saved to: {output_path}")


if __name__ == '__main__':
    main()
