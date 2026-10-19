
import json
import re

# Prompt Engineering
prompt = """
Extract workshop information from the given paragraph.
Return valid JSON with these fields:
title, date, venue, speaker, topics.
If information is missing, use null.
Never invent missing information.
Return JSON only.
"""

# Three test paragraphs
paragraphs = [
    """Title: Generative AI Workshop.
    Date: 20 October 2026.
    Venue: Computer Lab 2.
    Speaker: Dr. Amit Patil.
    Topics: Prompt Engineering, RAG, AI Safety.""",

    """Title: Python Workshop.
    Date: 22 October 2026.
    Venue: Seminar Hall.
    Topics: Python Basics, Functions.""",

    """Title: Cloud Computing Workshop.
    Date: 25 October 2026.
    Venue: Lab 1.
    Speaker: Ms. Neha Shah.
    Topics: Cloud Storage, Virtual Machines."""
]

fields = ["title", "date", "venue", "speaker", "topics"]

def extract_field(text, field):
    pattern = rf"{field}\s*:\s*([^.\n]+)"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None

def extract_information(paragraph):
    result = {}

    for field in fields:
        result[field] = extract_field(paragraph, field)

    # Validate JSON structure
    assert list(result.keys()) == fields
    json_text = json.dumps(result, indent=4)
    json.loads(json_text)  # Check valid JSON

    return result

print("PROMPT:")
print(prompt)

for i, paragraph in enumerate(paragraphs, start=1):
    print(f"\nTEST {i}")
    print("Input:", paragraph)

    output = extract_information(paragraph)
    print("Output JSON:")
    print(json.dumps(output, indent=4))

    missing = [
        field for field, value in output.items()
        if value is None
    ]
    print("Validation:", "PASS" if len(output) == 5 else "FAIL")
    print("Missing fields:", missing)
