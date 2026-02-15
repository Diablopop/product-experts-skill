# Changelog

All notable changes to the product-experts skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-15

### Initial Release

**Features:**
- 302 product management experts from Lenny's Podcast
- Parallel expert analysis (5 experts analyzed simultaneously in ~2-3 minutes)
- Comprehensive synthesis with common themes and divergent perspectives
- Pre-built index included (no API calls needed for basic usage)
- Customizable output templates
- Skills-first search algorithm (3x weight on expertise, 2x on topics)

**Components:**
- Automated installation script (`install.sh`)
- Configuration-based path management
- Index freshness checker (`check-index.py`)
- Batch index rebuilder (`build-index.py`)
- Comprehensive documentation (README, INSTALL, how-to-use, troubleshooting, customization)
- Sample output demonstrating strategic leadership question

**Requirements:**
- Python 3.9+
- Claude Code (VSCode extension)
- 50-100 MB disk space for transcripts

**Known Limitations:**
- Requires manual transcript download from Lenny's Dropbox
- Excludes "Interview Q Compilation.txt" (compilation episode produces inconsistent results)
- Index rebuild requires Anthropic API key (~$2-3 for 302+ transcripts)

---

## Future Releases

### Planned Features
- Automatic transcript download option
- GitHub Actions workflow for index updates
- Support for other podcast transcript formats
- Expert recommendation based on question history
- Multi-language transcript support

---

## Version History Summary

- **1.0.0** (2026-02-15) - Initial public release with 302 experts
