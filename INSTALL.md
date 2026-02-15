# Installation Guide

Detailed step-by-step installation instructions for the product-experts skill.

## Prerequisites

Before installing, make sure you have:

- **Python 3.9 or higher**
  ```bash
  python3 --version
  # Should show 3.9.0 or higher
  ```

- **Claude Code** (VSCode extension)
  - Download from: https://www.anthropic.com/claude-code
  - Make sure it's installed and authenticated

- **~5 GB disk space**
  - 50-100 MB for transcripts
  - Rest for Claude Code and dependencies

## Quick Install (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/andrewschauer/product-experts-skill.git
cd product-experts-skill
```

### 2. Run the Installer

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Check Python version
- Install required dependencies
- Prompt you for configuration (transcript and output directories)
- Copy skill files to `~/.claude/skills/product-experts/`
- Create your config file

### 3. Download Transcripts

Visit Lenny's Dropbox and download all transcript files:

🔗 **[Download Transcripts](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0)**

**Important:** Do not download `Interview Q Compilation.txt` (compilation episode that produces inconsistent results).

Save them to the transcripts directory you specified during installation.

### 4. Verify Installation

```bash
# Check skill files are in place
ls ~/.claude/skills/product-experts/SKILL.md

# Check config was created
cat ~/.claude/skills/product-experts/config.json

