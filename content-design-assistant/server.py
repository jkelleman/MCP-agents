#!/usr/bin/env python3
"""
Content Design Assistant MCP Server

A Model Context Protocol server that helps content designers and UX writers:
- Review content for clarity, readability, and accessibility
- Check tone and voice consistency
- Identify jargon and suggest simpler alternatives
- Evaluate error messages and microcopy
- Provide actionable feedback based on UX writing best practices

Built using FastMCP from the official MCP Python SDK.
"""

import sys
import re
from typing import List, Dict
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# Create the FastMCP server
mcp = FastMCP("content-design-assistant")


@mcp.tool()
def analyze_readability(text: str) -> str:
    """
    Analyze text readability and provide metrics and recommendations.

    Checks:
    - Sentence length
    - Word complexity
    - Paragraph structure
    - Readability score estimation

    Args:
        text: The content to analyze

    Returns:
        Detailed readability analysis with recommendations
    """
    if not text or not text.strip():
        return "Error: No text provided for analysis"

    text = text.strip()

    # Basic metrics
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = text.split()
    avg_sentence_length = len(words) / len(sentences) if sentences else 0

    # Count long sentences (>25 words)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 25)

    # Count complex words (>3 syllables - rough estimate based on length)
    complex_words = sum(1 for w in words if len(w) > 12)

    # Identify passive voice patterns
    passive_indicators = ['was', 'were', 'been', 'being', 'be']
    passive_count = sum(1 for word in words if word.lower() in passive_indicators)

    # Build report
    report = f"""
Content Readability Analysis
============================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Metrics:
--------
• Total words: {len(words)}
• Total sentences: {len(sentences)}
• Average sentence length: {avg_sentence_length:.1f} words
• Long sentences (>25 words): {long_sentences}
• Complex words (>12 chars): {complex_words}
• Passive voice indicators: {passive_count}

Recommendations:
----------------
"""

    # Generate recommendations
    if avg_sentence_length > 20:
        report += "Average sentence length is high. Aim for 15-20 words per sentence.\n"
    else:
        report += "Good sentence length - keeps content scannable.\n"

    if long_sentences > len(sentences) * 0.3:
        report += "Many long sentences detected. Break them into shorter ones.\n"

    if complex_words > len(words) * 0.1:
        report += "Many complex words found. Consider simpler alternatives.\n"
    else:
        report += "Good word choice - mostly simple, clear language.\n"

    if passive_count > len(words) * 0.05:
        report += "Possible overuse of passive voice. Use active voice for clarity.\n"
    else:
        report += "Good use of active voice.\n"

    report += "\nOverall: "
    if avg_sentence_length < 20 and complex_words < len(words) * 0.1:
        report += "Content is clear and readable! "
    elif avg_sentence_length < 25:
        report += "Content is mostly readable with room for improvement."
    else:
        report += "Content needs simplification for better readability."

    return report


@mcp.tool()
def check_accessibility(text: str) -> str:
    """
    Check content for accessibility issues and provide recommendations.

    Checks for:
    - Vague link text ("click here", "read more")
    - Missing context
    - All-caps text
    - Special characters that may confuse screen readers
    - Abbreviations without expansion

    Args:
        text: The content to check

    Returns:
        Accessibility analysis with specific issues and fixes
    """
    if not text or not text.strip():
        return "Error: No text provided for accessibility check"

    text = text.strip()
    issues = []

    # Check for vague link text
    vague_links = ['click here', 'read more', 'learn more', 'more info', 'click', 'here']
    for link in vague_links:
        if link.lower() in text.lower():
            issues.append(f"Vague link text detected: '{link}' - Use descriptive text that explains the destination")

    # Check for all-caps text
    words = text.split()
    all_caps = [w for w in words if w.isupper() and len(w) > 1 and w.isalpha()]
    if all_caps:
        issues.append(f"All-caps text found: {', '.join(all_caps[:5])} - Screen readers may read letter-by-letter")

    # Check for common abbreviations
    common_abbrevs = ['e.g.', 'i.e.', 'etc.', 'vs.']
    found_abbrevs = [abbrev for abbrev in common_abbrevs if abbrev in text]
    if found_abbrevs:
        issues.append(f"ℹAbbreviations found: {', '.join(found_abbrevs)} - Consider spelling out on first use")

    # Check for special characters
    special_chars = ['&', '@', '#', '%']
    found_special = [char for char in special_chars if char in text]
    if found_special:
        issues.append(f"ℹSpecial characters found: {', '.join(found_special)} - Ensure they're necessary and contextual")

    # Build report
    report = f"""
Accessibility Check
===================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Issues Found: {len(issues)}
"""

    if issues:
        report += "\nDetailed Issues:\n" + "\n".join(issues)
        report += "\n\nBest Practices:\n"
        report += "• Use descriptive link text that makes sense out of context\n"
        report += "• Avoid all-caps; use bold or emphasis instead\n"
        report += "• Spell out abbreviations on first use\n"
        report += "• Write numbers as numerals (not words) for clarity\n"
        report += "• Keep sentences short and direct\n"
    else:
        report += "\nNo major accessibility issues detected!\n"
        report += "Continue following accessibility best practices.\n"

    return report


