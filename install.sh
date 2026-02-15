#!/bin/bash

# Product Experts Skill - Installation Script
# This script installs the product-experts skill for Claude Code

set -e  # Exit on error

echo "======================================================================="
echo "Product Experts Skill - Installation"
echo "======================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running from correct directory
if [ ! -f "skill/SKILL.md" ]; then
    echo -e "${RED}❌ Error: Please run this script from the product-experts-skill directory${NC}"
    echo "Usage: cd product-experts-skill && ./install.sh"
    exit 1
fi

echo "Step 1: Checking prerequisites..."
echo "-----------------------------------"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Please install Python 3.9 or higher:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}❌ Python version $PYTHON_VERSION is too old${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip3 not found, attempting to install...${NC}"
    python3 -m ensurepip --default-pip || {
        echo -e "${RED}❌ Could not install pip${NC}"
        exit 1
    }
fi

echo ""
echo "Step 2: Installing Python dependencies..."
echo "------------------------------------------"

# Install anthropic package
if python3 -c "import anthropic" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} anthropic package already installed"
else
    echo "Installing anthropic package..."
    pip3 install anthropic || {
        echo -e "${RED}❌ Failed to install anthropic package${NC}"
        exit 1
    }
    echo -e "${GREEN}✓${NC} anthropic package installed"
fi

echo ""
echo "Step 3: Configuration"
echo "---------------------"
echo "I need to know where you want to store transcripts and outputs."
echo ""

# Get transcripts directory
read -p "Transcripts directory [~/Documents/lennys-podcast-transcripts]: " TRANSCRIPTS_DIR
TRANSCRIPTS_DIR=${TRANSCRIPTS_DIR:-~/Documents/lennys-podcast-transcripts}

# Expand tilde
TRANSCRIPTS_DIR="${TRANSCRIPTS_DIR/#\~/$HOME}"

# Get output directory
read -p "Output directory [~/Documents/product-experts-outputs]: " OUTPUT_DIR
OUTPUT_DIR=${OUTPUT_DIR:-~/Documents/product-experts-outputs}

# Expand tilde
OUTPUT_DIR="${OUTPUT_DIR/#\~/$HOME}"

echo ""
echo "Configuration:"
echo "  Transcripts: $TRANSCRIPTS_DIR"
echo "  Outputs: $OUTPUT_DIR"
echo ""

# Create directories if they don't exist
mkdir -p "$TRANSCRIPTS_DIR"
mkdir -p "$OUTPUT_DIR"

echo -e "${GREEN}✓${NC} Directories created"

echo ""
echo "Step 4: Installing skill files..."
echo "----------------------------------"

# Create skill directory
SKILL_DIR="$HOME/.claude/skills/product-experts"
mkdir -p "$SKILL_DIR/index"
mkdir -p "$SKILL_DIR/templates"

# Copy files
echo "Copying skill files..."
cp skill/SKILL.md "$SKILL_DIR/"
cp config.example.json "$SKILL_DIR/"  # Keep example for reference
cp skill/index/*.py "$SKILL_DIR/index/"
cp skill/index/*.json "$SKILL_DIR/index/"
cp skill/templates/*.md "$SKILL_DIR/templates/"

# Make scripts executable
chmod +x "$SKILL_DIR/index/build-index.py"
chmod +x "$SKILL_DIR/index/check-index.py"

echo -e "${GREEN}✓${NC} Skill files copied to $SKILL_DIR"

echo ""
echo "Step 5: Creating config file..."
echo "--------------------------------"

# Create config.json with user's paths
# Convert paths back to use ~ for portability
TRANSCRIPTS_DISPLAY="${TRANSCRIPTS_DIR/#$HOME/~}"
OUTPUT_DISPLAY="${OUTPUT_DIR/#$HOME/~}"

cat > "$SKILL_DIR/config.json" << EOF
{
  "transcripts_directory": "$TRANSCRIPTS_DISPLAY",
  "output_directory": "$OUTPUT_DISPLAY",
  "skill_directory": "~/.claude/skills/product-experts"
}
EOF

# Verify config was created successfully
if [ ! -f "$SKILL_DIR/config.json" ]; then
    echo -e "${RED}❌ Failed to create config.json${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Config file created: $SKILL_DIR/config.json"

echo ""
echo "======================================================================="
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo "======================================================================="
echo ""
echo "⚠️  IMPORTANT: The skill requires transcripts to work!"
echo ""
echo "Next steps:"
echo ""
echo "1. Download transcripts from Lenny's Dropbox (~50-100 MB):"
echo "   https://www.dropbox.com/scl/fo/yxi4s2w998p1gvtpu4193/AMdNPR8AOw0lMklwtnC0TrQ?rlkey=j06x0nipoti519e0xgm23zsn9&e=1&st=ahz0fj11&dl=0"
echo ""
echo "   Save all .txt files to: $TRANSCRIPTS_DIR"
echo "   IMPORTANT: Exclude 'Interview Q Compilation.txt' (compilation episode)"
echo ""
echo "2. Verify transcripts downloaded:"
echo "   ls $TRANSCRIPTS_DIR/*.txt | wc -l"
echo "   (Should show 302 files)"
echo ""
echo "3. Check index status:"
echo "   python3 $SKILL_DIR/index/check-index.py"
echo ""
echo "4. Try the skill in Claude Code:"
echo "   /product-experts"
echo ""
echo "Documentation:"
echo "  - Quick start: README.md"
echo "  - Installation: INSTALL.md"
echo "  - Usage guide: docs/how-to-use.md"
echo "  - Troubleshooting: docs/troubleshooting.md"
echo ""
echo "Need help? https://github.com/andrewschauer/product-experts-skill/issues"
echo ""
