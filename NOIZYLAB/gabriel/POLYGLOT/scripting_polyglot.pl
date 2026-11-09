#!/usr/bin/env perl
#|ruby -e'puts"Ruby";exit'
#|python3 -c'print("Python3");exit()'
#|node -e'console.log("Node.js");process.exit()'
#|lua -e'print("Lua");os.exit()'
#|php -r'echo"PHP\n";exit;'
#|awk 'BEGIN{print"AWK";exit}'
#|sed -n 's/.*/SED/p;q'

eval 'exec perl -x $0 ${1+"$@"}'
    if 0;

use strict;
use warnings;

print "Perl\n";

__END__

=pod

=head1 SCRIPTING POLYGLOT

This file executes correctly in:

=over 4

=item * Perl (primary)
=item * Ruby  
=item * Python3
=item * Node.js
=item * Lua
=item * PHP
=item * AWK
=item * SED

=back

=head1 USAGE

    perl scripting_polyglot.pl
    ruby scripting_polyglot.pl  
    python3 scripting_polyglot.pl
    node scripting_polyglot.pl
    lua scripting_polyglot.pl

=cut
