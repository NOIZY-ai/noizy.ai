/*
#!/bin/bash
# This file compiles/runs as: C, C++, Objective-C, and runs as Bash
echo "Bash/Shell"
exit 0
*/

#if 0
Bash execution handled above
#endif

#ifdef __OBJC__
    #import <Foundation/Foundation.h>
#else
    #ifdef __cplusplus
        #include <iostream>
    #else
        #include <stdio.h>
    #endif
#endif

int main(int argc, char *argv[]) {
    #ifdef __OBJC__
        @autoreleasepool {
            NSLog(@"Objective-C");
        }
    #else
        #ifdef __cplusplus
            std::cout << "C++" << std::endl;
        #else
            printf("C\n");
        #endif
    #endif
    return 0;
}

/*
COMPILATION:
    gcc compiled_polyglot.c -o polyglot_c && ./polyglot_c
    g++ compiled_polyglot.c -o polyglot_cpp && ./polyglot_cpp  
    clang -framework Foundation compiled_polyglot.c -o polyglot_objc && ./polyglot_objc
    bash compiled_polyglot.c
*/
