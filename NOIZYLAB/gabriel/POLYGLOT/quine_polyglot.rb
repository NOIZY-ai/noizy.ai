#/*
s='#/*%cs=%r;print s%%((39,s)*2)%c#*/include<stdio.h>%cint main(){char*s="#/*%%cs=%%r;print s%%%%(%%s)%%c#*/include<stdio.h>%%cint main(){char*s=%%c%%s%%c;printf(s,39,s,39,10,10,34,s,34,10,10,10);}%%c";printf(s,39,s,39,10,10,34,s,34,10,10,10);}%c';print s%((39,s)*2)
#*/
#if 0
s='#/*%cs=%r;print s%%((39,s)*2)%c#*/include<stdio.h>%cint main(){char*s="#/*%%cs=%%r;print s%%%%(%%s)%%c#*/include<stdio.h>%%cint main(){char*s=%%c%%s%%c;printf(s,39,s,39,10,10,34,s,34,10,10,10);}%%c";printf(s,39,s,39,10,10,34,s,34,10,10,10);}%c';print s%((39,s)*2)
=begin
#endif
#include<stdio.h>
int main(){char*s="#/*%cs=%r;print s%%((39,s)*2)%c#*/include<stdio.h>%cint main(){char*s=\"#/*%%cs=%%r;print s%%%%(%%s)%%c#*/include<stdio.h>%%cint main(){char*s=%%c%%s%%c;printf(s,39,s,39,10,10,34,s,34,10,10,10);}%%c\";printf(s,39,s,39,10,10,34,s,34,10,10,10);}%c";printf(s,39,s,39,10,10,34,s,34,10,10,10);}
#if 0
=end
puts "Ruby Quine Polyglot"
__END__
#endif