# Verify transcripts downloaded
ls ~/Documents/lennys-podcast-transcripts/*.txt | wc -l
# Should show 302 files (excludes Interview Q Compilation.txt)
```

### 5. Test the Skill

Open Claude Code and type:
```
/product-experts
```

You should see:
```
I'll consult 5 product experts from Lenny's podcast to help with your challenge.

What product management question or challenge do you need advice on?
```

✅ **You're ready to go!**

---

## Manual Installation

If the installer script doesn't work or you prefer manual installation:

### 1. Install Python Dependencies

```bash
pip3 install anthropic
```

### 2. Create Skill Directory

```bash
mkdir -p ~/.claude/skills/product-experts/index
mkdir -p ~/.claude/skills/product-experts/templates
```

### 3. Copy Skill Files

From the cloned repository:

```bash
# Copy main skill file
cp skill/SKILL.md ~/.claude/skills/product-experts/

# Copy index files
cp skill/index/*.py ~/.claude/skills/product-experts/index/
cp skill/index/*.json ~/.claude/skills/product-experts/index/

# Copy templates
cp skill/templates/* ~/.claude/skills/product-experts/templates/

# Make scripts executable
chmod +x ~/.claude/skills/product-experts/index/*.py
```

### 4. Create Configuration

```bash
# Copy example config
cp config.example.json ~/.claude/skills/product-experts/config.json

# Edit with your paths
nano ~/.claude/skills/product-experts/config.json
```

Edit the file to include your actual paths:

```json
{
  "transcripts_directory": "~/Documents/lennys-podcast-transcripts",
  "output_directory": "~/Documents/product-experts-outputs",
  "skill_directory": "~/.claude/skills/product-experts"
}
```

### 5. Create Directories

```bash
# Create transcripts directory
mkdir -p ~/Documents/lennys-podcast-transcripts

# Create outputs directory
mkdir -p ~/Documents/product-experts-outputs
```

### 6. Download Transcripts

Visit [Lenny's Dropbox](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0) and download all `.txt` files to `~/Documents/lennys-podcast-transcripts/`.

### 7. Verify Installation

```bash
# Check directory structure
ls -la ~/.claude/skills/product-experts/

# Should show:
# - SKILL.md
# - config.json
# - index/ (with .py and .json files)
# - templates/ (with .md files)

# Check transcripts
ls ~/Documents/lennys-podcast-transcripts/*.txt | wc -l
# Should show 302
```

---

## Installation Locations

### Default Directory Structure

```
~/.claude/skills/product-experts/
├── SKILL.md                           # Skill definition
├── config.json                        # Your configuration
├── index/
│   ├── expert-index.json             # Pre-built index (302 experts)
│   ├── topics-index.json             # Pre-built topics index
│   ├── build-index.py                # Rebuild index script
│   └── check-index.py                # Check index freshness
└── templates/
    ├── expert-analysis.md            # Expert response template
    └── summary-template.md           # Synthesis template

~/Documents/lennys-podcast-transcripts/
└── [Expert Name].txt                 # 302 transcript files

~/Documents/product-experts-outputs/
└── [timestamp]-[topic-slug]/         # Output from consultations
    ├── summary.md
    └── experts/
        └── [expert-name].md
```

### Customizing Locations

You can use different directories by editing `config.json`:

```json
{
  "transcripts_directory": "/path/to/your/transcripts",
  "output_directory": "/path/to/your/outputs",
  "skill_directory": "~/.claude/skills/product-experts"
}
```

**Note:** Use `~` for home directory or absolute paths. Avoid spaces in directory names.

---

## Platform-Specific Instructions

### macOS

Default installation should work smoothly. If you don't have Python 3:

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Verify
python3 --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# Fedora/RHEL
sudo dnf install python3 python3-pip

# Verify
python3 --version
```

Then follow the installation steps above.

### Windows (WSL)

This skill works best in WSL (Windows Subsystem for Linux):

1. Install WSL: https://docs.microsoft.com/en-us/windows/wsl/install
2. Install Ubuntu from Microsoft Store
3. Follow Linux installation instructions above

**Note:** Claude Code should also be running in WSL mode.

---

## Troubleshooting Installation

### "Python not found"

**Solution:**
```bash
# Check if Python 3 is installed
which python3

# If not found, install it (see Platform-Specific Instructions)
```

### "Permission denied" errors

**Solution:**
```bash
# Make sure you have write permissions
mkdir -p ~/.claude/skills/
ls -la ~/.claude/

# If permission issues persist, check ownership
sudo chown -R $USER ~/.claude/
```

### "Skill not appearing in Claude Code"

**Checklist:**
1. File is named exactly `SKILL.md` (case-sensitive)
2. Located at `~/.claude/skills/product-experts/SKILL.md`
3. Has valid YAML frontmatter (between `---` markers)
4. Restart Claude Code after installation

**Verify:**
```bash
# Check file location and name
ls -la ~/.claude/skills/product-experts/SKILL.md

# Check frontmatter syntax
head -10 ~/.claude/skills/product-experts/SKILL.md
```

### "Config file not found" when using skill

**Solution:**
```bash
# Make sure config.json exists
ls ~/.claude/skills/product-experts/config.json

# If not, copy from example
cp ~/.claude/skills/product-experts/config.example.json \
   ~/.claude/skills/product-experts/config.json

# Edit with your paths
nano ~/.claude/skills/product-experts/config.json
```

### "Transcripts directory not found"

**Solution:**
```bash
# Check directory exists
ls ~/Documents/lennys-podcast-transcripts/

# If not, create it
mkdir -p ~/Documents/lennys-podcast-transcripts/

# Download transcripts from Dropbox
# Then verify:
ls ~/Documents/lennys-podcast-transcripts/*.txt | wc -l
```

---

## Updating the Skill

To update to a newer version:

### 1. Backup Your Configuration

```bash
cp ~/.claude/skills/product-experts/config.json ~/config.backup.json
```

### 2. Pull Latest Changes

```bash
cd /path/to/product-experts-skill
git pull origin main
```

### 3. Reinstall

```bash
./install.sh
```

Your config and transcripts won't be affected.

### 4. Restore Configuration (if needed)

```bash
cp ~/config.backup.json ~/.claude/skills/product-experts/config.json
```

---

## Uninstalling

To completely remove the skill:

```bash
# Remove skill files
rm -rf ~/.claude/skills/product-experts/

# Remove transcripts (optional)
rm -rf ~/Documents/lennys-podcast-transcripts/

# Remove outputs (optional)
rm -rf ~/Documents/product-experts-outputs/

# Uninstall Python dependency (optional)
pip3 uninstall anthropic
```

---

## Next Steps

After successful installation:

1. **[How to Use](docs/how-to-use.md)** - Learn how to use the skill
2. **[Getting Transcripts](docs/getting-transcripts.md)** - Keep transcripts updated
3. **[Customization](docs/customization.md)** - Advanced configuration options
4. **Try your first consultation:**
   ```
   /product-experts
   ```

---

## Getting Help

If you run into issues:

1. **Check:** [Troubleshooting Guide](docs/troubleshooting.md)
2. **Search:** [GitHub Issues](https://github.com/andrewschauer/product-experts-skill/issues)
3. **Ask:** [GitHub Discussions](https://github.com/andrewschauer/product-experts-skill/discussions)
4. **Report a bug:** [New Issue](https://github.com/andrewschauer/product-experts-skill/issues/new)
