#/*bin/true;cat<<'EOF'>/dev/null 2>&1
#<?php echo"PHP\n";__halt_compiler();?>
#*/
#include/*
q='''
=begin
--[[
#`[
#`(
"""
:
exec python3 "$0" "$@"
"""
#Different interpreters see different code!
print("Python"); exit()
#=cut
#*/
#include <stdio.h>
int main(){printf("C\n");return 0;}
#if 0
'''
#=end
#--]]
#`]
#`)
#Ruby
puts "Ruby"
__END__
=cut
print "Perl\n";
__END__
--Lua
print("Lua")
--[[
#endif
/*
*/
