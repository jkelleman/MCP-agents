#!/usr/bin/env python3
"""
Meeting Notes Organizer MCP Server

A Model Context Protocol server that helps process meeting transcripts and notes:
- Extract action items with owners and due dates
- Identify key decisions made
- Summarize discussion points
- Track open questions and blockers
- Generate follow-up email templates

Built using FastMCP from the official MCP Python SDK.
"""

import sys
import re
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create the FastMCP server
mcp = FastMCP("meeting-notes-organizer")


@mcp.tool()
def extract_action_items(transcript: str) -> str:
    """
    Extract action items from meeting transcript or notes.
    
    Identifies:
    - Tasks mentioned
    - Assigned owners (if mentioned)
    - Due dates (if mentioned)
    - Priority level
    
    Args:
        transcript: Meeting transcript or notes text
        
    Returns:
        Structured list of action items
    """
    if not transcript or not transcript.strip():
        return "Error: No transcript provided"
    
    transcript = transcript.strip()
    action_items = []
    
    # Action keywords
    action_keywords = [
        r'\b(?:will|should|needs? to|has to|must|going to|gonna|todo|to-do|action|task)\b',
        r'\b(?:follow up|followup|reach out|contact|email|schedule|set up|setup)\b',
        r'\b(?:create|build|implement|develop|design|write|update|review|test)\b',
        r'\b(?:send|share|provide|prepare|draft|finalize|complete|finish)\b'
    ]
    
    # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', transcript) if s.strip()]
    
    for sentence in sentences:
        # Check if sentence contains action keywords
        has_action = any(re.search(pattern, sentence, re.IGNORECASE) for pattern in action_keywords)
        
        if has_action:
            # Extract potential owner
            owner_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:will|should|needs? to)', sentence)
            owner = owner_match.group(1) if owner_match else "Unassigned"
            
            # Extract potential due date
            date_patterns = [
                r'by\s+(\w+\s+\d+)',  # by Monday, by Jan 15
                r'(?:next|this)\s+(\w+)',  # next week, this Friday
                r'(\d{1,2}/\d{1,2})',  # 1/15
                r'in\s+(\d+\s+\w+)'  # in 2 days, in 1 week
            ]
            
            due_date = "No due date specified"
            for pattern in date_patterns:
                date_match = re.search(pattern, sentence, re.IGNORECASE)
                if date_match:
                    due_date = date_match.group(1)
                    break
            
            # Determine priority
            priority_keywords = ['urgent', 'asap', 'critical', 'important', 'priority', 'blocker']
            priority = "Normal"
            if any(keyword in sentence.lower() for keyword in priority_keywords):
                priority = "High"
            
            action_items.append({
                'task': sentence,
                'owner': owner,
                'due_date': due_date,
                'priority': priority
            })
    
    # Build report
    report = f"""
Action Items Extracted
======================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total Action Items: {len(action_items)}

"""
    
    if action_items:
        # Group by priority
        high_priority = [item for item in action_items if item['priority'] == 'High']
        normal_priority = [item for item in action_items if item['priority'] == 'Normal']
        
        if high_priority:
            report += "🔴 HIGH PRIORITY:\n"
            report += "=" * 50 + "\n"
            for i, item in enumerate(high_priority, 1):
                report += f"\n{i}. {item['task']}\n"
                report += f"   👤 Owner: {item['owner']}\n"
                report += f"   📅 Due: {item['due_date']}\n"
        
        if normal_priority:
            report += "\n📋 NORMAL PRIORITY:\n"
            report += "=" * 50 + "\n"
            for i, item in enumerate(normal_priority, 1):
                report += f"\n{i}. {item['task']}\n"
                report += f"   👤 Owner: {item['owner']}\n"
                report += f"   📅 Due: {item['due_date']}\n"
        
        report += "\n\n💡 Tip: Review action items for clarity and assign owners if missing.\n"
    else:
        report += "No clear action items found in the transcript.\n"
        report += "Look for statements about future tasks, follow-ups, or commitments.\n"
    
    return report