@mcp.tool()
def evaluate_tone(text: str, desired_tone: str = "professional and friendly") -> str:
    """
    Evaluate content tone and check if it matches the desired tone.

    Analyzes:
    - Formality level
    - Emotional tone
    - Personality indicators
    - Consistency

    Args:
        text: The content to evaluate
        desired_tone: The tone you're aiming for (e.g., "professional and friendly", "casual", "formal")

    Returns:
        Tone analysis with recommendations
    """
    if not text or not text.strip():
        return "Error: No text provided for tone evaluation"

    text = text.strip().lower()

    # Tone indicators
    formal_words = ['utilize', 'commence', 'terminate', 'endeavor', 'pursuant', 'hereby']
    casual_words = ['cool', 'awesome', 'hey', 'yeah', 'yup', 'nope', 'stuff', 'things']
    friendly_words = ['help', 'easy', 'simple', 'welcome', 'glad', 'happy', 'great', 'thanks']
    cold_words = ['must', 'required', 'mandatory', 'prohibited', 'forbidden', 'denied']

    formal_count = sum(1 for word in formal_words if word in text)
    casual_count = sum(1 for word in casual_words if word in text)
    friendly_count = sum(1 for word in friendly_words if word in text)
    cold_count = sum(1 for word in cold_words if word in text)

    # Check for contractions
    contractions = ["don't", "won't", "can't", "isn't", "aren't", "we'll", "you'll", "it's"]
    contraction_count = sum(1 for contr in contractions if contr in text)

    # Check for exclamation marks
    exclamations = text.count('!')

    # Build analysis
    report = f"""
Tone Analysis
=============
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Desired Tone: {desired_tone}

Tone Indicators:
----------------
• Formal language: {formal_count} instances
• Casual language: {casual_count} instances
• Friendly language: {friendly_count} instances
• Cold/strict language: {cold_count} instances
• Contractions: {contraction_count}
• Exclamation marks: {exclamations}

Assessment:
-----------
"""

    # Determine current tone
    if formal_count > casual_count and cold_count > friendly_count:
        current_tone = "Formal and distant"
        report += f"Current tone: {current_tone}\n"
        report += "Content feels overly formal and cold. Consider:\n"
        report += "  • Using contractions (you'll, we'll)\n"
        report += "  • Adding helpful, supportive language\n"
        report += "  • Simplifying formal words\n"
    elif casual_count > 3:
        current_tone = "Very casual"
        report += f"Current tone: {current_tone}\n"
        report += "Content may be too casual for professional context. Consider:\n"
        report += "  • Replacing slang with standard terms\n"
        report += "  • Maintaining friendliness with clearer language\n"
    elif friendly_count > 2 and contraction_count > 0:
        current_tone = "Professional and friendly"
        report += f"Current tone: {current_tone}\n"
        report += "Great balance! Tone is approachable yet professional.\n"
    elif cold_count > 2:
        current_tone = "Cold and directive"
        report += f"Current tone: {current_tone}\n"
        report += "Content feels strict. Consider:\n"
        report += "  • Explaining WHY something is required\n"
        report += "  • Using 'please' and 'thank you'\n"
        report += "  • Framing as helpful guidance\n"
    else:
        current_tone = "Neutral"
        report += f"Current tone: {current_tone}\n"
        report += "ℹContent is clear but could be more engaging.\n"

    if exclamations > 3:
        report += "\nMany exclamation marks detected. Use sparingly for emphasis.\n"

    return report


