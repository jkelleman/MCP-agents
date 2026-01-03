#!/usr/bin/env python3
"""
Documentation Helper MCP Server

A Model Context Protocol server that helps search, understand, and work with documentation:
- Search across multiple documentation files
- Summarize documentation sections
- Find code examples
- Explain technical concepts
- Generate documentation templates
- Check documentation completeness

Built using FastMCP from the official MCP Python SDK.
"""

import sys
import os
import re
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create the FastMCP server
mcp = FastMCP("documentation-helper")


@mcp.tool()
def search_documentation(query: str, doc_path: str = ".") -> str:
    """
    Search for content across documentation files.
    
    Searches for:
    - Keywords and phrases
    - Function/class names
    - Concepts and topics
    - Code examples
    
    Args:
        query: Search term or phrase
        doc_path: Path to documentation directory (default: current directory)
        
    Returns:
        Search results with file locations and context
    """
    if not query or not query.strip():
        return "Error: No search query provided"
    
    query = query.strip().lower()
    results = []
    
    # Common documentation file extensions
    doc_extensions = ['.md', '.txt', '.rst', '.adoc', '.html']
    
    try:
        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return f"Error: Documentation path '{doc_path}' does not exist"
        
        # Search through files
        for file_path in doc_path_obj.rglob('*'):
            if file_path.is_file() and file_path.suffix in doc_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Find matches
                        if query in content.lower():
                            # Get context around matches
                            lines = content.split('\n')
                            matches = []
                            
                            for i, line in enumerate(lines):
                                if query in line.lower():
                                    # Get 2 lines before and after for context
                                    start = max(0, i - 2)
                                    end = min(len(lines), i + 3)
                                    context = '\n'.join(lines[start:end])
                                    matches.append({
                                        'line_num': i + 1,
                                        'context': context
                                    })
                            
                            if matches:
                                results.append({
                                    'file': str(file_path.relative_to(doc_path_obj)),
                                    'matches': matches[:3]  # Limit to first 3 matches per file
                                })
                
                except Exception as e:
                    continue  # Skip files that can't be read
        
        # Build report
        report = f"""
Documentation Search Results
============================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Query: "{query}"
Directory: {doc_path}

Found in {len(results)} file(s):

"""
        
        if results:
            for file_result in results[:10]:  # Limit to 10 files
                report += f"\n📄 {file_result['file']}\n"
                report += "=" * 50 + "\n"
                
                for match in file_result['matches']:
                    report += f"\nLine {match['line_num']}:\n"
                    report += match['context'] + "\n"
                    report += "-" * 50 + "\n"
            
            if len(results) > 10:
                report += f"\n... and {len(results) - 10} more files\n"
        else:
            report += f"No results found for '{query}'\n\n"
            report += "Try:\n"
            report += "• Different keywords\n"
            report += "• Broader search terms\n"
            report += "• Check the documentation path\n"
        
        return report
        
    except Exception as e:
        return f"Error searching documentation: {str(e)}"


@mcp.tool()
def summarize_documentation(file_path: str, max_sections: int = 5) -> str:
    """
    Summarize a documentation file's content and structure.
    
    Provides:
    - Overview of content
    - Main sections/headings
    - Key concepts covered
    - Code examples present
    
    Args:
        file_path: Path to documentation file
        max_sections: Maximum sections to include in summary (default: 5)
        
    Returns:
        Structured summary of the documentation
    """
    if not file_path or not file_path.strip():
        return "Error: No file path provided"
    
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return f"Error: File '{file_path}' does not exist"
        
        with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract headings (Markdown style)
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        
        # Count code blocks
        code_blocks = len(re.findall(r'```[\s\S]*?```', content))
        
        # Count links
        links = len(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content))
        
        # Estimate reading time (average 200 words per minute)
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)
        
        # Build report
        report = f"""
Documentation Summary
====================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

File: {file_path}

📊 Statistics:
--------------
• Word count: {word_count:,}
• Reading time: ~{reading_time} min
• Code examples: {code_blocks}
• Links: {links}
• Sections: {len(headings)}

"""
        
        if headings:
            report += "📑 Main Sections:\n"
            report += "-" * 50 + "\n"
            for i, heading in enumerate(headings[:max_sections], 1):
                report += f"{i}. {heading}\n"
            
            if len(headings) > max_sections:
                report += f"... and {len(headings) - max_sections} more sections\n"
        else:
            report += "ℹ️ No clear section headings found\n"
        
        # Extract first paragraph as overview
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        if paragraphs:
            first_para = paragraphs[0][:300]  # First 300 chars
            if len(paragraphs[0]) > 300:
                first_para += "..."
            report += f"\n📝 Overview:\n"
            report += "-" * 50 + "\n"
            report += first_para + "\n"
        
        return report
        
    except Exception as e:
        return f"Error summarizing documentation: {str(e)}"


