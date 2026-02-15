# Contributing to Product Experts Skill

Thank you for your interest in contributing! This document provides guidelines for contributing to the product-experts skill.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Contributing Code](#contributing-code)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project follows the principle of being helpful, respectful, and constructive. Please:
- Be welcoming to newcomers
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check the [troubleshooting guide](docs/troubleshooting.md)
- Search [existing issues](https://github.com/andrewschauer/product-experts-skill/issues) to avoid duplicates

**When submitting a bug report, include:**
- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs. what actually happened
- **Environment details:**
  - Operating system (macOS, Linux, Windows/WSL)
  - Python version (`python3 --version`)
  - Claude Code version
  - Skill version (from CHANGELOG.md)
- **Error messages** (full text, not screenshots when possible)
- **Relevant configuration** (redact any personal paths)

**Example bug report:**
```markdown
## Bug: check-index.py fails with FileNotFoundError

**Environment:**
- macOS 14.2
- Python 3.11.5
- product-experts skill v1.0.0

**Steps to reproduce:**
1. Run `python3 ~/.claude/skills/product-experts/index/check-index.py`
2. Error appears

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: '~/.claude/skills/product-experts/config.json'
```

**Expected:** Script should expand tilde and find config file
```

### Suggesting Enhancements

We welcome feature suggestions! Please:
- **Check [existing feature requests](https://github.com/andrewschauer/product-experts-skill/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)** first
- **Describe the use case** - what problem does this solve?
- **Describe the solution** - what would you like to see?
- **Consider alternatives** - what other approaches did you consider?

**Example enhancement request:**
```markdown
## Enhancement: Auto-download transcripts during installation

**Problem:** Users must manually download 302 transcript files, which is tedious and error-prone.

**Proposed solution:** Add optional flag to install.sh:
`./install.sh --download-transcripts`

This would:
1. Use curl/wget to download from Dropbox
2. Show progress bar
3. Verify file count (should be 302)
4. Skip if transcripts already exist

**Alternatives considered:**
- GitHub LFS (rejected: 50-100MB repo would be slow to clone)
- Separate download script (possible, but less convenient)

**Trade-offs:**
- Adds dependency on curl/wget
- Makes installation slower
- But eliminates biggest user friction point
```

## Contributing Code

### Getting Started

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork"
   git clone https://github.com/YOUR-USERNAME/product-experts-skill.git
   cd product-experts-skill
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow [style guidelines](#style-guidelines)
   - Test your changes thoroughly
   - Update documentation if needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Use a clear title describing the change
   - Reference any related issues
   - Describe what changed and why
   - Include testing steps

### Pull Request Guidelines

**Good PR example:**
```markdown
## Add automatic transcript download option

Fixes #12

### What changed
- Added `--download-transcripts` flag to install.sh
- Downloads transcripts from Lenny's Dropbox using curl
- Verifies 302 files were downloaded
- Skips download if files already exist

### Why
Users found manual download tedious. This eliminates the biggest friction point in installation.

### Testing
- Tested on macOS 14.2 with fresh install
- Tested on Ubuntu 22.04
- Tested skip behavior when files exist
- Tested error handling when Dropbox is unreachable

### Documentation
- Updated INSTALL.md with new flag
- Updated README Quick Start section
- Added troubleshooting entry for download failures
```

## Style Guidelines

### Python Code

- **PEP 8 compliance** - Use standard Python style
- **Python 3.9+ compatibility** - Don't use features from Python 3.10+
- **Type hints encouraged** but not required
- **Docstrings for functions:**
  ```python
  def extract_metadata(intro_text, filename):
      """Extract expert metadata from transcript introduction.

      Args:
          intro_text: First 150 lines of transcript
          filename: Original transcript filename

      Returns:
          dict: Metadata with bio, companies, roles, expertise, topics
      """
  ```

### Bash Scripts

- **POSIX-compatible** when possible (test with `shellcheck`)
- **Error handling:** Use `set -e` to exit on errors
- **User feedback:** Use colored output for success/errors
- **Comments:** Explain non-obvious sections

### Markdown Documentation

- **Sentence case headings** (not Title Case)
- **Code blocks:** Always specify language (```bash, ```python, ```json)
- **Line length:** Wrap prose at 80-100 characters (not strict)
- **Links:** Use relative links within repo, absolute for external

### JSON Files

- **2-space indentation**
- **No trailing commas**
- **ensure_ascii=False** for unicode characters
- **Sorted keys** where order doesn't matter (e.g., config.json)

## Testing

Currently, the skill has no automated test suite. When contributing:

### Manual Testing Checklist

- [ ] Fresh installation works on your platform
- [ ] Existing installations can upgrade without breaking
- [ ] Config changes are backward-compatible
- [ ] Error messages are clear and actionable
- [ ] Documentation matches implementation

### Future Testing Goals

We'd love contributions toward:
- Unit tests for Python scripts
- Integration tests for skill workflow
- CI/CD pipeline (GitHub Actions)

## Questions?

- **General questions:** [GitHub Discussions](https://github.com/andrewschauer/product-experts-skill/discussions)
- **Bug or feature-specific:** Comment on relevant issue
- **Security concerns:** Email (to be added)

## Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes for their contributions
- Commit history

Thank you for contributing! 🎉