@mcp.tool()
def identify_decisions(transcript: str) -> str:
    """
    Identify key decisions made during the meeting.
    
    Looks for:
    - Agreement statements
    - Conclusions reached
    - Approved plans
    - Rejected options
    
    Args:
        transcript: Meeting transcript or notes text
        
    Returns:
        List of decisions with context
    """
    if not transcript or not transcript.strip():
        return "Error: No transcript provided"
    
    transcript = transcript.strip()
    decisions = []
    
    # Decision keywords
    decision_patterns = [
        r'\b(?:decided|agreed|approved|confirmed|resolved)\b',
        r'\b(?:we\'ll|we will|let\'s|we should)\b',
        r'\b(?:moving forward|going forward|from now on)\b',
        r'\b(?:conclusion|consensus|agreement)\b',
        r'\b(?:rejected|declined|not going to|won\'t)\b'
    ]
    
    # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', transcript) if s.strip()]
    
    for sentence in sentences:
        # Check if sentence contains decision indicators
        has_decision = any(re.search(pattern, sentence, re.IGNORECASE) for pattern in decision_patterns)
        
        if has_decision:
            # Determine decision type
            if any(word in sentence.lower() for word in ['rejected', 'declined', 'not going', 'won\'t', 'no']):
                decision_type = "❌ Rejected"
            elif any(word in sentence.lower() for word in ['approved', 'agreed', 'yes', 'confirmed']):
                decision_type = "✅ Approved"
            else:
                decision_type = "📌 Decided"
            
            decisions.append({
                'type': decision_type,
                'decision': sentence
            })
    
    # Build report
    report = f"""
Key Decisions
=============
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total Decisions: {len(decisions)}

"""
    
    if decisions:
        for i, item in enumerate(decisions, 1):
            report += f"\n{i}. {item['type']}\n"
            report += f"   {item['decision']}\n"
        
        report += "\n\n💡 Tip: Document decisions in project tracking tools and share with stakeholders.\n"
    else:
        report += "No clear decisions found in the transcript.\n"
        report += "Look for statements about agreements, approvals, or directions chosen.\n"
    
    return report


@mcp.tool()
def summarize_discussion(transcript: str, max_points: int = 5) -> str:
    """
    Summarize main discussion points from the meeting.
    
    Creates a concise summary of:
    - Main topics discussed
    - Key points made
    - Important context
    
    Args:
        transcript: Meeting transcript or notes text
        max_points: Maximum number of summary points (default: 5)
        
    Returns:
        Concise summary of discussion
    """
    if not transcript or not transcript.strip():
        return "Error: No transcript provided"
    
    transcript = transcript.strip()
    
    # Split into paragraphs or major sections
    sections = [s.strip() for s in transcript.split('\n\n') if s.strip()]
    
    if not sections:
        sections = [transcript]
    
    # Basic extraction - identify topic sentences
    discussion_points = []
    
    # Topic indicators
    topic_keywords = [
        r'\b(?:discussed|talking about|regarding|about|covering)\b',
        r'\b(?:main|key|important|critical|focus)\b',
        r'\b(?:issue|problem|challenge|concern)\b',
        r'\b(?:update|status|progress)\b'
    ]
    
    for section in sections[:max_points * 2]:  # Look at more sections than needed
        # Get first sentence of each section as potential discussion point
        sentences = [s.strip() for s in re.split(r'[.!?]+', section) if s.strip()]
        if sentences:
            first_sentence = sentences[0]
            # Check if it looks like a topic sentence
            if len(first_sentence.split()) > 5:  # Not too short
                discussion_points.append(first_sentence)
    
    # Limit to max_points
    discussion_points = discussion_points[:max_points]
    
    # Build report
    report = f"""
Discussion Summary
==================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Main Points Discussed:
----------------------
"""
    
    if discussion_points:
        for i, point in enumerate(discussion_points, 1):
            report += f"\n{i}. {point}\n"
        
        # Add word count
        word_count = len(transcript.split())
        report += f"\n\n📊 Original transcript: {word_count} words\n"
        report += f"📄 Summary: {len(discussion_points)} key points\n"
    else:
        report += "\nCould not identify clear discussion points.\n"
        report += "The transcript may need more structure or context.\n"
    
    return report