@mcp.tool()
def find_code_examples(doc_path: str = ".", language: str = "") -> str:
    """
    Find code examples across documentation files.
    
    Searches for:
    - Code blocks
    - Inline code
    - Specific programming language examples
    
    Args:
        doc_path: Path to documentation directory (default: current directory)
        language: Filter by programming language (e.g., 'python', 'javascript')
        
    Returns:
        List of code examples with locations
    """
    try:
        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return f"Error: Documentation path '{doc_path}' does not exist"
        
        examples = []
        doc_extensions = ['.md', '.txt', '.rst', '.adoc']
        
        # Search through files
        for file_path in doc_path_obj.rglob('*'):
            if file_path.is_file() and file_path.suffix in doc_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Find code blocks
                        code_pattern = r'```(\w*)\n([\s\S]*?)```'
                        matches = re.finditer(code_pattern, content)
                        
                        for match in matches:
                            lang = match.group(1).lower() if match.group(1) else 'unknown'
                            code = match.group(2).strip()
                            
                            # Filter by language if specified
                            if not language or lang == language.lower():
                                examples.append({
                                    'file': str(file_path.relative_to(doc_path_obj)),
                                    'language': lang,
                                    'code': code[:200]  # First 200 chars
                                })
                
                except Exception:
                    continue
        
        # Build report
        report = f"""
Code Examples Found
===================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Directory: {doc_path}
{f"Language filter: {language}" if language else "All languages"}

Found {len(examples)} example(s):

"""
        
        if examples:
            # Group by language
            by_language = {}
            for ex in examples:
                lang = ex['language'] or 'unknown'
                if lang not in by_language:
                    by_language[lang] = []
                by_language[lang].append(ex)
            
            for lang, lang_examples in by_language.items():
                report += f"\n## {lang.upper()} ({len(lang_examples)} examples)\n"
                report += "=" * 50 + "\n"
                
                for ex in lang_examples[:5]:  # First 5 per language
                    report += f"\n📄 {ex['file']}\n"
                    report += "```" + lang + "\n"
                    report += ex['code']
                    if len(ex['code']) >= 200:
                        report += "\n..."
                    report += "\n```\n"
                
                if len(lang_examples) > 5:
                    report += f"\n... and {len(lang_examples) - 5} more {lang} examples\n"
        else:
            report += "No code examples found.\n"
        
        return report
        
    except Exception as e:
        return f"Error finding code examples: {str(e)}"


@mcp.tool()
def check_documentation_completeness(doc_path: str = ".") -> str:
    """
    Check documentation for completeness and identify gaps.
    
    Checks for:
    - README file
    - Getting started guide
    - API documentation
    - Examples
    - Common sections
    
    Args:
        doc_path: Path to documentation directory (default: current directory)
        
    Returns:
        Completeness report with recommendations
    """
    try:
        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return f"Error: Documentation path '{doc_path}' does not exist"
        
        findings = {
            'has_readme': False,
            'has_getting_started': False,
            'has_api_docs': False,
            'has_examples': False,
            'has_contributing': False,
            'has_changelog': False,
            'files_found': []
        }
        
        # Check for common documentation files
        for file_path in doc_path_obj.rglob('*'):
            if file_path.is_file():
                filename_lower = file_path.name.lower()
                findings['files_found'].append(file_path.name)
                
                if 'readme' in filename_lower:
                    findings['has_readme'] = True
                if 'getting' in filename_lower or 'quickstart' in filename_lower or 'started' in filename_lower:
                    findings['has_getting_started'] = True
                if 'api' in filename_lower or 'reference' in filename_lower:
                    findings['has_api_docs'] = True
                if 'example' in filename_lower or 'tutorial' in filename_lower:
                    findings['has_examples'] = True
                if 'contributing' in filename_lower:
                    findings['has_contributing'] = True
                if 'changelog' in filename_lower or 'history' in filename_lower:
                    findings['has_changelog'] = True
        
        # Calculate completeness score
        checks = [
            findings['has_readme'],
            findings['has_getting_started'],
            findings['has_api_docs'],
            findings['has_examples']
        ]
        completeness = (sum(checks) / len(checks)) * 100
        
        # Build report
        report = f"""
Documentation Completeness Check
=================================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Directory: {doc_path}
Completeness Score: {completeness:.0f}%

Essential Documentation:
------------------------
"""
        
        report += f"{'✅' if findings['has_readme'] else '❌'} README file\n"
        report += f"{'✅' if findings['has_getting_started'] else '❌'} Getting started guide\n"
        report += f"{'✅' if findings['has_api_docs'] else '❌'} API documentation\n"
        report += f"{'✅' if findings['has_examples'] else '❌'} Examples/tutorials\n"
        
        report += "\nOptional But Recommended:\n"
        report += "------------------------\n"
        report += f"{'✅' if findings['has_contributing'] else '⚪'} Contributing guide\n"
        report += f"{'✅' if findings['has_changelog'] else '⚪'} Changelog\n"
        
        # Recommendations
        report += "\n💡 Recommendations:\n"
        report += "-" * 50 + "\n"
        
        if not findings['has_readme']:
            report += "❗ Create a README.md with project overview and quick start\n"
        if not findings['has_getting_started']:
            report += "❗ Add a getting started or quickstart guide\n"
        if not findings['has_api_docs']:
            report += "⚠️ Consider adding API reference documentation\n"
        if not findings['has_examples']:
            report += "⚠️ Add code examples or tutorials for common use cases\n"
        
        if completeness == 100:
            report += "🎉 Great! All essential documentation is present!\n"
        
        report += f"\n📁 Total files found: {len(findings['files_found'])}\n"
        
        return report
        
    except Exception as e:
        return f"Error checking documentation completeness: {str(e)}"


