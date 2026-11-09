import os
import json
import csv

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.aiff', '.alac'}

REPORT_CSV = '/Users/m2ultra/joe_audio_report.csv'
REPORT_JSON = '/Users/m2ultra/joe_audio_report.json'
SCAN_ROOT = '/Volumes/JOE'

def is_audio_file(filename):
    return any(filename.lower().endswith(ext) for ext in AUDIO_EXTENSIONS)

def scan_audio_files(root):
    audio_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if is_audio_file(fname):
                full_path = os.path.join(dirpath, fname)
                # Duration skipped for speed
                audio_files.append({
                    'path': full_path,
                    'duration_seconds': 0,
                    'duration_hms': "N/A (Fast Scan)"
                })
    return audio_files

def write_csv(audio_files, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['path', 'duration_seconds', 'duration_hms'])
        writer.writeheader()
        for entry in audio_files:
            writer.writerow(entry)

def write_json(audio_files, json_path):
    with open(json_path, 'w') as f:
        json.dump(audio_files, f, indent=2)

def main():
    print(f'Scanning {SCAN_ROOT} for audio files (Fast Mode)...')
    audio_files = scan_audio_files(SCAN_ROOT)
    print(f'Found {len(audio_files)} audio files. Writing reports...')
    write_csv(audio_files, REPORT_CSV)
    write_json(audio_files, REPORT_JSON)
    print(f'Reports written to {REPORT_CSV} and {REPORT_JSON}')

if __name__ == '__main__':
    main()
