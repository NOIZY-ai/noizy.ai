import sys
import os
import subprocess
import argparse

# NOIZYLAB CINEMA v1.0
# "Director" Module: Strongest Local Video Capabilities
# Powered by: FFmpeg (The industry standard)

def run_ffmpeg(cmd_list):
    try:
        print(f"    -> EXEC: {' '.join(cmd_list)}")
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        print(f"!!! FFmpeg Error: {e}")

def extract_audio(input_file, fmt="mp3"):
    print(f"\n>>> [NOIZY CINEMA] EXTRACTING AUDIO FROM: {input_file}")
    base = os.path.splitext(input_file)[0]
    output = f"{base}.{fmt}"
    
    # -vn: Disable video, -acodec: copy (if possible) or libmp3lame
    cmd = ["ffmpeg", "-i", input_file, "-vn"]
    if fmt == "mp3":
        cmd.extend(["-acodec", "libmp3lame", "-q:a", "0"]) # Best quality VBR
    elif fmt == "wav":
        cmd.extend(["-acodec", "pcm_s16le"])
    
    cmd.append(output)
    run_ffmpeg(cmd)
    print(f"    -> EXPORTED: {output}")

def compress_video(input_file, crf=23):
    print(f"\n>>> [NOIZY CINEMA] COMPRESSING VISUALS: {input_file}")
    base = os.path.splitext(input_file)[0]
    output = f"{base}_optimized.mp4"
    
    # CRF 18-28 is sane. Lower is better quality.
    cmd = ["ffmpeg", "-i", input_file, "-vcodec", "libx264", "-crf", str(crf), "-preset", "fast", output]
    run_ffmpeg(cmd)
    print(f"    -> OPTIMIZED: {output}")

def make_visualizer(audio_file, image_file=None):
    print(f"\n>>> [NOIZY CINEMA] GENERATING VISUALIZER FOR: {audio_file}")
    base = os.path.splitext(audio_file)[0]
    output = f"{base}_visualizer.mp4"
    
    # Simple waveform visualizer
    # ffmpeg -i audio.mp3 -filter_complex "showwaves=s=1280x720:mode=line:rate=25,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -c:a copy out.mp4
    
    cmd = ["ffmpeg", "-i", audio_file]
    
    # Complex filter for reactive waveform
    filter_graph = "showwaves=s=1920x1080:mode=line:colors=cyan:rate=25,format=yuv420p[v]"
    
    cmd.extend(["-filter_complex", filter_graph, "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "fast", output])
    
    run_ffmpeg(cmd)
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
