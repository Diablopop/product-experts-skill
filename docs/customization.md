# Customization

Advanced configuration options for the product-experts skill.

## Configuration File

The skill uses `~/.claude/skills/product-experts/config.json` for all path configuration.

### Default Configuration

```json
{
  "transcripts_directory": "~/Documents/lennys-podcast-transcripts",
  "output_directory": "~/Documents/product-experts-outputs",
  "skill_directory": "~/.claude/skills/product-experts"
}
```

### Customizing Directories

Edit `~/.claude/skills/product-experts/config.json`:

```bash
nano ~/.claude/skills/product-experts/config.json
```

**Examples:**

Store transcripts on external drive:
```json
{
  "transcripts_directory": "/Volumes/External/lennys-podcasts"
}
```

Use Dropbox for outputs (auto-sync across devices):
```json
{
  "output_directory": "~/Dropbox/product-expert-advice"
}
```

Use absolute paths:
```json
{
  "transcripts_directory": "/Users/andrew/Documents/transcripts",
  "output_directory": "/Users/andrew/Documents/outputs"
}
```

## Modifying Expert Selection Algorithm

The expert selection logic is in `SKILL.md`. To customize:

### Change Scoring Weights

Edit `~/.claude/skills/product-experts/SKILL.md`, find Step 3:

**Default weights:**
```markdown
- **Keyword overlap** with expertise areas (weight: 3x)
- **Topic relevance** (weight: 2x)
- **Diversity bonus** (prefer varied backgrounds/perspectives)
```

**Customize:**
- Increase topic weight (4x) if you care more about recent episode topics
- Increase expertise weight (5x) if you want deep domain experts
- Add company weight if you want experts from specific company backgrounds

### Change Number of Experts

**Default:** 5 experts

To consult more or fewer experts, edit SKILL.md:
- Change "Select top 5" to "Select top 3" or "Select top 7"
- Update all references to 5 throughout the file
- Note: More experts = longer analysis time and more reading

**Tradeoffs:**
- **3 experts:** Faster (~1-2 min), less diverse perspectives
- **5 experts:** Balanced (default)
- **7 experts:** Slower (~3-4 min), more comprehensive but redundant

## Modifying Index Building

### Customize Metadata Extraction

Edit `~/.claude/skills/product-experts/index/build-index.py`:

**Change intro length analyzed:**
```python
# Default: First 150 lines
INTRO_LINES = 150

# For shorter intros:
INTRO_LINES = 100

# For more context:
INTRO_LINES = 200
```

**Customize metadata fields:**

Find the `extract_metadata_with_claude()` function and modify the prompt:

```python
prompt = f"""Analyze this podcast transcript introduction...

Extract the following information in JSON format:
- bio: ...
- companies: ...
- roles: ...
- expertise: ...
- topics: ...
- industry: ...  # ADD NEW FIELD
- location: ...  # ADD NEW FIELD
```

Then update the `expert_entry` dict to include new fields.

### Change Model for Indexing

**Default:** `claude-haiku-4-5-20251001` (fastest, cheapest)

For potentially better metadata extraction:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",  # More capable
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```

**Tradeoffs:**
- Haiku: Fast, cheap (~$0.50 for 300 transcripts)
- Sonnet: Slower, better, pricier (~$2-3 for 300 transcripts)

## Customizing Output Format

### Modify Expert Response Template

Edit `~/.claude/skills/product-experts/templates/expert-analysis.md`:

**Add sections:**
```markdown
## Potential Risks or Concerns
[What could go wrong with this advice?]

## Related Resources
[Links, books, or tools this expert mentioned]

## Follow-up Questions
[Questions to explore this topic deeper]
```

**Remove sections:**
Delete any section you don't find useful.

### Modify Summary Template

Edit `~/.claude/skills/product-experts/templates/summary-template.md`:

**Add sections:**
```markdown
## Quick Reference
[One-page summary of all advice]

## Expert Consensus Score
[How much did experts agree? 1-10 scale]

## Recommended Reading
[Books or articles mentioned across experts]
```

## Advanced: Using with Other Podcasts

The skill can work with transcripts from any podcast.

### Adapting to Different Podcasts

1. **Download transcripts** from your podcast of choice
2. **Format as .txt files** named after the guest
3. **Adjust intro length** in `build-index.py`:
   ```python
   # Some podcasts have longer/shorter intros
   INTRO_LINES = 100  # or 200, depending on podcast
   ```
4. **Rebuild index:**
   ```bash
   python3 ~/.claude/skills/product-experts/index/build-index.py
   ```
5. **Update SKILL.md** references:
   - Change "Lenny's Podcast" to your podcast name
   - Update skill description

### Multi-Podcast Support

To maintain indexes for multiple podcasts:

**Option 1: Separate installations**
```
~/.claude/skills/product-experts-lenny/
~/.claude/skills/product-experts-ycombinator/
~/.claude/skills/product-experts-acquired/
```

Each with its own config, transcripts, and index.

**Option 2: Combined index**
- Put all transcripts in one folder
- Add a `podcast` field to the index
- Filter by podcast in the skill logic

## Customizing Check Script

Edit `~/.claude/skills/product-experts/index/check-index.py`:

**Change thresholds for update recommendations:**

```python
# Default: 1-3 transcripts → incremental, 4+ → batch
if len(new_files) <= 3:
    print("Recommended: Incremental update")
