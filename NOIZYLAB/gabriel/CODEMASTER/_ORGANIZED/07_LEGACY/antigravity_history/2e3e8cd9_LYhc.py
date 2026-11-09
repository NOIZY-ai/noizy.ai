import json
import random
import os

LIBRARY_PATH = '/Users/m2ultra/NOIZYLAB/data/audio_library.json'

class AudioLibrarian:
    def __init__(self, library_path=LIBRARY_PATH):
        self.library_path = library_path
        self.library = self._load_library()

    def _load_library(self):
        if not os.path.exists(self.library_path):
            print(f"Librarian Error: Library not found at {self.library_path}")
            return {"tracks": []}
        try:
            with open(self.library_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Librarian Error loading library: {e}")
            return {"tracks": []}

    def get_total_tracks(self):
        return len(self.library.get('tracks', []))

    def get_track_by_id(self, track_id):
        for track in self.library.get('tracks', []):
            if track['id'] == track_id:
                return track
        return None

    def get_random_track(self, filters=None):
        """
        Get a random track, optionally filtering by tags or properties.
        filters: dict (e.g., {'tags': ['wav']})
        """
        tracks = self.library.get('tracks', [])
        if not tracks:
            return None

        candidates = tracks
        if filters:
            if 'tags' in filters:
                required_tags = set(filters['tags'])
                candidates = [t for t in candidates if required_tags.issubset(set(t.get('tags', [])))]
        
        if not candidates:
            return None
            
        return random.choice(candidates)

    def search_tracks(self, query, limit=10):
        """Simple keyword search in filename or path."""
        results = []
        query = query.lower()
        for track in self.library.get('tracks', []):
            if query in track['filename'].lower() or query in track['path'].lower():
                results.append(track)
                if len(results) >= limit:
                    break
        return results

if __name__ == "__main__":
    # Simple test
    librarian = AudioLibrarian()
    print(f"Librarian Database: {librarian.get_total_tracks()} tracks loaded.")
    track = librarian.get_random_track()
    if track:
        print(f"Random Track Choice: {track['filename']}")
        print(f"Path: {track['path']}")
