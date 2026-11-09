#!/usr/bin/env python3
"""
POLYGLOT GENERATOR - Build custom polyglots
NOIZYLAB 2024
"""

import argparse
import sys
from typing import List, Dict

LANGUAGE_BLOCKS: Dict[str, Dict] = {
    "python": {
        "comment": "#",
        "multiline_start": '"""',
        "multiline_end": '"""',
        "hello": 'print("Python")',
        "exit": "exit()",
    },
    "ruby": {
        "comment": "#",
        "multiline_start": "=begin",
        "multiline_end": "=end",
        "hello": 'puts "Ruby"',
        "exit": "__END__",
    },
    "perl": {
        "comment": "#",
        "multiline_start": "=pod",
        "multiline_end": "=cut",
        "hello": 'print "Perl\\n"',
        "exit": "__END__",
    },
    "lua": {
        "comment": "--",
        "multiline_start": "--[[",
        "multiline_end": "]]",
        "hello": 'print("Lua")',
        "exit": "os.exit()",
    },
    "bash": {
        "comment": "#",
        "multiline_start": ": <<'POLYGLOT_END'",
        "multiline_end": "POLYGLOT_END",
        "hello": "echo Bash",
        "exit": "exit 0",
    },
    "c": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'puts("C");',
        "exit": "return 0;",
        "wrapper": 'int main(){%s}',
        "header": "#include<stdio.h>",
    },
    "javascript": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'console.log("JavaScript")',
        "exit": "",
    },
    "php": {
        "comment": "//",
        "hello": '<?php echo "PHP\\n"; exit; ?>',
        "exit": "",
    },
    "julia": {
        "comment": "#",
        "multiline_start": "#=",
        "multiline_end": "=#",
        "hello": 'println("Julia")',
        "exit": "",
    },
    "raku": {
        "comment": "#",
        "multiline_start": "#`[",
        "multiline_end": "]",
        "hello": 'say "Raku"',
        "exit": "exit",
    },
    # Systems Languages
    "rust": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'println!("Rust");',
        "exit": "",
        "wrapper": "fn main() { %s }",
    },
    "go": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'fmt.Println("Go")',
        "exit": "",
        "wrapper": 'package main\nimport "fmt"\nfunc main() { %s }',
    },
    "zig": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'std.debug.print("Zig\\n", .{});',
        "exit": "",
        "wrapper": 'const std = @import("std");\npub fn main() void { %s }',
    },
    "d": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": 'writeln("D");',
        "exit": "",
        "wrapper": "import std.stdio;\nvoid main() { %s }",
    },
    "v": {
        "comment": "//",
        "multiline_start": "/*",
        "multiline_end": "*/",
        "hello": "println('V')",
        "exit": "",
        "wrapper": "fn main() { %s }",
    },
}

TEMPLATES = {
    "minimal": """#/*
{php}
#*/
{python_start}
{ruby_start}
{lua_start}
{python_code}
{lua_end}
{ruby_end}
{ruby_code}
{lua_code}
""",
    "systems": """// Systems Polyglot - Rust / Go / Zig / D / V
// Compile with: rustc, go build, zig build, dmd, v
// Each language sees valid code, others in comments

/* Go code (hidden from Rust)
package main
import "fmt"
func main() { fmt.Println("Go") }
*/

/* Zig code (hidden from Rust)
const std = @import("std");
pub fn main() void { std.debug.print("Zig\\n", .{}); }
*/

/* D code (hidden from Rust)
import std.stdio;
void main() { writeln("D"); }
*/

/* V code (hidden from Rust)
fn main() { println('V') }
*/

fn main() {
    println!("Rust");
}
""",
    "full": """#/*bin/true 2>/dev/null
{php}
#*/
#include<stdio.h>/*
{julia_start}
{python_start}
{ruby_start}
{perl_start}
{lua_start}
{raku_start}
*/
int main(){{puts("C");return 0;}}
#if 0
{perl_end}
{perl_code};__END__
{ruby_end}
{ruby_code};__END__
{julia_end}
{julia_code}
{julia_start}
{raku_end}
{raku_code}
{lua_end}
{lua_code}
{lua_start}
{python_end}
{python_code}
#endif
exec echo Bash;exit
#*/
""",
}


def generate_polyglot(languages: List[str], template: str = "full") -> str:
    """Generate a polyglot for the specified languages."""
    replacements = {}
    
    for lang in LANGUAGE_BLOCKS:
        block = LANGUAGE_BLOCKS[lang]
        replacements[f"{lang}_start"] = block.get("multiline_start", "")
        replacements[f"{lang}_end"] = block.get("multiline_end", "")
        replacements[f"{lang}_code"] = block.get("hello", "")
        replacements[lang] = block.get("hello", "")
    
    result = TEMPLATES.get(template, TEMPLATES["full"])
    for key, value in replacements.items():
        result = result.replace(f"{{{key}}}", value)
    
    return result


def list_languages():
    """List all supported languages."""
    print("\n🌐 SUPPORTED LANGUAGES:\n")
    
    # Group by category
    scripting = ["python", "ruby", "perl", "lua", "bash", "javascript", "php", "julia", "raku"]
    systems = ["rust", "go", "zig", "d", "v", "c"]
    
    print("  SCRIPTING:")
    for lang in scripting:
        if lang in LANGUAGE_BLOCKS:
            print(f"    • {lang:<12} │ {LANGUAGE_BLOCKS[lang]['hello']}")
    
    print("\n  SYSTEMS:")
    for lang in systems:
        if lang in LANGUAGE_BLOCKS:
            print(f"    • {lang:<12} │ {LANGUAGE_BLOCKS[lang]['hello']}")
    
    print(f"\n  Total: {len(LANGUAGE_BLOCKS)} languages")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="🌐 POLYGLOT GENERATOR - Build custom polyglots",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    # Show available languages
  %(prog)s python ruby lua           # Generate Python/Ruby/Lua polyglot
  %(prog)s --all                     # Generate with all languages
  %(prog)s python ruby -o my.poly    # Save to file
        """,
    )
    parser.add_argument("languages", nargs="*", help="Languages to include")
    parser.add_argument("--list", "-l", action="store_true", help="List available languages")
    parser.add_argument("--all", "-a", action="store_true", help="Include all languages")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--template", "-t", choices=["minimal", "full", "systems"], default="full")
    
    args = parser.parse_args()
    
    if args.list:
        list_languages()
        return
    
    if args.all:
        languages = list(LANGUAGE_BLOCKS.keys())
    elif args.languages:
        languages = [l.lower() for l in args.languages]
        invalid = [l for l in languages if l not in LANGUAGE_BLOCKS]
        if invalid:
            print(f"❌ Unknown languages: {', '.join(invalid)}")
            print("Use --list to see available languages")
            sys.exit(1)
    else:
        parser.print_help()
        return
    
    polyglot = generate_polyglot(languages, args.template)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(polyglot)
        print(f"✅ Generated polyglot saved to: {args.output}")
        print(f"   Languages: {', '.join(languages)}")
    else:
        print(polyglot)


if __name__ == "__main__":
    main()
