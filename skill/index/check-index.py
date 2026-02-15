#!/usr/bin/env python3
"""
Check if the product-experts index is up-to-date with transcript files.

Compares transcript files in your directory against what's indexed and
suggests the best way to update if new transcripts are found.
"""

import json
import os
from pathlib import Path

# Load configuration
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

def load_config():
    """Load configuration from config.json."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: Config file not found: {CONFIG_FILE}")
        print("Please create config.json from config.example.json")
        exit(1)

config = load_config()
transcripts_dir = Path(config['transcripts_directory']).expanduser()
index_file = Path(__file__).parent / 'expert-index.json'

# Check if index exists
if not index_file.exists():
    print("❌ Error: Index file not found")
    print(f"Expected: {index_file}")
    print("\nPlease run build-index.py first to create the index")
    exit(1)

# Load index
try:
    with open(index_file, 'r') as f:
        index_data = json.load(f)

    # Handle both old format (array) and new format (with metadata)
    if isinstance(index_data, dict) and 'metadata' in index_data:
        metadata = index_data['metadata']
        experts = index_data['experts']
    else:
        # Old format - array of experts
        metadata = {
            "last_updated": "Unknown",
            "transcript_count": len(index_data),
            "dropbox_url": "https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0"
        }
        experts = index_data

except json.JSONDecodeError:
    print(f"❌ Error: Could not parse index file: {index_file}")
    exit(1)

# Check if transcripts directory exists
if not transcripts_dir.exists():
    print(f"❌ Error: Transcripts directory not found: {transcripts_dir}")
    print(f"\nPlease download transcripts from:")
    print(f"  {metadata.get('dropbox_url', 'Lenny\\'s Dropbox')}")
    exit(1)

# Get indexed filenames
indexed_files = {expert['filename'] for expert in experts}

# Get actual transcript files
actual_files = {f.name for f in transcripts_dir.glob('*.txt') if f.name != '.DS_Store'}

# Compare
new_files = actual_files - indexed_files
missing_files = indexed_files - actual_files

# Report
print("=" * 70)
print("📊 Index Status")
print("=" * 70)
print(f"Last updated: {metadata.get('last_updated', 'Unknown')}")
print(f"Indexed transcripts: {len(indexed_files)}")
print(f"Files in folder: {len(actual_files)}")
print()

if new_files:
    print(f"⚠️  Found {len(new_files)} new transcript(s) not in index:")
    for f in sorted(new_files):
        print(f"  - {f}")
    print()

    print("=" * 70)
    print("How to Update:")
    print("=" * 70)

    if len(new_files) <= 3:
        print("\n📝 Recommended: Incremental update (FREE)")
        print("   In any Claude Code conversation, say:")
        print()
        print('   "I added new transcripts to my product-experts folder.')
        print('    Can you update the index?"')
        print()
        print("   Claude will read the new transcripts and update the index.")

    else:
        print(f"\n🔄 Recommended: Batch rebuild (~$2-3)")
        print("   You have many new transcripts. Rebuilding the entire index")
        print("   is more efficient:")
        print()
        print("   python3 ~/.claude/skills/product-experts/index/build-index.py")
        print()
        print("   Make sure ANTHROPIC_API_KEY is set in your environment.")

    if len(new_files) <= 3:
        print("\n   Alternative: Batch rebuild")
        print("   python3 ~/.claude/skills/product-experts/index/build-index.py")
    else:
        print("\n   Alternative: Incremental update (free but slower)")
        print('   Ask Claude: "Update the product-experts index"')

    print()

else:
    print("✅ Index is up-to-date!")
    print()

if missing_files:
    print("=" * 70)
    print(f"⚠️  {len(missing_files)} indexed file(s) not found in folder:")
    print("=" * 70)
    for f in sorted(missing_files):
        print(f"  - {f}")
    print()
    print("These transcripts are in your index but missing from your folder.")
    print("Consider downloading them from Lenny's Dropbox:")
    print(f"  {metadata.get('dropbox_url', '')}")
    print()

print("=" * 70)