@mcp.tool()
def review_error_message(error_text: str) -> str:
    """
    Review error messages for clarity, helpfulness, and actionability.

    Checks:
    - Clear problem statement
    - Explanation of cause
    - Actionable next steps
    - Appropriate tone
    - No jargon or error codes prominently displayed

    Args:
        error_text: The error message to review

    Returns:
        Detailed review with improvement suggestions
    """
    if not error_text or not error_text.strip():
        return "Error: No error message provided for review"

    error_text = error_text.strip()

    issues = []
    suggestions = []

    # Check for error code at the beginning
    if re.match(r'^(Error|ERR|E)\s*\d+', error_text, re.IGNORECASE):
        issues.append("Error code appears first - users won't understand technical codes")
        suggestions.append("Move error codes to the end for support reference")

    # Check for technical jargon
    jargon = ['null pointer', 'exception', 'stack trace', 'timeout', 'gateway', 'protocol', 'authentication failed']
    found_jargon = [term for term in jargon if term.lower() in error_text.lower()]
    if found_jargon:
        issues.append(f"Technical jargon detected: {', '.join(found_jargon)}")
        suggestions.append("Replace technical terms with plain language explanations")

    # Check for actionable steps
    action_indicators = ['try', 'check', 'verify', 'contact', 'refresh', 'restart']
    has_actions = any(word in error_text.lower() for word in action_indicators)
    if not has_actions:
        issues.append("No clear next steps provided")
        suggestions.append("Add specific actions users can take to resolve the issue")

    # Check for explanation
    if len(error_text) < 30:
        issues.append("Message is very brief - may lack context")
        suggestions.append("Explain what happened and why it matters")

    # Check tone
    harsh_words = ['failed', 'invalid', 'incorrect', 'wrong', 'denied']
    found_harsh = [word for word in harsh_words if word.lower() in error_text.lower()]
    if found_harsh and 'please' not in error_text.lower():
        issues.append("Tone feels harsh or blaming")
        suggestions.append("Soften language and offer help rather than blame")

    # Build report
    report = f"""
Error Message Review
====================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Original Message:
{error_text}

Issues Found: {len(issues)}
"""

    if issues:
        report += "\nIssues:\n" + "\n".join(issues)
        report += "\n\nSuggestions:\n" + "\n".join(suggestions)

        report += "\n\nError Message Template:\n"
        report += "[Clear problem description]\n\n"
        report += "This usually happens when:\n"
        report += "• [Common cause 1]\n"
        report += "• [Common cause 2]\n\n"
        report += "What to do:\n"
        report += "1. [Specific action step]\n"
        report += "2. [Alternative if step 1 fails]\n"
        report += "3. [How to get more help]\n\n"
        report += "Error code: [CODE] (for support reference)\n"
    else:
        report += "\nError message looks good!\n"
        report += "It's clear, actionable, and user-friendly.\n"

    return report


@mcp.tool()
def suggest_alternatives(word_or_phrase: str) -> str:
    """
    Suggest simpler, clearer alternatives for complex or jargon-heavy terms.

    Provides plain-language alternatives commonly used in UX writing.

    Args:
        word_or_phrase: The term to find alternatives for

    Returns:
        List of suggested alternatives with usage notes
    """
    if not word_or_phrase or not word_or_phrase.strip():
        return "Error: No word or phrase provided"

    term = word_or_phrase.strip().lower()

    # Dictionary of common UX writing alternatives
    alternatives = {
        'utilize': ['use', 'apply'],
        'commence': ['start', 'begin'],
        'terminate': ['end', 'stop', 'delete'],
        'purchase': ['buy', 'get'],
        'obtain': ['get', 'receive'],
        'facilitate': ['help', 'make easier', 'enable'],
        'endeavor': ['try', 'attempt'],
        'transmit': ['send', 'share'],
        'authenticate': ['sign in', 'log in', 'verify'],
        'configuration': ['settings', 'setup'],
        'execute': ['run', 'start', 'do'],
        'modify': ['change', 'edit', 'update'],
        'designate': ['choose', 'select', 'name'],
        'initiate': ['start', 'begin', 'create'],
        'provision': ['create', 'set up', 'make'],
        'subsequent': ['next', 'following', 'later'],
        'prior to': ['before'],
        'in order to': ['to'],
        'at this point in time': ['now', 'currently'],
        'click here': ['[describe destination]', 'view details', 'learn more about [topic]']
    }

    report = f"""
Alternative Suggestions
=======================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Original: "{word_or_phrase}"
"""

    if term in alternatives:
        report += f"\nSuggested alternatives:\n"
        for i, alt in enumerate(alternatives[term], 1):
            report += f"{i}. {alt}\n"

        report += f"\nTip: Choose the alternative that fits your context best.\n"
        report += "Plain language improves clarity and accessibility.\n"
    else:
        report += f"\nNo pre-defined alternatives found for '{word_or_phrase}'.\n"
        report += "\nGeneral guidelines:\n"
        report += "• Use shorter, common words\n"
        report += "• Choose active voice over passive\n"
        report += "• Be specific and concrete\n"
        report += "• Think about how you'd explain it to a friend\n"

        # Check if it's already simple
        if len(term.split()) <= 2 and len(term) <= 10:
            report += f"\n'{word_or_phrase}' is already fairly simple!\n"

    return report