@mcp.tool()
def explain_concept(concept: str, doc_path: str = ".") -> str:
    """
    Find and explain a technical concept from documentation.
    
    Searches documentation for:
    - Concept definition
    - Usage examples
    - Related concepts
    
    Args:
        concept: Technical term or concept to explain
        doc_path: Path to documentation directory (default: current directory)
        
    Returns:
        Explanation with references to documentation
    """
    if not concept or not concept.strip():
        return "Error: No concept provided"
    
    concept = concept.strip()
    
    # Use search_documentation to find the concept
    search_results = search_documentation(concept, doc_path)
    
    report = f"""
Concept Explanation
===================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Concept: "{concept}"

Documentation References:
{search_results}

💡 Tip: Review the context above to understand how '{concept}' is used.
Look for definition paragraphs, code examples, and related terms.
"""
    
    return report


@mcp.tool()
def generate_doc_template(doc_type: str = "api") -> str:
    """
    Generate documentation template for common documentation types.
    
    Available templates:
    - api: API endpoint documentation
    - function: Function/method documentation
    - class: Class documentation
    - readme: Project README
    - tutorial: Tutorial/guide
    
    Args:
        doc_type: Type of documentation template to generate
        
    Returns:
        Documentation template ready to fill in
    """
    templates = {
        'api': """# API Endpoint: [Endpoint Name]

## Overview
[Brief description of what this endpoint does]

## Endpoint
```
[METHOD] /api/v1/[resource]
```

## Authentication
[Required authentication method]

## Request

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1    | string | Yes    | [Description] |
| param2    | integer | No    | [Description] |

### Request Body
```json
{
  "field1": "value",
  "field2": 123
}
```

## Response

### Success Response (200 OK)
```json
{
  "status": "success",
  "data": {
    "id": "123",
    "field1": "value"
  }
}
```

### Error Responses

**400 Bad Request**
```json
{
  "status": "error",
  "message": "Invalid parameter"
}
```

**401 Unauthorized**
```json
{
  "status": "error",
  "message": "Authentication required"
}
```

## Example

```bash
curl -X [METHOD] https://api.example.com/api/v1/[resource] \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"field1": "value"}'
```

## Rate Limiting
[Information about rate limits]

## Notes
- [Additional note 1]
- [Additional note 2]
""",
        
        'function': """## `function_name(param1, param2)`

### Description
[Brief description of what the function does]

### Parameters

- **param1** (`type`) - [Description of parameter 1]
- **param2** (`type`, optional) - [Description of parameter 2]. Default: `default_value`

### Returns

- **`return_type`** - [Description of return value]

### Raises

- **`ErrorType`** - [When this error occurs]

### Examples

```python
# Example 1: Basic usage
result = function_name("value1", 42)
print(result)  # Output: [expected output]

# Example 2: With optional parameter
result = function_name("value1", 42, optional_param=True)
```

### Notes

- [Important note 1]
- [Important note 2]

### See Also

- [`related_function()`](#related-function) - [Brief description]
""",
        
        'class': """## Class: `ClassName`

### Description
[Brief description of what this class does]

### Constructor

```python
ClassName(param1, param2)
```

#### Parameters
- **param1** (`type`) - [Description]
- **param2** (`type`) - [Description]

### Attributes

- **attribute1** (`type`) - [Description]
- **attribute2** (`type`) - [Description]

### Methods

#### `method_name(param)`

[Description of what the method does]

**Parameters:**
- **param** (`type`) - [Description]

**Returns:**
- `return_type` - [Description]

**Example:**
```python
instance = ClassName(val1, val2)
result = instance.method_name(param_value)
```

### Examples

```python
# Create instance
obj = ClassName("value1", "value2")

# Use methods
result = obj.method_name("input")
print(result)
```

### Notes

- [Important note about usage]
""",
        
        'readme': """# Project Name

[Brief project description in 1-2 sentences]

## Features

- ✨ Feature 1
- 🚀 Feature 2
- 💡 Feature 3

## Installation

```bash
# Using pip
pip install project-name

# Using npm
npm install project-name
```

## Quick Start

```python
# Example code showing basic usage
from project import ClassName

# Create instance
obj = ClassName()

# Do something
result = obj.do_something()
print(result)
```

## Documentation

Full documentation is available at [https://docs.example.com](https://docs.example.com)

## Examples

See the [examples/](examples/) directory for more examples:

- [Example 1](examples/example1.py) - Basic usage
- [Example 2](examples/example2.py) - Advanced features

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[License Type] - see [LICENSE](LICENSE) file for details

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our community](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/user/repo/issues)
""",
        
        'tutorial': """# [Tutorial Title]

[Brief introduction explaining what users will learn]

## What You'll Learn

- Item 1
- Item 2
- Item 3

## Prerequisites

- Prerequisite 1
- Prerequisite 2
- Basic knowledge of [concept]

## Step 1: [First Step Title]

[Explanation of first step]

```python
# Code example
code_here()
```

**What's happening:**
- Point 1
- Point 2

## Step 2: [Second Step Title]

[Explanation of second step]

```python
# Code example
more_code()
```

## Step 3: [Third Step Title]

[Continue pattern...]

## Running the Code

```bash
# Command to run
python script.py
```

**Expected output:**
```
[Show what users should see]
```

## Troubleshooting

**Problem:** [Common issue]
**Solution:** [How to fix it]

## Next Steps

- [What to learn next]
- [Related tutorials]
- [Advanced topics]

## Full Code

```python
# Complete working example
[full code here]
```
"""
    }
    
    doc_type_lower = doc_type.lower()
    
    if doc_type_lower in templates:
        return f"""
Documentation Template: {doc_type.upper()}
{'=' * 50}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{templates[doc_type_lower]}

💡 Tip: Fill in the placeholders [like this] with your specific information.
"""
    else:
        available = ', '.join(templates.keys())
        return f"""
Error: Unknown documentation type '{doc_type}'

Available templates:
{available}

Example usage: generate_doc_template("api")
"""


