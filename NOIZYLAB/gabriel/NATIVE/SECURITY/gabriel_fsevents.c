/**
 * gabriel_fsevents.c
 * Part of GABRIEL SYSTEM OMEGA (Native Bridge)
 * 
 * High-Performance File System Monitor for macOS
 * Uses FSEvents/CoreServices for Zero Latency tracking.
 */

#include <CoreServices/CoreServices.h>
#include <stdio.h>
#include <stdlib.h>

// Callback function when an event occurs
void myCallbackFunction(
    ConstFSEventStreamRef streamRef,
    void *clientCallBackInfo,
    size_t numEvents,
    void *eventPaths,
    const FSEventStreamEventFlags eventFlags[],
    const FSEventStreamEventId eventIds[])
{
    int i;
    char **paths = (char **)eventPaths;

    // Output JSON-like format for Python parser to consume
    for (i = 0; i < numEvents; i++) {
        printf("{\"event\": \"change\", \"path\": \"%s\", \"id\": %llu}\n", paths[i], eventIds[i]);
        fflush(stdout); // Ensure Python side gets it immediately
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <path_to_watch>\n", argv[0]);
        return 1;
    }

    const char *path_to_watch = argv[1];
    printf("[NATIVE-SEC] Gabriel Sentry watching: %s\n", path_to_watch);

    CFStringRef myPath = CFStringCreateWithCString(NULL, path_to_watch, kCFStringEncodingUTF8);
    CFArrayRef pathsToWatch = CFArrayCreate(NULL, (const void **)&myPath, 1, NULL);

    void *callbackInfo = NULL;
    FSEventStreamRef stream;
    CFAbsoluteTime latency = 0.1; /* Latency in seconds */

    stream = FSEventStreamCreate(
        NULL,
        &myCallbackFunction,
        callbackInfo,
        pathsToWatch,
        kFSEventStreamEventIdSinceNow,
        latency,
        kFSEventStreamCreateFlagNone
    );

    FSEventStreamScheduleWithRunLoop(stream, CFRunLoopGetCurrent(), kCFRunLoopDefaultMode);
    FSEventStreamStart(stream);

    // Keep the utility running
    CFRunLoopRun();

    return 0;
}
