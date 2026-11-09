# GABRIEL NATIVE BUILD SYSTEM
# Builds Metal-cpp kernels and FSEvents monitor

CC=clang
CXX=clang++
CFLAGS=-O3 -Wall
CXXFLAGS=-std=c++17 -O3 -Wall -fno-objc-arc

# HEADERS & FRAMEWORKS
# Pointing to the found MLX metal-cpp headers
INCLUDES=-I/Users/m2ultra/NOIZYLAB/MC96/venv/lib/python3.14/site-packages/mlx/include/metal_cpp

LDFLAGS=-framework CoreServices
# Metal-cpp needs Foundation, Metal, QuartzCore
METAL_LDFLAGS=-framework Metal -framework Foundation -framework QuartzCore -framework CoreGraphics -framework AppKit

OUT_DIR=../bin

.PHONY: all setup build_security build_metal clean

all: setup build_security build_metal

setup:
	mkdir -p $(OUT_DIR)

build_security:
	@echo "Building Gabriel FSEvents Sentry..."
	$(CC) $(CFLAGS) $(LDFLAGS) SECURITY/gabriel_fsevents.c -o $(OUT_DIR)/gabriel_fsevents
	@echo "✅ Built: $(OUT_DIR)/gabriel_fsevents"

build_metal:
	@echo "🔨 Building Gabriel Metal Core (Runtime Compile Mode)..."
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(METAL_LDFLAGS) METAL/GabrielHeavyCompute.cpp -o $(OUT_DIR)/gabriel_metal_proto
	@echo "✅ Built Host: $(OUT_DIR)/gabriel_metal_proto"

clean:
	rm -f $(OUT_DIR)/gabriel_fsevents $(OUT_DIR)/gabriel_metal_proto