@mcp.prompt()
def content_review_prompt(content: str, content_type: str = "general") -> list[base.Message]:
    """
    Generate a comprehensive content review prompt for any piece of content.

    Args:
        content: The content to review
        content_type: Type of content (error_message, button_label, onboarding, email, documentation)

    Returns:
        Structured prompt for thorough content review
    """
    prompt_text = f"""
Please review this {content_type} content for UX writing best practices:

Content to review:
---
{content}
---

Review criteria:
1. Clarity - Is the message immediately clear?
2. Readability - Can users scan and understand quickly?
3. Tone - Is it appropriate, friendly, and professional?
4. Actionability - Are next steps clear (if applicable)?
5. Accessibility - Any issues for screen readers or non-native speakers?
6. Conciseness - Can it be shorter without losing meaning?

Use these tools for analysis:
- analyze_readability: Check sentence length and complexity
- check_accessibility: Find accessibility issues
- evaluate_tone: Assess if tone matches brand voice
- review_error_message: (if it's an error message) Check for best practices
- suggest_alternatives: Find simpler word choices

Provide specific, actionable feedback with examples of improvements.
"""

    return [base.UserMessage(prompt_text)]


@mcp.prompt()
def microcopy_suggestions(element_type: str, context: str) -> str:
    """
    Generate microcopy suggestions for UI elements.

    Args:
        element_type: Type of UI element (button, link, empty_state, success_message, placeholder, tooltip)
        context: Description of what the element does or when it appears

    Returns:
        Microcopy suggestions with best practices
    """
    examples = {
        'button': [
            "Be specific: 'Create workspace' not 'Submit'",
            "Use verb + noun: 'Upload file', 'Save changes'",
            "Keep it short: 1-3 words maximum"
        ],
        'link': [
            "Describe the destination: 'View pricing' not 'Click here'",
            "Make it scannable: Links should make sense out of context",
            "Be concise: 'Learn about features' not 'Click here to learn more about our features'"
        ],
        'empty_state': [
            "Start positive: 'No items yet' not 'No items'",
            "Explain the benefit: Tell users what this feature does",
            "Provide clear next action: 'Create your first pipeline'"
        ],
        'success_message': [
            "Confirm the action: 'File uploaded' not just 'Success'",
            "Suggest next steps: What can they do now?",
            "Keep it brief: One line is usually enough"
        ],
        'placeholder': [
            "Show an example: 'marketing-workspace' not 'Enter name'",
            "Be specific: 'your@email.com' not 'Email'",
            "Keep it short: Placeholders should fit in the field"
        ],
        'tooltip': [
            "Explain, don't repeat: Add info not shown in the label",
            "Be concise: 1-2 sentences maximum",
            "Use when needed: Don't tooltip everything"
        ]
    }

    element_type_lower = element_type.lower()

    prompt = f"""
Microcopy for {element_type}
Context: {context}

Best practices for {element_type}:
"""

    if element_type_lower in examples:
        for practice in examples[element_type_lower]:
            prompt += f"\n• {practice}"
    else:
        prompt += "\n• Be clear and specific"
        prompt += "\n• Use simple, familiar words"
        prompt += "\n• Keep it concise"
        prompt += "\n• Make it actionable"

    prompt += f"\n\nSuggested {element_type} text for your context:\n[Analyze context and provide 3-5 specific suggestions]"

    return prompt


def main():
    """
    Main entry point for the Content Design Assistant MCP Server.
    Starts the server with STDIO transport.
    """
    try:
        print("Starting Content Design Assistant MCP Server...", file=sys.stderr)
        print("Server ready to review content and provide UX writing feedback", file=sys.stderr)

        # Run the server
        mcp.run()

    except Exception as e:
        print(f"Failed to start Content Design Assistant: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
