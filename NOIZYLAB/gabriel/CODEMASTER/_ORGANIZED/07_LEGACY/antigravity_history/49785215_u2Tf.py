import json
import uuid
import datetime
import os

# Configuration
SOURCE_REPORT = '/Users/m2ultra/joe_audio_report.json'
TARGET_LIBRARY = '/Users/m2ultra/NOIZYLAB/data/audio_library.json'

def load_source_data(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Source file {filepath} not found.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def load_existing_library(filepath):
    if not os.path.exists(filepath):
        return {"meta": {}, "tracks": []}
    with open(filepath, 'r') as f:
        return json.load(f)

def ingest_tracks(source_data):
    tracks = []
    print(f"Processing {len(source_data)} tracks...")
    
    for entry in source_data:
        # Create a unique ID for each track
        track_id = str(uuid.uuid4())
        
        # Extract filename and folder
        full_path = entry.get('path', '')
        filename = os.path.basename(full_path)
        folder = os.path.dirname(full_path)
        
        # Determine basic tags
        tags = ["audio", "JOE"]
        if "Kontakt" in full_path:
            tags.append("kontakt")
        if ".wav" in filename.lower():
            tags.append("wav")
        
        track = {
            "id": track_id,
            "path": full_path,
            "filename": filename,
            "folder": folder, # Preserving folder structure
            "duration": entry.get('duration_seconds', 0),
            "hms": entry.get('duration_hms', ''),
            "tags": tags,
            "added_at": datetime.datetime.now().isoformat()
        }
        tracks.append(track)
        
    return tracks

def save_library(library_data, filepath):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Update Metadata
    library_data["meta"] = {
        "last_updated": datetime.datetime.now().isoformat(),
        "total_tracks": len(library_data["tracks"]),
        "version": "1.0"
    }
    
    with open(filepath, 'w') as f:
        json.dump(library_data, f, indent=2)
    print(f"Library saved to {filepath} with {len(library_data['tracks'])} tracks.")

def main():
    print("Starting Audio Library Ingestion...")
    
    source_data = load_source_data(SOURCE_REPORT)
    if not source_data:
        return

    # In a full merge scenario, we might want to check for duplicates against existing DB.
    # For this initial ingestion, we will treat the scan as the master source for this volume.
    # If we want to append, we would follow a different logic.
    # Assuming "fresh start" for this volume based on the request "FOUND ALL...".
    
    tracks = ingest_tracks(source_data)
    
    library = {
        "meta": {},
        "tracks": tracks
    }
    
    save_library(library, TARGET_LIBRARY)
    print("Ingestion Complete.")

if __name__ == "__main__":
    main()
