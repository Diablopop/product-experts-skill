#!/usr/bin/env python3
"""
Build searchable index from Lenny's podcast transcripts.

This script processes all transcript files in the specified directory,
extracts expert metadata from the introductions using Claude API,
and generates two JSON index files for efficient expert search.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic

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
TRANSCRIPTS_DIR = os.path.expanduser(config['transcripts_directory'])
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPERT_INDEX_FILE = os.path.join(OUTPUT_DIR, "expert-index.json")
TOPICS_INDEX_FILE = os.path.join(OUTPUT_DIR, "topics-index.json")

# Dropbox link to Lenny's transcripts
DROPBOX_URL = "https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0"

# Number of lines to read from each transcript (captures intro section)
INTRO_LINES = 150


def extract_episode_version(filename):
    """Extract episode version from filename (e.g., '4.0' from 'Elena Verna 4.0.txt')."""
    match = re.search(r'(\d+\.\d+)\.txt$', filename)
    return match.group(1) if match else None


def get_expert_name_from_filename(filename):
    """Extract expert name from filename, removing .txt and version numbers."""
    name = filename.replace('.txt', '')
    # Remove version numbers like '4.0'
    name = re.sub(r'\s+\d+\.\d+$', '', name)
    return name


def read_transcript_intro(filepath, num_lines=INTRO_LINES):
    """Read the first num_lines from a transcript file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= num_lines:
                    break
                lines.append(line)
            return ''.join(lines)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def extract_metadata_with_claude(intro_text, filename):
    """Use Claude API to extract expert metadata from transcript intro."""
    client = Anthropic()

    expert_name = get_expert_name_from_filename(filename)

    prompt = f"""Analyze this podcast transcript introduction and extract structured metadata about the guest expert.

Transcript intro:
{intro_text}

Extract the following information in JSON format:
- bio: A concise 2-3 sentence biography highlighting their main accomplishments and expertise
- companies: Array of company names they've worked at (mentioned in the intro)
- roles: Array of job titles/roles (e.g., "CEO", "VP of Product", "Head of Growth")
- expertise: Array of 5-10 keyword expertise areas (e.g., "growth", "pricing", "PLG", "onboarding")
- topics: Array of 5-10 specific topics covered in this episode

Return ONLY valid JSON in this exact format:
{{
  "bio": "...",
  "companies": ["...", "..."],
  "roles": ["...", "..."],
  "expertise": ["...", "...", "..."],
  "topics": ["...", "...", "..."]
}}

Be specific and extract actual content from the text. Focus on product management, growth, and business topics."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text)

        metadata = json.loads(response_text)
        return metadata
    except Exception as e:
        print(f"Error extracting metadata for {filename}: {e}")
        return None


def build_expert_index():
    """Build the expert index from all transcripts."""
    transcripts_path = Path(TRANSCRIPTS_DIR)
    transcript_files = sorted([f for f in transcripts_path.glob("*.txt") if f.name != ".DS_Store"])

    total_files = len(transcript_files)
    print(f"Found {total_files} transcript files")
    print(f"Processing transcripts and extracting metadata...\n")

    expert_index = []

    for idx, transcript_file in enumerate(transcript_files, 1):
        filename = transcript_file.name
        print(f"[{idx}/{total_files}] Processing: {filename}")

        # Read intro section
        intro_text = read_transcript_intro(transcript_file)
        if not intro_text:
            print(f"  ⚠️  Skipped (could not read file)\n")
            continue

        # Extract metadata using Claude
        metadata = extract_metadata_with_claude(intro_text, filename)
        if not metadata:
            print(f"  ⚠️  Skipped (metadata extraction failed)\n")
            continue

        # Build expert entry
        expert_entry = {
            "name": get_expert_name_from_filename(filename),
            "filename": filename,
            "bio": metadata.get("bio", ""),
            "companies": metadata.get("companies", []),
            "roles": metadata.get("roles", []),
            "expertise": metadata.get("expertise", []),
            "topics": metadata.get("topics", []),
            "episode_version": extract_episode_version(filename)
        }

        expert_index.append(expert_entry)
        print(f"  ✓ Extracted: {len(metadata.get('expertise', []))} expertise areas, {len(metadata.get('topics', []))} topics\n")

    return expert_index


def build_topics_index(expert_index):
    """Build reverse index mapping topics to expert names."""
    topics_map = {}

    for expert in expert_index:
        expert_name = expert["name"]

        # Add from expertise keywords
        for keyword in expert.get("expertise", []):
            keyword_lower = keyword.lower()
            if keyword_lower not in topics_map:
                topics_map[keyword_lower] = []
            if expert_name not in topics_map[keyword_lower]:
                topics_map[keyword_lower].append(expert_name)

        # Add from topics
        for topic in expert.get("topics", []):
            topic_lower = topic.lower()
            if topic_lower not in topics_map:
                topics_map[topic_lower] = []
            if expert_name not in topics_map[topic_lower]:
                topics_map[topic_lower].append(expert_name)

    return topics_map


def save_indexes(expert_index, topics_index):
    """Save both indexes to JSON files with metadata."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Create metadata
    metadata = {
        "last_updated": today,
        "transcript_count": len(expert_index),
        "source": "Lenny's Podcast",
        "dropbox_url": DROPBOX_URL,
        "generated_by": "build-index.py v1.0"
    }

    # Save expert index with metadata
    expert_output = {
        "metadata": metadata,
        "experts": expert_index
    }

    with open(EXPERT_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(expert_output, f, indent=2, ensure_ascii=False)

    expert_index_size = os.path.getsize(EXPERT_INDEX_FILE) / 1024
    print(f"✓ Expert index saved: {EXPERT_INDEX_FILE}")
    print(f"  Size: {expert_index_size:.1f} KB")
    print(f"  Experts: {len(expert_index)}\n")

    # Save topics index with metadata
    topics_output = {
        "metadata": metadata,
        "topics": topics_index
    }

    with open(TOPICS_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(topics_output, f, indent=2, ensure_ascii=False)

    topics_index_size = os.path.getsize(TOPICS_INDEX_FILE) / 1024
    print(f"✓ Topics index saved: {TOPICS_INDEX_FILE}")
    print(f"  Size: {topics_index_size:.1f} KB")
    print(f"  Topics: {len(topics_index)}\n")


def main():
    """Main execution function."""
    print("=" * 70)
    print("Building Product Experts Index")
    print("=" * 70)
    print()

    # Check if transcripts directory exists
    if not os.path.exists(TRANSCRIPTS_DIR):
        print(f"❌ Error: Transcripts directory not found: {TRANSCRIPTS_DIR}")
        print(f"Please download transcripts from: {DROPBOX_URL}")
        return

    # Build expert index
    expert_index = build_expert_index()

    if not expert_index:
        print("❌ No experts indexed. Exiting.")
        return

    print("=" * 70)
    print(f"Building topics index from {len(expert_index)} experts...")
    print("=" * 70)
    print()

    # Build topics index
    topics_index = build_topics_index(expert_index)

    # Save both indexes
    print("=" * 70)
    print("Saving indexes...")
    print("=" * 70)
    print()
    save_indexes(expert_index, topics_index)

    print("=" * 70)
    print("✓ Index build complete!")
    print("=" * 70)
    print()
    print(f"Total experts indexed: {len(expert_index)}")
    print(f"Total topics mapped: {len(topics_index)}")
    print()
    print("Next steps:")
    print("1. Review a few expert entries in expert-index.json")
    print("2. Check topics-index.json for topic coverage")
    print("3. The product-experts skill is ready to use!")


if __name__ == "__main__":
    main()
