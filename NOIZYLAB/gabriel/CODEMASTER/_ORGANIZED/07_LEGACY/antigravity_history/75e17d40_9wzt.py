import json
from datetime import datetime

DB_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/vi_db.json"


SEEDS = [
    # Synths
    {"name": "Serum", "developer": "Xfer Records", "type": "Wavetable Synth"},
    {"name": "Omnisphere 2", "developer": "Spectrasonics", "type": "Power Synth"},
    {"name": "Diva", "developer": "u-he", "type": "Analog Modeling Synth"},
    {"name": "Massive X", "developer": "Native Instruments", "type": "Wavetable Synth"},
    {"name": "Sylenth1", "developer": "LennarDigital", "type": "Subtractive Synth"},
    {"name": "Pigments 5", "developer": "Arturia", "type": "Polychrome Synth"},
    {"name": "Phase Plant", "developer": "Kilohearts", "type": "Modular Synth"},
    {"name": "Vital", "developer": "Matt Tytel", "type": "Wavetable Synth"},
    {"name": "V Collection X", "developer": "Arturia", "type": "Collection"},
    {"name": "Komplete 14", "developer": "Native Instruments", "type": "Collection"},
    {"name": "Falcon 3", "developer": "UVI", "type": "Hybrid Synth"},
    {"name": "Nexus 4", "developer": "reFX", "type": "Rompler"},
    {"name": "Spire", "developer": "Reveal Sound", "type": "Polyphonic Synth"},
    {"name": "Hive 2", "developer": "u-he", "type": "Wavetable/Subtractive"},
    {"name": "Zebra 2", "developer": "u-he", "type": "Modular Synth"},
    {"name": "Repro", "developer": "u-he", "type": "Analog Modeling"},
    {"name": "Juno-60", "developer": "Roland Cloud", "type": "Emulation"},
    {"name": "Jupiter-8", "developer": "Roland Cloud", "type": "Emulation"},
    {"name": "Minimoog V", "developer": "Arturia", "type": "Emulation"},
    {"name": "Prophet-5 V", "developer": "Arturia", "type": "Emulation"},
    
    # Samplers / Keys
    {"name": "Kontakt 7", "developer": "Native Instruments", "type": "Sampler"},
    {"name": "Keyscape", "developer": "Spectrasonics", "type": "Keyboards"},
    {"name": "Trilian", "developer": "Spectrasonics", "type": "Bass Module"},
    {"name": "Superior Drummer 3", "developer": "Toontrack", "type": "Drums"},
    {"name": "Addictive Drums 2", "developer": "XLN Audio", "type": "Drums"},
    {"name": "EZDrummer 3", "developer": "Toontrack", "type": "Drums"},
    {"name": "Battery 4", "developer": "Native Instruments", "type": "Drum Sampler"},
    {"name": "ARCADE", "developer": "Output", "type": "Loop Sampler"},
    {"name": "Serato Sample", "developer": "Serato", "type": "Sampler"},
    {"name": "TAL-Sampler", "developer": "TAL Software", "type": "Vintage Sampler"},
    
    # Effects
    {"name": "Pro-Q 3", "developer": "FabFilter", "type": "EQ"},
    {"name": "Pro-L 2", "developer": "FabFilter", "type": "Limiter"},
    {"name": "Pro-C 2", "developer": "FabFilter", "type": "Compressor"},
    {"name": "Saturn 2", "developer": "FabFilter", "type": "Saturation"},
    {"name": "ValhallaVintageVerb", "developer": "Valhalla DSP", "type": "Reverb"},
    {"name": "ValhallaRoom", "developer": "Valhalla DSP", "type": "Reverb"},
    {"name": "ValhallaShimmer", "developer": "Valhalla DSP", "type": "Reverb"},
    {"name": "RC-20 Retro Color", "developer": "XLN Audio", "type": "Lo-Fi Effect"},
    {"name": "Decapitator", "developer": "Soundtoys", "type": "Saturation"},
    {"name": "EchoBoy", "developer": "Soundtoys", "type": "Delay"},
    {"name": "Little AlterBoy", "developer": "Soundtoys", "type": "Vocal Effect"},
    {"name": "EffectList", "developer": "Soundtoys", "type": "Collection"},
    {"name": "Soothe2", "developer": "Oeksound", "type": "Resonance Suppressor"},
    {"name": "Gullfoss", "developer": "Soundtheory", "type": "Intelligent EQ"},
    {"name": "Ozone 11", "developer": "iZotope", "type": "Mastering Suite"},
    {"name": "Neutron 4", "developer": "iZotope", "type": "Mixing Suite"},
    {"name": "Rx 10", "developer": "iZotope", "type": "Audio Repair"},
    {"name": "Trash 2", "developer": "iZotope", "type": "Distortion"},
    {"name": "Vulf Compressor", "developer": "Goodhertz", "type": "Compressor"},
    {"name": "ShaperBox 3", "developer": "Cableguys", "type": "Multi-Effect"},
    {"name": "Kickstart 2", "developer": "Nicky Romero", "type": "Sidechain"},
    {"name": "LFO Tool", "developer": "Xfer Records", "type": "LFO/Sidechain"},
    {"name": "Endless Smile", "developer": "Dada Life", "type": "Build-up Effect"},
    {"name": "Sausage Fattener", "developer": "Dada Life", "type": "Saturation/Limiter"},
    {"name": "OTT", "developer": "Xfer Records", "type": "Multiband Compressor"},
    {"name": "Portal", "developer": "Output", "type": "Granular FX"},
    {"name": "Thermal", "developer": "Output", "type": "Distortion"},
    {"name": "Movement", "developer": "Output", "type": "Rhythm FX"},
    {"name": "Shadow Hills Class A", "developer": "Plugin Alliance", "type": "Compressor"},
    {"name": "Black Box HG-2", "developer": "Plugin Alliance", "type": "Saturation"},
    {"name": "SSL G-Bus Compressor", "developer": "Waves/Universal Audio", "type": "Compressor"},
    {"name": "1176 Collection", "developer": "Universal Audio", "type": "Compressor"},
    {"name": "LA-2A Collection", "developer": "Universal Audio", "type": "Compressor"},
    {"name": "Pultec EQ Collection", "developer": "Universal Audio", "type": "EQ"},
    {"name": "Auto-Tune Pro", "developer": "Antares", "type": "Pitch Correction"},
    {"name": "Melodyne 5", "developer": "Celemony", "type": "Pitch Correction"},
    {"name": "VocAlign Ultra", "developer": "Synchro Arts", "type": "Alignment"},
]

def seed_db():
    print(f"🌱 Seeding Database with {len(SEEDS)} entries...")
    
    current_data = {"metadata": {"last_updated": str(datetime.now().date())}, "instruments": []}
    
    # Load existing if any
    try:
        with open(DB_PATH, 'r') as f:
            exist = json.load(f)
            if 'instruments' in exist:
                current_data['instruments'] = exist['instruments']
    except:
        pass
        
    # Add Seeds (Avoid duplicates by name)
    existing_names = {i['name'].lower() for i in current_data['instruments']}
    
    count = len(current_data['instruments'])
    added = 0
    
    for item in SEEDS:
        if item['name'].lower() in existing_names:
            continue
            
        count += 1
        item['id'] = f"vi_{count:03d}"
        item['release_date'] = "Unknown"
        item['added_at'] = str(datetime.now())
        
        current_data['instruments'].append(item)
        added += 1
        
    # Save
    with open(DB_PATH, 'w') as f:
        json.dump(current_data, f, indent=2)
        
    print(f"✅ Database Seeded! Added {added} new instruments.")
    print(f"Total: {len(current_data['instruments'])} entries.")

if __name__ == "__main__":
    seed_db()