@mcp.prompt()
def documentation_review_prompt(doc_path: str = ".") -> list[base.Message]:
    """
    Generate comprehensive documentation review prompt.
    
    Args:
        doc_path: Path to documentation directory
        
    Returns:
        Structured prompt for thorough documentation review
    """
    prompt_text = f"""
Please review the documentation in this directory: {doc_path}

Use these tools for analysis:

1. check_documentation_completeness - Check for essential documentation files
2. search_documentation - Search for specific topics or gaps
3. find_code_examples - Verify code examples are present
4. summarize_documentation - Review key documentation files

Provide assessment of:
- Completeness: What's missing?
- Clarity: Is content easy to understand?
- Examples: Are there enough code examples?
- Structure: Is documentation well-organized?
- Recommendations: What should be added or improved?

Format findings clearly with specific, actionable recommendations.
"""
    
    return [base.UserMessage(prompt_text)]


def main():
    """
    Main entry point for the Documentation Helper MCP Server.
    Starts the server with STDIO transport.
    """
    try:
        print("Starting Documentation Helper MCP Server...", file=sys.stderr)
        print("Server ready to search and analyze documentation", file=sys.stderr)
        
        # Run the server
        mcp.run()
        
    except Exception as e:
        print(f"Failed to start Documentation Helper: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