@mcp.tool()
def extract_questions(transcript: str) -> str:
    """
    Extract questions raised during the meeting (answered and unanswered).
    
    Identifies:
    - Questions asked
    - Whether they were answered
    - Follow-up needed
    
    Args:
        transcript: Meeting transcript or notes text
        
    Returns:
        List of questions and their status
    """
    if not transcript or not transcript.strip():
        return "Error: No transcript provided"
    
    transcript = transcript.strip()
    
    # Find all questions
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', transcript) if s.strip()]
    questions = [s + '?' for s in sentences if '?' in s or 
                 any(s.lower().startswith(q) for q in ['who', 'what', 'when', 'where', 'why', 'how', 'can', 'should', 'would', 'could', 'is', 'are', 'do', 'does'])]
    
    # Categorize questions
    answered = []
    unanswered = []
    
    for i, question in enumerate(questions):
        # Simple heuristic: if next few sentences don't contain indicators, it's unanswered
        try:
            context_start = transcript.index(question)
            context_after = transcript[context_start:context_start + 300]
            
            answer_indicators = ['yes', 'no', 'answer', 'because', 'it is', 'that\'s', 'correct', 'exactly']
            has_answer = any(indicator in context_after.lower() for indicator in answer_indicators)
            
            if has_answer:
                answered.append(question)
            else:
                unanswered.append(question)
        except ValueError:
            unanswered.append(question)
    
    # Build report
    report = f"""
Questions Identified
====================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total Questions: {len(questions)}
"""
    
    if unanswered:
        report += f"\n\n❓ UNANSWERED QUESTIONS ({len(unanswered)}):\n"
        report += "=" * 50 + "\n"
        for i, q in enumerate(unanswered, 1):
            report += f"{i}. {q}\n"
        
        report += "\n⚠️ These questions need follow-up!\n"
    
    if answered:
        report += f"\n\n✅ ANSWERED QUESTIONS ({len(answered)}):\n"
        report += "=" * 50 + "\n"
        for i, q in enumerate(answered, 1):
            report += f"{i}. {q}\n"
    
    if not questions:
        report += "\n\nNo questions found in the transcript.\n"
    
    return report


@mcp.tool()
def identify_blockers(transcript: str) -> str:
    """
    Identify blockers, risks, and concerns mentioned in the meeting.
    
    Looks for:
    - Blockers preventing progress
    - Risks and concerns
    - Dependencies
    - Issues raised
    
    Args:
        transcript: Meeting transcript or notes text
        
    Returns:
        List of blockers and concerns
    """
    if not transcript or not transcript.strip():
        return "Error: No transcript provided"
    
    transcript = transcript.strip()
    blockers = []
    
    # Blocker keywords
    blocker_patterns = [
        r'\b(?:blocker|blocked|blocking|stuck)\b',
        r'\b(?:risk|concern|worry|worried|problem|issue)\b',
        r'\b(?:waiting for|waiting on|depends on|dependency)\b',
        r'\b(?:can\'t|cannot|unable to|won\'t work|doesn\'t work)\b',
        r'\b(?:challenge|difficulty|obstacle|impediment)\b'
    ]
    
    # Split into sentences
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', transcript) if s.strip()]
    
    for sentence in sentences:
        # Check if sentence contains blocker indicators
        has_blocker = any(re.search(pattern, sentence, re.IGNORECASE) for pattern in blocker_patterns)
        
        if has_blocker:
            # Categorize severity
            if any(word in sentence.lower() for word in ['critical', 'urgent', 'major', 'serious', 'blocker']):
                severity = "🔴 Critical"
            elif any(word in sentence.lower() for word in ['concern', 'risk', 'might', 'could']):
                severity = "🟡 Concern"
            else:
                severity = "🔵 Issue"
            
            blockers.append({
                'severity': severity,
                'issue': sentence
            })
    
    # Build report
    report = f"""
Blockers & Concerns
===================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total Issues: {len(blockers)}

"""
    
    if blockers:
        # Sort by severity
        critical = [b for b in blockers if '🔴' in b['severity']]
        concerns = [b for b in blockers if '🟡' in b['severity']]
        issues = [b for b in blockers if '🔵' in b['severity']]
        
        if critical:
            report += "🔴 CRITICAL BLOCKERS:\n"
            report += "=" * 50 + "\n"
            for i, b in enumerate(critical, 1):
                report += f"{i}. {b['issue']}\n\n"
        
        if concerns:
            report += "🟡 CONCERNS & RISKS:\n"
            report += "=" * 50 + "\n"
            for i, b in enumerate(concerns, 1):
                report += f"{i}. {b['issue']}\n\n"
        
        if issues:
            report += "🔵 OTHER ISSUES:\n"
            report += "=" * 50 + "\n"
            for i, b in enumerate(issues, 1):
                report += f"{i}. {b['issue']}\n\n"
        
        report += "💡 Tip: Address critical blockers immediately and track all issues.\n"
    else:
        report += "✅ No blockers or concerns identified!\n"
    
    return report


