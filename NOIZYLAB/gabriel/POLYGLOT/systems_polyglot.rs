// Rust / Go / Zig / D / V Systems Polyglot
// Each language sees different valid code

#![allow(unused)]

/* Go code (commented for Rust)
package main
import "fmt"
func main() { fmt.Println("Go") }
*/

/* Zig code (commented for Rust)
const std = @import("std");
pub fn main() void {
    std.debug.print("Zig\n", .{});
}
*/

/* D code (commented for Rust)
import std.stdio;
void main() { writeln("D"); }
*/

/* V code (commented for Rust)
fn main() { println('V') }
*/

fn main() {
    println!("Rust");
}
