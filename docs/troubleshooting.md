# Troubleshooting

Common issues and solutions for the product-experts skill.

## Installation Issues

### "Config file not found"

**Error:**
```
❌ Error: Config file not found: ~/.claude/skills/product-experts/config.json
```

**Solution:**
1. Check if `config.example.json` exists:
   ```bash
   ls ~/.claude/skills/product-experts/config.example.json
   ```
2. Copy it to `config.json`:
   ```bash
   cp ~/.claude/skills/product-experts/config.example.json \
      ~/.claude/skills/product-experts/config.json
   ```
3. Edit `config.json` with your actual paths:
   ```bash
   nano ~/.claude/skills/product-experts/config.json
   ```

### "Transcripts directory not found"

**Error:**
```
❌ Error: Transcripts directory not found: ~/Documents/lennys-podcast-transcripts
```

**Solution:**
1. Check your config.json path:
   ```bash
   cat ~/.claude/skills/product-experts/config.json
   ```
2. Make sure the directory exists:
   ```bash
   mkdir -p ~/Documents/lennys-podcast-transcripts
   ```
3. Download transcripts from [Lenny's Dropbox](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0)
   - **Important:** Do not download `Interview Q Compilation.txt` (compilation episode)

### "Permission denied" when running scripts

**Error:**
```
-bash: ./build-index.py: Permission denied
```

**Solution:**
Make the scripts executable:
```bash
chmod +x ~/.claude/skills/product-experts/index/build-index.py
chmod +x ~/.claude/skills/product-experts/index/check-index.py
```

## Skill Usage Issues

### Skill not appearing when typing `/product-experts`

**Possible causes:**

1. **Skill not installed in correct location**
   - Check: `ls ~/.claude/skills/product-experts/SKILL.md`
   - Should exist and contain skill definition

2. **Skill directory not named correctly**
   - Should be: `~/.claude/skills/product-experts/`
   - Not: `~/.claude/skills/product-experts-skill/`

3. **SKILL.md has syntax errors**
   - Check the frontmatter (YAML header)
   - Must have `---` at start and end
   - Must include `name:` and `description:`

**Solution:**
Reinstall using the installation script:
```bash
cd /path/to/product-experts-skill
./install.sh
```

### "No experts found matching your question"

**Possible causes:**
1. Index files are empty or corrupted
2. Question is too vague or uses non-PM terminology

**Solution:**
1. Check index exists and has content:
   ```bash
   wc -l ~/.claude/skills/product-experts/index/expert-index.json
   # Should show thousands of lines
   ```
2. If empty, rebuild:
   ```bash
   python3 ~/.claude/skills/product-experts/index/build-index.py
   ```
3. Make question more specific using PM terminology

### Expert analysis is taking too long (>5 minutes)

**Possible causes:**
1. Subagents running sequentially instead of in parallel
2. Very large transcript files
3. API rate limiting

**What's happening:**
Check the timestamps on expert files:
```bash
ls -lt ~/Documents/product-experts-outputs/[latest-folder]/experts/
```

If timestamps are minutes apart, they ran sequentially (this is a bug in the skill execution).

**Solution:**
This is expected to be 2-3 minutes. If it's taking >5 minutes:
- Wait for it to complete (it will finish)
- Report issue at: https://github.com/andrewschauer/product-experts-skill/issues

## Index Issues

### "Index is out of date"

**Message:**
```
⚠️ Found 5 new transcript(s) not in index
```

**Solution:**
See [How to Use - Keeping Your Index Updated](how-to-use.md#keeping-your-index-updated)

For 1-3 transcripts:
```
Ask Claude: "Update my product-experts index for these new transcripts"
```

For 10+ transcripts:
```bash
python3 ~/.claude/skills/product-experts/index/build-index.py
```

### "Indexed files not found in folder"

**Message:**
```
⚠️ 10 indexed file(s) not found in folder
```

**Meaning:**
Your index references transcripts that aren't in your directory.

**Solution:**
1. Download missing transcripts from [Lenny's Dropbox](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0)
2. Or rebuild index to match your current files:
   ```bash
   python3 ~/.claude/skills/product-experts/index/build-index.py
   ```

### Build-index.py fails with API errors

**Error:**
```
Error: API key not found
```

**Solution:**
Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Add to your `~/.bashrc` or `~/.zshrc` to persist:
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
```

## Output Issues

### Output files are empty or incomplete

**Possible causes:**
1. Subagent crashed during analysis
2. Transcript file is corrupted
3. Disk space issue

**Solution:**
1. Check disk space:
   ```bash
   df -h ~/Documents/product-experts-outputs/
   ```
2. Check if transcript files are readable:
   ```bash
   head -20 ~/Documents/lennys-podcast-transcripts/[expert-name].txt
   ```
3. Try running the skill again

### Can't find output files

**Check output directory configuration:**
```bash
cat ~/.claude/skills/product-experts/config.json
```

**Find recent outputs:**
```bash
ls -lt ~/Documents/product-experts-outputs/ | head -10
```

**Outputs are named with timestamps:**
- Format: `YYYY-MM-DD-HH-MM-[topic-slug]/`
- Example: `2026-02-12-15-18-pm-job-hunting-getting-noticed/`

## Path and Configuration Issues

### Tilde (~) not expanding in paths

**Error:**
```
Directory not found: ~/Documents/transcripts
```

**Solution:**
The config.json should use `~` for home directory, which Python will expand.

If issues persist, use absolute paths:
```json
{
  "transcripts_directory": "/Users/yourname/Documents/lennys-podcast-transcripts",
  "output_directory": "/Users/yourname/Documents/product-experts-outputs"
}
```

### Spaces in directory paths

**Problem:**
Paths with spaces can cause issues in some contexts.

**Solution:**
1. Avoid spaces in directory names (use hyphens or underscores)
2. Or use quotes in config.json:
   ```json
   "transcripts_directory": "~/Documents/Lenny's Transcripts"
   ```

## Python Issues

### "Python not found" or "python3: command not found"

**Solution:**
Install Python 3.9 or higher:

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get install python3
```

Check version:
```bash
python3 --version
# Should show 3.9 or higher
```

### "Module not found: anthropic"

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
Install the Anthropic SDK:
```bash
pip3 install anthropic
```

## Getting Help

If you've tried the solutions above and still have issues:

1. **Check existing issues:**
   - https://github.com/andrewschauer/product-experts-skill/issues

2. **Create a new issue:**
   - Include error messages (full text)
   - Include your config.json (remove any sensitive paths)
   - Include output of:
     ```bash
     python3 --version
     ls -la ~/.claude/skills/product-experts/
     cat ~/.claude/skills/product-experts/config.json
     ```

3. **Discussion forum:**
   - https://github.com/andrewschauer/product-experts-skill/discussions

## Common Questions

**Q: Can I use this with other podcasts?**
A: Yes! The skill works with any podcast transcripts. Just:
1. Export transcripts as `.txt` files
2. Name them after the guest
3. Rebuild the index

**Q: How much does it cost to use?**
A: The skill itself is free with Claude Code. Rebuilding the index costs ~$2-3 if you use the batch method.

**Q: Can I run this without internet?**
A: No, the skill requires Claude Code which needs internet. The index building script also uses the Anthropic API.

**Q: Why are some experts selected over others?**
A: The skill scores experts based on keyword overlap with your question. More specific questions get better expert matches.

**Q: Can I manually choose which experts to consult?**
A: Not currently. The skill automatically selects the 5 most relevant experts. You can influence selection by being specific in your question.
