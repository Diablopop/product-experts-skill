# Getting Transcripts

The product-experts skill analyzes full transcripts from Lenny's Podcast. You need to download these transcripts to use the skill.

## Download from Dropbox

Lenny Rachitsky generously makes all his podcast transcripts publicly available via Dropbox.

🔗 **[Download Transcripts](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0)**

## Installation Steps

1. **Visit the Dropbox link** above
2. **Select all files** (or the ones you want)
   - As of February 2026, there are 303 transcript files in the Dropbox
   - Each file is named after the guest expert (e.g., "Elena Verna.txt")
3. **Download to your transcripts directory**
   - The directory you specified during installation
   - Default: `~/Documents/lennys-podcast-transcripts/`
4. **Exclude compilation episodes**
   - **Do not download:** `Interview Q Compilation.txt`
   - This is a compilation episode (not a single expert interview) and creates unusual results
5. **Verify download**
   - You should have **302 transcript files** (303 minus the compilation)
   - Make sure all files are `.txt` format
   - Files should be 30-50 pages each (full transcripts, not summaries)

## File Format

Each transcript file should:
- Be in `.txt` format (plain text)
- Be named after the expert (e.g., "Ada Chen Rekhi.txt")
- Contain the full interview transcript
- Some experts have multiple episodes (e.g., "Elena Verna 4.0.txt")

**Important:** Do not include compilation episodes like "Interview Q Compilation.txt". The skill is designed for single-expert interviews, and compilation episodes produce inconsistent results.

## Verifying Your Download

After downloading, you can verify your setup:

```bash
# Check how many transcripts you have
ls ~/Documents/lennys-podcast-transcripts/*.txt | wc -l
# Should show 302 (not 303 - excludes Interview Q Compilation.txt)

# Compare to what's indexed
python3 ~/.claude/skills/product-experts/index/check-index.py
```

The check script will show if you're missing any transcripts or if you have new ones that aren't indexed yet.

## Keeping Transcripts Updated

Lenny publishes new episodes regularly. To stay current:

1. **Check the Dropbox** periodically for new files
2. **Download new transcripts** to your transcripts directory
3. **Update your index** (see [How to Use](how-to-use.md#keeping-your-index-updated))

## Storage Requirements

- **Space needed:** ~50-100 MB for 302 transcripts
- **Format:** Plain text (.txt files)
- **Location:** Any directory on your computer (you specify this in config.json)

## Alternative: Self-Transcription

If you have a podcast subscription service that provides transcripts, you can use those instead:
- Export transcripts as `.txt` files
- Name them after the guest expert
- Place them in your transcripts directory

The skill works with any podcast transcripts in plain text format, though it's optimized for Lenny's Podcast structure.

## Supporting Lenny

These transcripts represent hundreds of hours of interviews and are Lenny's intellectual property. While he makes them publicly available, please consider:

- **[Subscribe to Lenny's Newsletter](https://www.lennysnewsletter.com/)** - Support his work
- **Share the podcast** - Help others discover it
- **Give credit** - When sharing insights, mention the source

This tool helps you get more value from Lenny's incredible archive. Please support him!

## Troubleshooting

**Problem:** Files won't download from Dropbox
- Try downloading in smaller batches
- Check your internet connection
- Make sure you have enough disk space

**Problem:** Files are in wrong format (PDF, DOCX, etc.)
- Transcripts must be `.txt` format
- If you have other formats, convert them to plain text

**Problem:** Directory path issues
- Use absolute paths in config.json
- Use `~` for your home directory (e.g., `~/Documents/transcripts/`)
- Avoid spaces in directory names, or use quotes if necessary

For more help, see [Troubleshooting](troubleshooting.md).
