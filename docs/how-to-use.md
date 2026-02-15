# How to Use the Product Experts Skill

This guide covers everything you need to know to get expert advice using the product-experts skill.

## Basic Usage

### Invoking the Skill

In any Claude Code conversation, type:

```
/product-experts
```

Claude will respond with:
```
I'll consult 5 product experts from Lenny's podcast to help with your challenge.

What product management question or challenge do you need advice on?
```

### Asking Your Question

Be specific about your challenge. The more context you provide, the better the expert selection and advice.

**Good questions:**
- "How do I get noticed when hunting for PM jobs? I'm not talking about interviews, but how to get interviews in the first place."
- "What's the best pricing strategy for a PLG product moving upmarket to enterprise?"
- "How should I structure my product org as we scale from 5 to 20 PMs?"

**Less effective questions:**
- "Tell me about product management" (too broad)
- "What's growth?" (too generic)
- "Help" (no specific challenge)

### What Happens Next

1. **Expert Selection** (~10 seconds)
   - Claude analyzes your question
   - Selects 5 most relevant experts from 302 options
   - Shows you who was selected and why

2. **Expert Analysis** (~2-3 minutes)
   - 5 parallel agents read full transcripts (30-50 pages each)
   - Each extracts advice from that expert's perspective
   - Includes direct quotes with context

3. **Synthesis** (~30 seconds)
   - Combines insights across all 5 experts
   - Identifies common themes and divergent perspectives
   - Creates actionable takeaways

4. **Results Delivered**
   - Executive summary in chat
   - Links to detailed expert responses
   - Links to synthesis document

## Understanding the Output

### Output Directory Structure

Each consultation creates a timestamped folder:

```
~/Documents/product-experts-outputs/
└── 2026-02-12-15-18-pm-job-hunting-getting-noticed/
    ├── summary.md
    └── experts/
        ├── phyl-terry.md
        ├── jackie-bavaro.md
        ├── lauren-ipsen.md
        ├── hari-srinivasan.md
        └── gergely-orosz.md
```

### Summary File

The `summary.md` file includes:
- **Executive Summary** - High-level synthesis (2-3 paragraphs)
- **Common Themes** - What most experts agreed on
- **Divergent Perspectives** - Where experts had different views
- **Key Takeaways & Action Items** - 5-7 concrete, actionable recommendations
- **Expert Panel** - Links to individual expert responses
- **Next Steps** - Suggested actions based on the advice

### Individual Expert Files

Each expert's markdown file includes:
- Expert background and bio
- Key insights relevant to your question
- Actionable advice from that expert's perspective
- Relevant experience and examples from their interview
- Direct quotes from the transcript with context
- Related topics they covered

## Advanced Usage

### Building on Previous Context

The skill has access to your conversation history before invocation. You can:

```
[Discuss your challenge with Claude normally]

You: I'm struggling with pricing our product. We have a freemium model but
conversion is low. I'm wondering if we should add a middle tier or remove
the free tier entirely.

Claude: [discusses your situation, asks clarifying questions]

You: /product-experts
```

The experts will receive context about your specific situation, not just your question.

### Follow-up Questions

After receiving expert advice, you can:

```
You: Can you dive deeper into what Gergely said about pedigree?
     I didn't understand the academy companies concept.

You: These experts talked about pricing, but I want to hear specifically
     about PLG pricing. Can you consult different experts focused on that?
```

Claude will either elaborate using the existing consultation or run a new one with different experts.

### Combining Multiple Sessions

You can run multiple consultations on related topics:

```
Session 1: "How do I structure pricing tiers for PLG?"
Session 2: "How do I measure and optimize conversion from free to paid?"
Session 3: "What activation metrics matter most for PLG products?"
```

Each creates a separate output folder you can reference later.

## Keeping Your Index Updated

Lenny publishes new episodes regularly. Your index may become out-of-date.

### Check if Your Index is Current

```bash
python3 ~/.claude/skills/product-experts/index/check-index.py
```

This shows:
- When your index was last updated
- How many transcripts are indexed vs. in your folder
- Which new transcripts aren't indexed yet
- Recommended update method

### Update Method 1: Incremental (Free, 1-3 New Transcripts)

If you've added just a few new transcripts:

1. Download new transcript files to your transcripts directory
2. In any Claude Code conversation:
   ```
   I added [Expert Name].txt to my product-experts transcripts.
   Can you update the index?
   ```

Claude will read the new transcript, extract metadata, and update both index files.

**Cost:** Free (included in Claude Code)
**Time:** ~30-60 seconds per transcript
**Best for:** 1-3 new transcripts

### Update Method 2: Batch (API, 10+ New Transcripts)

If you have many new transcripts:

1. Download all new transcripts to your directory
2. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```
3. Run the batch indexer:
   ```bash
   python3 ~/.claude/skills/product-experts/index/build-index.py
   ```

**Cost:** ~$2-3 for 10+ transcripts (uses Anthropic API)
**Time:** ~5-10 minutes for full rebuild
**Best for:** 10+ new transcripts or full re-index

## Tips for Better Results

### Ask Specific Questions

**Instead of:** "How do I grow?"
**Try:** "We have 10K MAU with 2% conversion to paid. How do I diagnose whether the problem is acquisition, activation, or monetization?"

### Provide Context

**Instead of:** "Should I hire more PMs?"
**Try:** "We have 5 PMs and 30 engineers across 3 product lines. Teams are moving slowly and I'm worried about coordination overhead. Should I hire more PMs or reorganize?"

### Iterate on Expert Selection

If the selected experts don't feel right:
- Be more specific about your domain (B2B, B2C, marketplace, etc.)
- Mention specific companies or situations as references
- Ask for experts with specific backgrounds

### Use the Synthesis, Then Dig Deeper

1. Read the executive summary first (in chat)
2. Identify which insights resonate most
3. Read those specific expert responses in detail
4. Ask follow-up questions about specific advice

## Example Session

Here's what a real consultation looks like:

```
You: /product-experts

Claude: I'll consult 5 product experts from Lenny's podcast to help with
your challenge.

What product management question or challenge do you need advice on?

You: How do I get noticed when hunting for PM jobs? I need help getting
interviews, not doing well in interviews.

Claude: I've selected these 5 experts to advise you:

1. Phyl Terry - Author of 'Never Search Alone', expert on job searching
2. Jackie Bavaro - Wrote 'Cracking the PM Interview', former Head of PM at Asana
3. Lauren Ipsen - Executive recruiter, 80+ senior PM placements
4. Hari Srinivasan - VP of Product at LinkedIn Talent Solutions
5. Gergely Orosz - Built massive newsletter audience, hired many PMs

Analyzing their transcripts now...

[~2-3 minutes pass]

Claude: [Shows Executive Summary in chat]

✓ Expert panel consultation complete!

📄 Summary: [link to summary.md]

👥 Individual expert responses:
- Phyl Terry: [link]
- Jackie Bavaro: [link]
...

Would you like me to dive deeper into any expert's advice, or consult
additional experts on a specific aspect?
```

## Next Steps

- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Customization](customization.md)** - Advanced configuration
- **[Getting Transcripts](getting-transcripts.md)** - Keep transcripts updated
