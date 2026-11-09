import mlx.core as mx
try:
    import mlx.fft
    print("mlx.fft imported successfully")
except ImportError:
    print("mlx.fft NOT found")

print(f"MLX Version: {getattr(mx, '__version__', 'unknown')}")
print(f"MLX Dir: {dir(mx)}")
