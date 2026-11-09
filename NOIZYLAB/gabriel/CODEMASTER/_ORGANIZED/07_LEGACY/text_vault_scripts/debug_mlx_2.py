import mlx.core as mx
try:
    print(f"mx.fft type: {type(mx.fft)}")
    # Try a dummy FFT
    a = mx.array([1, 2, 3, 4])
    print("Calling mx.fft.rfft(a)...")
    spec = mx.fft.rfft(a)
    print("Success!")
    print(spec)
except Exception as e:
    print(f"Error: {e}")
