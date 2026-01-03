# Documentation Helper MCP Server

A Model Context Protocol (MCP) server that helps you search, understand, and work with documentation files.

## 🎯 Features

### Tools Available

1. **`search_documentation`** - Search across multiple documentation files
   - Keyword and phrase search
   - Contextual results
   - File location tracking
   - Supports Markdown, text, RST, AsciiDoc

2. **`summarize_documentation`** - Summarize documentation content
   - Overview of file structure
   - Main sections and headings
   - Statistics (word count, reading time, code examples)
   - Key concepts

3. **`find_code_examples`** - Find code examples
   - Search all documentation
   - Filter by programming language
   - Shows code context
   - Groups by language

4. **`check_documentation_completeness`** - Audit documentation
   - Checks for essential files (README, getting started, etc.)
   - Completeness score
   - Recommendations for improvements
   - Gap identification

5. **`explain_concept`** - Explain technical concepts
   - Searches for concept definitions
   - Shows usage examples
   - Provides documentation references

6. **`generate_doc_template`** - Generate documentation templates
   - API endpoint documentation
   - Function/method documentation
   - Class documentation
   - README template
   - Tutorial template

### Prompts Available

- **`documentation_review_prompt`** - Comprehensive documentation review template

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- uv (recommended) or pip

### Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the documentation-helper directory
cd documentation-helper

# Install dependencies
uv add "mcp[cli]"
uv pip install -e .
```

### Running the Server

```bash
# Run with uv
uv run python -m documentation_helper.server

# Or use MCP CLI
uv run mcp run documentation_helper/server.py
```

## 💡 Usage Examples

### Example 1: Search Documentation

```python
# Search for a term across all documentation
search_documentation("authentication", "./docs")

# Returns matches with context and file locations
```

### Example 2: Check Completeness

```python
# Audit your documentation
check_documentation_completeness("./docs")

# Returns:
# ✅ README file
# ✅ Getting started guide
# ❌ API documentation
# Completeness Score: 67%
```

### Example 3: Find Code Examples

```python
# Find all Python examples
find_code_examples("./docs", language="python")

# Or find all examples
find_code_examples("./docs")
```

### Example 4: Generate Template

```python
# Generate an API documentation template
generate_doc_template("api")

# Returns ready-to-use template with placeholders
```

## 🔧 Integration with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "documentation-helper": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/documentation-helper",
        "run",
        "documentation-helper"
      ]
    }
  }
}
```

## 📋 Testing with MCP Inspector

```bash
# Install MCP Inspector
npx @modelcontextprotocol/inspector

# In the Inspector, connect using:
uv run python -m documentation_helper.server
```

## 💼 Use Cases

**Perfect for:**
- ✅ Finding specific information in large documentation sets
- ✅ Onboarding new team members (search for concepts)
- ✅ Auditing documentation completeness
- ✅ Creating consistent documentation templates
- ✅ Discovering code examples
- ✅ Technical writing and documentation maintenance

**Works with:**
- Markdown (.md)
- Plain text (.txt)
- ReStructuredText (.rst)
- AsciiDoc (.adoc)
- HTML (.html)

## 🎨 Best Practices

### For Better Results:

✅ **Organize documentation**
- Keep related docs in subdirectories
- Use consistent naming conventions
- Include README in each major section

✅ **Use clear headings**
- Markdown headings help with summarization
- Structure documents logically
- Use heading levels appropriately

✅ **Include code examples**
- Use fenced code blocks with language tags
- ````python, ````javascript, etc.
- Add comments explaining examples

✅ **Cross-reference**
- Link related documentation
- Create an index or table of contents
- Use consistent terminology

## 🔍 Search Tips

**Effective searches:**
```python
# Specific terms
search_documentation("JWT token validation")

# Function names
search_documentation("authenticate_user")

# Concepts
search_documentation("rate limiting")
```

**Better than:**
```python
# Too vague
search_documentation("how to")

# Single letters
search_documentation("a")
```

## 🛠️ Development

```bash
# Run in development mode
uv run python server.py

# Test individual tools
python -c "from server import search_documentation; print(search_documentation('test', '.'))"
```

## 📚 Integration Ideas

Combine with:
- **CI/CD** - Automated documentation checks
- **IDE plugins** - Quick documentation lookup
- **Chatbots** - Answer questions from docs
- **Knowledge bases** - Index and search documentation
- **Static site generators** - Validate documentation structure

## 🤝 Contributing

Built for the MCP community. Contributions welcome!

---

*Part of the MCP-Oreilly repository - Real-world MCP agents for everyday tasks*
