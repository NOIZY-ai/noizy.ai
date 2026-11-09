#!/usr/bin/env python3
"""
🌍 GABRIEL ALL LANGUAGES
Framework for all known languages in the world
GORUNFREE Protocol
"""

import json
import sys
from pathlib import Path

class GabrielAllLanguages:
    """Framework for all world languages"""
    
    def __init__(self):
        self.languages_data = self._load_languages()
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'it': 'Italian',
            'fr': 'French',
            'pt': 'Portuguese'
        }
    
    def _load_languages(self):
        """Load world languages data"""
        data_file = Path(__file__).parent / "world_languages.json"
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def get_all_languages(self) -> dict:
        """Get all known languages"""
        if 'world_languages' in self.languages_data:
            return self.languages_data['world_languages'].get('top_50_languages', {})
        return {}
    
    def get_language_families(self) -> dict:
        """Get language families"""
        if 'world_languages' in self.languages_data:
            return self.languages_data['world_languages'].get('language_families', {})
        return {}
    
    def get_language_info(self, lang_code: str) -> dict:
        """Get information about a specific language"""
        all_langs = self.get_all_languages()
        for name, info in all_langs.items():
            if info.get('code') == lang_code:
                return {'name': name, **info}
        return {}
    
    def list_top_languages(self, limit: int = 50) -> list:
        """List top languages by speaker count"""
        all_langs = self.get_all_languages()
        sorted_langs = sorted(
            all_langs.items(),
            key=lambda x: x[1].get('speakers', 0),
            reverse=True
        )
        return sorted_langs[:limit]
    
    def get_languages_by_family(self, family: str) -> list:
        """Get all languages in a language family"""
        all_langs = self.get_all_languages()
        return [
            (name, info) for name, info in all_langs.items()
            if info.get('family') == family
        ]
    
    def get_statistics(self) -> dict:
        """Get language statistics"""
        if 'world_languages' in self.languages_data:
            return {
                'total_known': self.languages_data['world_languages'].get('total_known_languages', 0),
                'major_languages': self.languages_data['world_languages'].get('major_languages', 0),
                'endangered': self.languages_data['world_languages'].get('endangered', 0),
                'extinct': self.languages_data['world_languages'].get('extinct', 0),
                'top_50_count': len(self.get_all_languages())
            }
        return {}

def main():
    gabriel = GabrielAllLanguages()
    
    print("🌍 GABRIEL - ALL WORLD LANGUAGES")
    print("=" * 70)
    
    stats = gabriel.get_statistics()
    print(f"\n📊 World Language Statistics:")
    print(f"  Total known languages: {stats.get('total_known', 0):,}")
    print(f"  Major languages: {stats.get('major_languages', 0)}")
    print(f"  Endangered languages: {stats.get('endangered', 0):,}")
    print(f"  Extinct languages: {stats.get('extinct', 0)}")
    
    print(f"\n🗣️ Top 20 Languages by Speakers:")
    top_langs = gabriel.list_top_languages(20)
    for i, (name, info) in enumerate(top_langs, 1):
        speakers = info.get('speakers', 0)
        code = info.get('code', '')
        family = info.get('family', '')
        print(f"  {i:2d}. {name:20s} ({code:3s}) - {speakers:>12,} speakers - {family}")
    
    print(f"\n🌐 Language Families:")
    families = gabriel.get_language_families()
    for family, count in sorted(families.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {family:20s} - {count} languages")
    
    print(f"\n✅ Currently Trained Languages:")
    for code, name in gabriel.supported_languages.items():
        print(f"  {code}: {name}")
    
    print(f"\n🚀 Framework ready for all {stats.get('total_known', 0):,} languages!")

if __name__ == "__main__":
    main()

