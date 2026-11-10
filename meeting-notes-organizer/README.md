# Meeting Notes Organizer MCP Server

A Model Context Protocol (MCP) server that processes meeting transcripts and notes to extract actionable insights.

## Features

### Tools Available

1. **`extract_action_items`** - Extracts action items from transcripts
   - Identifies tasks and commitments
   - Assigns owners (when mentioned)
   - Captures due dates
   - Flags priority items

2. **`identify_decisions`** - Identifies key decisions made
   - Agreement statements
   - Approved/rejected options
   - Conclusions reached
   - Direction chosen

3. **`summarize_discussion`** - Creates concise summary
   - Main topics discussed
   - Key points made
   - Important context
   - Configurable summary length

4. **`extract_questions`** - Finds questions and their status
   - Answered questions
   - Unanswered questions needing follow-up
   - Context around questions

5. **`identify_blockers`** - Identifies blockers and concerns
   - Critical blockers
   - Risks and concerns
   - Dependencies
   - Issues raised

6. **`generate_followup_email`** - Creates follow-up email template
   - Professional format
   - Summary of decisions
   - Action items list
   - Next steps

### Prompts Available

- **`meeting_analysis_prompt`** - Comprehensive meeting analysis template

## Quick Start

### Prerequisites
- Python 3.10+
- uv (recommended) or pip

### Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the meeting-notes-organizer directory
cd meeting-notes-organizer

# Install dependencies
uv add "mcp[cli]"
uv pip install -e .
```

### Running the Server

```bash
# Run with uv
uv run python -m meeting_notes_organizer.server

# Or use MCP CLI
uv run mcp run meeting_notes_organizer/server.py
```

## Usage Examples

### Example 1: Extract Action Items

```python
# Paste your meeting transcript
transcript = """
Team discussed the Q1 roadmap. Sarah will create the design mockups 
by next Friday. John needs to review the API specs this week. 
We agreed to schedule a follow-up meeting for January 15th.
"""

# Use the extract_action_items tool
extract_action_items(transcript)

# Returns organized list with owners and due dates
```

### Example 2: Identify Decisions

```python
# Use the identify_decisions tool
identify_decisions(transcript)

# Returns:
# Approved: Schedule follow-up meeting for January 15th
# Decided: Sarah will create design mockups
```

### Example 3: Generate Follow-up Email

```python
# Use the generate_followup_email tool
generate_followup_email(
    meeting_title="Q1 Roadmap Planning",
    transcript=transcript,
    attendees="Sarah, John, Team"
)

# Returns professionally formatted email ready to send
```

## Integration with Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "meeting-notes-organizer": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/meeting-notes-organizer",
        "run",
        "meeting-notes-organizer"
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
uv run python -m meeting_notes_organizer.server
```

## Use Cases

**Perfect for:**
- Team standups and syncs
- Project planning meetings
- Client calls
- Strategy sessions
- Retrospectives
- All-hands meetings

**Input formats:**
- Manual meeting notes
- Transcripts from Teams/Zoom/Meet
- Voice-to-text conversions
- Slack thread summaries

## Best Practices

### For Better Results:

**Include speaker names** when possible
- "John: We should..." works better than just the text

**Mark action items clearly** 
- Use words like "will", "should", "needs to"

**Capture timeframes**
- Mention "by Friday", "next week", specific dates

**Note decisions explicitly**
- Use "we decided", "agreed to", "approved"

**Flag concerns**
- Mention "blocker", "risk", "concern" to track issues

## Development

```bash
# Run in development mode
uv run python server.py

# Test individual tools
python -c "from server import extract_action_items; print(extract_action_items('Your transcript'))"
```

## Integration Ideas

Combine with:
- **Calendar APIs** - Auto-create follow-up meetings
- **Task management** - Push action items to Jira/Asana
- **Email** - Auto-send follow-up summaries
- **Slack/Teams** - Post summaries to channels

## Contributing

Built for the MCP community. Contributions welcome!

---

*Part of the MCP-Oreilly repository - Real-world MCP agents for everyday tasks*
