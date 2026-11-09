# 🍎 Apple Sample Code Index

**Date**: 2025-12-23
**Context**: Support for Gabriel Native Bridge (Metal & Security)

## 1. Metal (C++)

The M2 Ultra GPU requires `metal-cpp` for native C++ access without Objective-C overhead.

### Official Resources

- **Reference**: [Metal-cpp Specification](https://developer.apple.com/metal/cpp/)
- **Sample Series**: "Learn Metal with C++" (Apple Developer)
- **WWDC Session**: "Program Metal in C++ with metal-cpp" (WWDC22)

### Community Repositories (GitHub)

- **`postmalloc/metal-cpp-example`**: Pure C++ port of Apple's examples.
- **`LeeTeng2001/metal-cpp-cmake`**: CMake build system adaptation (Useful for our Makefile).
- **`metal-by-example/learn-metal-cpp-ios`**: Comprehensive tutorials.

## 2. Endpoint Security (C/C++)

For file monitoring and process interception (replacing `gabriel_fsevents.c` in production).

### Official Resources

- **Project**: `SampleEndpointApp` (WWDC 2020 Session 10159)
- **Capabilities**:
  - **NOTIFY**: Passive monitoring (what we have now).
  - **AUTH**: Active blocking (future feature).

## 3. General Native Integration

- **Argument Buffers**: Efficiently passing data to GPU.
- **Function Pointers**: Dynamic pipeline states in Metal 3.
- **Mesh Shaders**: Advanced geometry processing for MC96.

**Action Item**: Proceed to mirror `SampleEndpointApp` logic in our local `gabriel_fsevents.c`.
