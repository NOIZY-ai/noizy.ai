import sys
import os
import subprocess
import argparse
from noizy_memcell import memory_core

# NOIZYLAB CINEMA v2.0
# "Director" Module: Strongest Local Video Capabilities
# OPTIMIZED: MemCell Integration, Robust FFmpeg Wrapper

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        print("!!! ERROR: FFmpeg not found.")
        memory_core.log_interaction("FFmpeg Missing", "CRITICAL_ERROR", "ENGR")
        return False

def run_ffmpeg(cmd_list, desc):
    if not check_ffmpeg(): return
    
    memory_core.log_interaction(f"Cinema Job: {desc}", "RENDER_START", "DIRECTOR")
    try:
        print(f"    -> EXEC: {' '.join(cmd_list)}")
        subprocess.run(cmd_list, check=True)
        memory_core.log_interaction(f"Cinema Job: {desc}", "SUCCESS", "DIRECTOR")
    except subprocess.CalledProcessError as e:
        print(f"!!! FFmpeg Error: {e}")
        memory_core.log_interaction(f"Render Failed: {e}", "ERROR", "ENGR")

def extract_audio(input_file, fmt="mp3"):
    print(f"\n>>> [NOIZY CINEMA] EXTRACTING AUDIO FROM: {input_file}")
    base = os.path.splitext(input_file)[0]
    output = f"{base}.{fmt}"
    
    cmd = ["ffmpeg", "-i", input_file, "-vn"]
    if fmt == "mp3":
        cmd.extend(["-acodec", "libmp3lame", "-q:a", "0"]) 
    elif fmt == "wav":
        cmd.extend(["-acodec", "pcm_s16le"])
    
    cmd.append(output)
    run_ffmpeg(cmd, "Extract Audio")
    print(f"    -> EXPORTED: {output}")

def compress_video(input_file, crf=23):
    print(f"\n>>> [NOIZY CINEMA] COMPRESSING VISUALS: {input_file}")
    base = os.path.splitext(input_file)[0]
    output = f"{base}_optimized.mp4"
    
    cmd = ["ffmpeg", "-i", input_file, "-vcodec", "libx264", "-crf", str(crf), "-preset", "fast", output]
    run_ffmpeg(cmd, "Compress Video")
    print(f"    -> OPTIMIZED: {output}")

def make_visualizer(audio_file):
    print(f"\n>>> [NOIZY CINEMA] GENERATING VISUALIZER FOR: {audio_file}")
    base = os.path.splitext(audio_file)[0]
    output = f"{base}_visualizer.mp4"
    
    filter_graph = "showwaves=s=1920x1080:mode=line:colors=cyan:rate=25,format=yuv420p[v]"
    cmd = ["ffmpeg", "-i", audio_file, "-filter_complex", filter_graph, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "fast", output]
    
    run_ffmpeg(cmd, "Generate Visualizer")
    print(f"    -> CREATED: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoizyLab Cinema Tools")
    parser.add_argument("input", help="Input media file")
    parser.add_argument("--extract", help="Extract audio (mp3/wav)", type=str)
    parser.add_argument("--compress", help="Compress video (CRF value)", type=int)
    parser.add_argument("--visualize", help="Create visualizer from audio", action="store_true")

    args = parser.parse_args()
    
    if args.extract:
        extract_audio(args.input, args.extract)
    elif args.compress:
        compress_video(args.input, args.compress)
    elif args.visualize:
        make_visualizer(args.input)
    else:
        print("Please specify a mode: --extract, --compress, or --visualize")