@mcp.tool()
def generate_followup_email(
    meeting_title: str,
    transcript: str,
    attendees: str = ""
) -> str:
    """
    Generate a follow-up email template based on meeting notes.
    
    Creates a professional email with:
    - Meeting summary
    - Key decisions
    - Action items
    - Next steps
    
    Args:
        meeting_title: Title/subject of the meeting
        transcript: Meeting transcript or notes
        attendees: Comma-separated list of attendee names (optional)
        
    Returns:
        Formatted follow-up email template
    """
    if not meeting_title or not transcript:
        return "Error: Meeting title and transcript required"
    
    # Use other tools to extract info (simplified inline version)
    email = f"""
Subject: Follow-up: {meeting_title}

Hi {attendees if attendees else "team"},

Thank you for joining today's meeting about {meeting_title}. Here's a summary of what we discussed and our next steps.

## 📋 Key Decisions

[Use the identify_decisions tool to populate this section]

## ✅ Action Items

[Use the extract_action_items tool to populate this section]

## 💬 Summary

[Use the summarize_discussion tool to populate this section]

## ❓ Open Questions

[Use the extract_questions tool for any unanswered questions]

## 🚧 Blockers/Concerns

[Use the identify_blockers tool if any issues were raised]

## 📅 Next Meeting

[Add next meeting date/time if scheduled]

Please let me know if I missed anything or if you have questions!

Best regards,
[Your name]

---
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return email


@mcp.prompt()
def meeting_analysis_prompt(transcript: str) -> list[base.Message]:
    """
    Generate comprehensive meeting analysis prompt.
    
    Args:
        transcript: Meeting transcript or notes text
        
    Returns:
        Structured prompt for full meeting analysis
    """
    prompt_text = f"""
Please analyze this meeting transcript comprehensively:

Transcript:
---
{transcript}
---

Use these tools to extract information:

1. extract_action_items - Find all action items with owners and due dates
2. identify_decisions - List key decisions made
3. summarize_discussion - Create concise summary of main points
4. extract_questions - Find answered and unanswered questions
5. identify_blockers - Identify any blockers or concerns

Then provide:
- A high-level overview
- Key takeaways
- Risk assessment
- Recommendations for follow-up

Format the output clearly for easy sharing with stakeholders.
"""
    
    return [base.UserMessage(prompt_text)]


def main():
    """
    Main entry point for the Meeting Notes Organizer MCP Server.
    Starts the server with STDIO transport.
    """
    try:
        print("Starting Meeting Notes Organizer MCP Server...", file=sys.stderr)
        print("Server ready to process meeting transcripts", file=sys.stderr)
        
        # Run the server
        mcp.run()
        
    except Exception as e:
        print(f"Failed to start Meeting Notes Organizer: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
