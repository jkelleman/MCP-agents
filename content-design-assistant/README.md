# Content Design Assistant MCP Server

A Model Context Protocol (MCP) server that helps content designers and UX writers create clear, accessible, and user-friendly content.

## Features

### Tools Available

1. **`analyze_readability`** - Analyzes text for readability metrics
   - Sentence length and complexity
   - Word choice analysis
   - Readability score estimation
   - Actionable recommendations

2. **`check_accessibility`** - Checks content for accessibility issues
   - Vague link text detection
   - All-caps text warnings
   - Abbreviation identification
   - Screen reader compatibility

3. **`evaluate_tone`** - Evaluates content tone
   - Formality level assessment
   - Emotional tone analysis
   - Consistency checking
   - Tone matching recommendations

4. **`review_error_message`** - Reviews error messages
   - Problem statement clarity
   - Cause explanation
   - Actionable next steps
   - Appropriate tone checking

5. **`suggest_alternatives`** - Suggests simpler alternatives
   - Plain language recommendations
   - Jargon replacement
   - UX writing best practices

### Prompts Available

- **`content_review_prompt`** - Comprehensive content review template
- **`microcopy_suggestions`** - UI element microcopy guidance

## Quick Start

### Prerequisites
- Python 3.10+
- uv (recommended) or pip

### Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the content-design-assistant directory
cd content-design-assistant

# Install dependencies
uv add "mcp[cli]"
uv pip install -e .
```

### Running the Server

```bash
# Run with uv
uv run python -m content_design_assistant.server

# Or use MCP CLI
uv run mcp run content_design_assistant/server.py
```

## Usage Examples

### Example 1: Review an Error Message

```python
# Use the review_error_message tool
review_error_message("Error 504: Gateway Timeout")

# Returns detailed analysis with suggestions for improvement
```

### Example 2: Check Readability

```python
# Use the analyze_readability tool
analyze_readability("Your content here...")

# Gets metrics on sentence length, complexity, and recommendations
```

### Example 3: Find Simpler Words

```python
# Use the suggest_alternatives tool
suggest_alternatives("utilize")

# Returns: ['use', 'apply'] with usage guidance
```

## Integration with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "content-design-assistant": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/content-design-assistant",
        "run",
        "content-design-assistant"
      ]
    }
  }
}
```

## Testing with MCP Inspector

```bash
# Install MCP Inspector
npx @modelcontextprotocol/inspector

# In the Inspector, connect using:
uv run python -m content_design_assistant.server
```

## Content Design Principles

This server follows UX writing best practices:

**Clarity First**
- Use plain language
- Be specific and concrete
- Avoid jargon

**Accessibility Always**
- Write for screen readers
- Use descriptive link text
- Keep it simple

**Tone Matters**
- Be professional yet friendly
- Show empathy
- Guide, don't blame

**Action-Oriented**
- Tell users what to do
- Provide clear next steps
- Make it easy to succeed

## Development

```bash
# Run in development mode
uv run python server.py

# Test individual tools
python -c "from server import analyze_readability; print(analyze_readability('Your text here'))"
```

## Resources

- [UX Writing Best Practices](https://uxwritinghub.com/)
- [Content Design London](https://contentdesign.london/)
- [Material Design Writing Guidelines](https://m3.material.io/foundations/content-design)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/)

## Contributing

Built for the MCP community. Contributions welcome!

---

*Part of the MCP-Oreilly repository - Real-world MCP agents for everyday tasks*
