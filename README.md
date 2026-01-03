# MCP Agents Portfolio - Real-World AI Solutions

**By Jen Kelleman** | Principal Content Designer @ Microsoft

Building production-ready MCP agents that solve real business problems.

---

## 👋 About This Repository

After completing the [O'Reilly Live Training on Model Context Protocol (MCP)](https://www.oreilly.com/live-events/create-ai-agents-with-model-context-protocol-mcp/0642572196868/0642572196851/) taught by Bruce Hopkins, I built three custom MCP agents that address everyday workflow challenges. This repository showcases both the original training materials and my practical implementations.

### What I Built

🎨 **Content Design Assistant** - Helps UX writers create accessible, clear content  
📝 **Meeting Notes Organizer** - Extracts action items and decisions from meeting transcripts  
📚 **Documentation Helper** - Searches and summarizes technical documentation

These agents demonstrate how MCP can transform common workplace tasks into AI-powered workflows.

## 🌟 Why MCP Matters - Key Learnings

Through this course and hands-on development, I learned why **Model Context Protocol is transforming how we build AI applications**:

### The HTTP of AI Communication

Just as HTTP standardized web communication, **MCP is becoming the standard for AI agent communication**. This matters because:

- **🔌 Universal Connectivity** - Any MCP client can connect to any MCP server, creating an ecosystem of interoperable AI tools
- **🔍 Dynamic Discovery** - AI assistants can discover and use new capabilities on the fly without hardcoding integrations
- **🔐 Secure by Design** - Standardized security patterns protect sensitive data while enabling powerful integrations
- **📈 Enterprise-Ready** - Access corporate data, confidential information, and personal sources securely

### Core Principles I Applied

**1. Tools as First-Class Citizens**  
MCP tools are discoverable, self-documenting functions that AI assistants can invoke. Each of my agents exposes 5-6 specialized tools.

**2. Prompts as Reusable Templates**  
Pre-built prompts guide AI interactions consistently, ensuring quality outputs every time.

**3. STDIO Transport**  
Simple, reliable communication using standard input/output makes deployment straightforward.

**4. Context is Everything**  
MCP enables AI to access exactly the context it needs—files, databases, APIs—without exposing everything.

---

## 📁 Repository Structure

### `/MCP-Oreilly-training/`
Original O'Reilly Live Training course materials including:
- **Python** weather MCP server example with FastMCP
- **Java 21** enterprise-grade implementations  
- **Node.js** lightweight server examples
- **PostgreSQL** database integration patterns

### My Custom MCP Agents

#### 🎨 `/content-design-assistant/`
**Purpose:** Help UX writers and content designers create better content

**Tools:**
- `analyze_readability` - Check sentence length, complexity, reading level
- `check_accessibility` - Find accessibility issues (vague links, all-caps, etc.)
- `evaluate_tone` - Assess if tone matches brand voice
- `review_error_message` - Evaluate error messages for clarity and helpfulness
- `suggest_alternatives` - Find simpler words to replace jargon

**Use Cases:** Review UI copy, improve error messages, check microcopy, audit accessibility

#### 📝 `/meeting-notes-organizer/`
**Purpose:** Extract actionable insights from meeting transcripts

**Tools:**
- `extract_action_items` - Find tasks with owners and due dates
- `identify_decisions` - List approved/rejected decisions
- `summarize_discussion` - Create concise meeting summary
- `extract_questions` - Find answered and unanswered questions
- `identify_blockers` - Flag risks and concerns
- `generate_followup_email` - Create professional follow-up template

**Use Cases:** Process Teams/Zoom transcripts, track action items, document decisions, create follow-ups

#### 📚 `/documentation-helper/`
**Purpose:** Search and understand technical documentation

**Tools:**
- `search_documentation` - Find content across multiple doc files
- `summarize_documentation` - Get overview of any doc file
- `find_code_examples` - Locate examples by language
- `check_documentation_completeness` - Audit for missing docs
- `explain_concept` - Find definitions and explanations
- `generate_doc_template` - Create API, function, README templates

**Use Cases:** Onboard new developers, find examples, audit docs, maintain documentation

---

## 🔧 Development Tools & SDKs I Used

### Primary Stack: Python + FastMCP

All three agents built with:
- **Python 3.10+** - Core language
- **FastMCP** - Official MCP SDK from Anthropic
- **STDIO transport** - Standard input/output communication
- **uv** - Modern Python package manager

### Why Python + FastMCP?

✅ **Rapid Development** - FastMCP handles all protocol complexity  
✅ **Type Safety** - Python type hints for reliable tools  
✅ **Simple Deployment** - No web servers needed, just STDIO  
✅ **Great Documentation** - Clear examples and patterns  

### Development Workflow

```bash
# Install dependencies
uv add "mcp[cli]"

# Run server locally
uv run python -m agent_name.server

# Test with MCP Inspector
npx @modelcontextprotocol/inspector
```

---

## 🌐 Integration Examples

### Claude Desktop Integration

Each agent can be integrated with Claude Desktop by adding to `claude_desktop_config.json`:

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

### Real-World Use Cases

**Content Design Assistant**
- Review UI strings before shipping
- Audit error messages for accessibility
- Check tone consistency across products
- Find simpler alternatives to technical terms

**Meeting Notes Organizer**
- Process daily standup transcripts
- Extract action items from client calls
- Document sprint planning decisions
- Track blockers across retrospectives

**Documentation Helper**
- Search internal wiki for answers
- Audit API documentation completeness
- Find code examples during development
- Onboard new team members faster

### Extensibility

Each agent can be extended to:
- Connect to external APIs (weather, databases, CRM)
- Integrate with enterprise tools (Jira, Confluence, Slack)
- Add custom business logic and validation
- Chain with other MCP servers for complex workflows

---

## 🚀 Getting Started

### Explore the Agents

Each agent directory contains:
- `server.py` - Full MCP server implementation
- `README.md` - Detailed documentation and examples
- `pyproject.toml` - Dependencies and configuration

### Run an Agent Locally

```bash
# Clone this repository
git clone https://github.com/jkelleman/MCP-Oreilly.git
cd MCP-Oreilly

# Navigate to any agent
cd content-design-assistant

# Install and run
uv add "mcp[cli]"
uv pip install -e .
uv run python -m content_design_assistant.server
```

### Test with MCP Inspector

```bash
# Install MCP Inspector (one-time)
npx @modelcontextprotocol/inspector

# Connect to your running agent
# Follow the Inspector UI to test tools and prompts
```

---

## 💡 What I Learned

### Technical Skills
- Building MCP servers with FastMCP
- Designing self-documenting AI tools
- Implementing STDIO transport
- Creating reusable prompt templates
- Testing with MCP Inspector

### Design Principles
- **Start with the user need** - Each agent solves a real problem
- **Tools should be focused** - Do one thing well
- **Context matters** - Give AI exactly what it needs
- **Make it testable** - MCP Inspector is invaluable
- **Documentation is key** - Clear READMEs and examples essential

### Future Applications
MCP opens up possibilities for:
- Enterprise AI assistants with secure data access
- Domain-specific tools for specialized workflows
- AI-powered automation of repetitive tasks
- Intelligent agents that combine multiple data sources
- Custom integrations without vendor lock-in

---

## 📚 Resources

### Official MCP Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

### Course Materials
- [O'Reilly Live Training](https://www.oreilly.com/live-events/create-ai-agents-with-model-context-protocol-mcp/0642572196868/0642572196851/)
- [MCP Book on Leanpub](https://leanpub.com/mcp)
- Original training materials in `/MCP-Oreilly-training/`

---

## 👤 About Me

**Jen Kelleman**  
Principal Content Designer @ Microsoft

I'm passionate about making AI accessible and useful for real work. These MCP agents represent my exploration of how AI can augment everyday workflows—from writing better content to organizing meetings to navigating documentation.

### Connect

- 💼 [LinkedIn](https://linkedin.com/in/jenniferkelleman)
- ✍️ [Medium](https://jenkelleman.medium.com)
- 🌐 [AI Content Design Handbook](https://jkelleman.github.io/ai-content-design-handbook/)
- 📧 jenkelleman@microsoft.com

### Other Projects

- **[AI Content Design Handbook](https://github.com/jkelleman/ai-content-design-handbook)** - Comprehensive guide for UX writing and content design in the AI era

---

**The future of AI agent development is here, and it speaks MCP!**

*Original course by [Bruce Hopkins](https://github.com/BruceTraining) | [O'Reilly Live Training](https://www.oreilly.com/live-events/)*
