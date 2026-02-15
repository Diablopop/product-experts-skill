# Product Experts Skill for Claude Code

> Get personalized advice from a panel of 5 product management experts by analyzing Lenny's Podcast transcripts.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What This Does

Ask any product management question and get advice from 5 relevant experts:

1. **Smart expert selection** - Analyzes 302 PM experts from Lenny's Podcast and selects the 5 most relevant
2. **Deep analysis** - Reads full interview transcripts (not summaries) to extract insights
3. **Personalized advice** - Generates responses from each expert's unique perspective
4. **Actionable synthesis** - Combines insights into a clear summary with citations

**Example:**
```
You: "How do I get noticed when hunting for PM jobs?"

Skill selects: Phyl Terry, Jackie Bavaro, Lauren Ipsen, Hari Srinivasan, Gergely Orosz
       ↓
Analyzes their full interviews in parallel
       ↓
Generates personalized advice from each expert
       ↓
Creates synthesis with common themes, divergent views, and actionable takeaways
```

## Features

- 🎯 Searches 302 product management experts from Lenny's Podcast
- 📊 Analyzes full transcripts (30-50 pages each) for deep insights
- 🔍 Includes direct quotes with timestamps for verification
- 📝 Generates markdown files for easy reference and sharing
- ⚡ Runs 5 expert analyses in parallel (~2-3 minutes total)
- 🔄 Easy to update with new podcast episodes

## Requirements

- Python 3.9+
- [Claude Code](https://www.anthropic.com/claude-code) (VSCode extension)
- Podcast transcripts in .txt format (see [Getting Transcripts](#getting-transcripts))

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/andrewschauer/product-experts-skill.git
cd product-experts-skill
```

### 2. Run Installation Script

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Check prerequisites (Python 3.9+)
- Install Python dependencies
- Prompt for configuration (transcript location, output location)
- Copy skill files to `~/.claude/skills/product-experts/`
- You're ready to use it!

### 3. Get Transcripts

Download Lenny's podcast transcripts from his public Dropbox:

🔗 **[Download Transcripts](https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0)**

Save all `.txt` files to the transcripts directory you specified during installation.

**Note:** Exclude `Interview Q Compilation.txt` (compilation episode, not a single expert interview).

### 4. Use the Skill

In Claude Code, type:
```
/product-experts
```

Then ask your question!

## Example Output

See [examples/sample-output/](examples/sample-output/) for complete example output.

## Keeping Your Index Updated

Lenny publishes new episodes regularly. To check for new transcripts:

```bash
python3 ~/.claude/skills/product-experts/check-index.py
```

This shows which transcripts aren't indexed yet and suggests how to update.

### Adding 1-2 New Transcripts (Free)

In any Claude Code conversation:
```
I added [Expert Name].txt to my product-experts transcripts.
Can you update the index?
```

### Adding 10+ New Transcripts (Batch, ~$2-3)

Regenerate the entire index:
```bash
python3 ~/.claude/skills/product-experts/index/build-index.py
```

Set your `ANTHROPIC_API_KEY` environment variable first.

## Documentation

- [Installation Guide](INSTALL.md) - Detailed manual installation steps
- [Getting Transcripts](docs/getting-transcripts.md) - How to obtain transcripts
- [How to Use](docs/how-to-use.md) - Usage guide with examples
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions
- [Customization](docs/customization.md) - Advanced configuration options

## How It Works

1. **Indexing** - Extracts expert metadata from transcript introductions (name, bio, expertise, topics)
2. **Search** - Scores experts by keyword overlap with your question (3x weight for expertise, 2x for topics)
3. **Analysis** - 5 parallel subagents read full transcripts and generate advice from each expert's perspective
4. **Synthesis** - Combines insights into actionable summary with common themes and divergent views

## Cost

- **Setup:** $0 (pre-built index included)
- **Usage:** Free (included in Claude Code)
- **Optional:** ~$2-3 to regenerate index for 10+ new transcripts

## Credits

**Created by:** Andrew Schauer
**Built with:** [Claude Code](https://www.anthropic.com/claude-code) by Anthropic
**Designed for:** [Lenny's Podcast](https://www.lennysnewsletter.com/) transcripts

This tool helps you get more value from Lenny Rachitsky's incredible archive of 302+ product management expert interviews. **Please support Lenny** by [subscribing to his newsletter](https://www.lennysnewsletter.com/).

Transcripts are Lenny's intellectual property and are publicly shared via his Dropbox. This tool respects his work by crediting the source and encouraging subscriptions.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

- **Issues:** [GitHub Issues](https://github.com/andrewschauer/product-experts-skill/issues)
- **Discussions:** [GitHub Discussions](https://github.com/andrewschauer/product-experts-skill/discussions)

---

⭐ **Found this helpful?** Star the repo and share it with other PMs!
