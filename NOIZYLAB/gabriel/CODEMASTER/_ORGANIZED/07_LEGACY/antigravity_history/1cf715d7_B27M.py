
import sys
import os
import time

# Add path
sys.path.append("/Users/m2ultra/NOIZYLAB/GABRIEL")

from agency_utils import DreamFactory, ImageGenerator

def stress_test():
    print("🩸 STARTING V31 STRESS TEST (OP MODE)...")
    
    # 1. Mock Audio
    audio_path = "/Users/m2ultra/NOIZYLAB/GABRIEL/tests/test_audio.mp3"
    # Create a dummy audio file if not exists (silence or sine wave)
    if not os.path.exists(audio_path):
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        # Generate 2 seconds of silence using ffmpeg
        os.system(f"ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 2 -q:a 9 -acodec libmp3lame {audio_path} -y")
        print("   ✅ Mock Audio Created")
        
    # 2. Generate Image URL
    print("   🔮 Generating Image...")
    start_t = time.time()
    img_url = ImageGenerator.generate("Stress Test Dune Aesthetic")
    print(f"   ✅ Image URL Generated ({time.time() - start_t:.2f}s)")
    
    # 3. Create Dream
    print("   🎞️ Rendering Dream (Video)...")
    start_t = time.time()
    video_path = DreamFactory.create_dream(audio_path, img_url)
    render_time = time.time() - start_t
    
    if video_path and os.path.exists(video_path):
        print(f"   ✅ DREAM RENDERED SUCCESSFULLY!")
        print(f"   ⏱️ Render Time: {render_time:.2f}s")
        print(f"   📂 Output: {video_path}")
        
        # Verify size
        size = os.path.getsize(video_path)
        print(f"   📦 Size: {size/1024:.2f} KB")
        return True
    else:
        print("   ❌ DREAM FAILED.")
        return False

if __name__ == "__main__":
    stress_test()