else:
    print("Recommended: Batch rebuild")
```

Change to:
```python
if len(new_files) <= 5:  # More lenient
    ...
```

**Add automatic index update:**

Add to the end of the script:
```python
if new_files and len(new_files) <= 2:
    print("\nAutomatically updating index...")
    # Call incremental update logic here
```

## Output Directory Customization

### Change Timestamp Format

Edit `SKILL.md`, find Step 4:

**Default:** `YYYY-MM-DD-HH-MM`

Change to:
```markdown
- **Timestamp format:** `YYYY-MM-DD-HH-MM-SS`
- **Timestamp format:** `YYYYMMDD-HHMM`
- **Timestamp format:** `YYYY-MM-DD`
```

### Change Folder Naming

**Default:** `[timestamp]-[slug]/`

Change to:
```markdown
- **Path:** `[slug]-[timestamp]/`  # slug first
- **Path:** `[timestamp]/`  # just timestamp
- **Path:** `sessions/[timestamp]-[slug]/`  # add prefix
```

### Organize by Topic

Modify the output path logic to create topic-based folders:

```markdown
**Path:** `[output_directory]/[main-topic]/[timestamp]-[slug]/`

Examples:
- growth/2026-02-12-15-18-plg-pricing/
- hiring/2026-02-12-15-18-pm-job-hunting/
- strategy/2026-02-12-15-18-okr-frameworks/
```

## Performance Optimization

### Reduce Analysis Time

**Option 1: Use Haiku for expert analysis**

In SKILL.md, find the subagent prompt and add:
```
Use model: haiku
```

Tradeoff: Faster but potentially less nuanced advice.

**Option 2: Analyze less of each transcript**

The subagents read full transcripts (30-50 pages). To speed up:
- Modify subagent prompt to read only first 50% of transcript
- Trade depth for speed

**Option 3: Reduce number of experts**

Consult 3 experts instead of 5:
- 40% faster
- Still provides good coverage

### Optimize Index Size

If index files are large and slow to load:

**Reduce metadata verbosity:**
- Shorten bio to 1 sentence instead of 2-3
- Limit topics to top 5 instead of 10
- Remove less useful fields

**Split index by topic area:**
- Create separate indexes: growth-experts.json, pricing-experts.json
- Load only relevant index based on question keywords
- Faster search, more complex logic

## Integration with Other Tools

### Export to Notion

Create a script to convert markdown outputs to Notion pages:
```bash
# After consultation, sync to Notion
python3 ~/scripts/sync-to-notion.py \
  ~/Documents/product-experts-outputs/[latest]/
```

### Email Summaries

Add a post-processing hook to email yourself summaries:
```bash
# Add to end of SKILL.md workflow
cat [summary-file] | mail -s "Expert Advice: [topic]" you@example.com
```

### Integration with Personal Knowledge Base

Symlink outputs to your knowledge base:
```bash
ln -s ~/Documents/product-experts-outputs ~/Obsidian/Vault/Expert-Advice
```

Now outputs appear in your Obsidian vault automatically.

## Debugging and Development

### Enable Verbose Logging

Add to `build-index.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Expert Selection

Create a test script:
```python
#!/usr/bin/env python3
import json

# Load index
with open('expert-index.json', 'r') as f:
    data = json.load(f)
    experts = data['experts']

# Test scoring for a question
question = "how do I improve activation?"
keywords = ['activation', 'improve', 'onboarding']

for expert in experts:
    score = 0
    for keyword in keywords:
        if keyword in str(expert['expertise']).lower():
            score += 3
        if keyword in str(expert['topics']).lower():
            score += 2

    if score > 0:
        print(f"{expert['name']}: {score}")
```

Run:
```bash
python3 test-scoring.py | sort -t: -k2 -rn | head -10
```

Shows top-scoring experts for your test question.

## Best Practices

1. **Back up your index** before rebuilding:
   ```bash
   cp expert-index.json expert-index.backup.json
   ```

2. **Test changes on a copy** before modifying the installed skill:
   ```bash
   cp -r ~/.claude/skills/product-experts \
         ~/.claude/skills/product-experts-test
   ```

3. **Document your customizations** in a CUSTOMIZATIONS.md file

4. **Version your changes** with git if you make significant modifications

5. **Share useful customizations** via GitHub issues or discussions

## Getting Help with Customization

- **GitHub Discussions:** https://github.com/andrewschauer/product-experts-skill/discussions
- **Open an issue:** https://github.com/andrewschauer/product-experts-skill/issues
- **See examples:** Check the `examples/` folder for sample customizations
