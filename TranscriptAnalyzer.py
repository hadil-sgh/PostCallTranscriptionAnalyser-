import ollama
import json
import re

client = ollama.Client()

SYSTEM_PROMPT_QA = """
You are a seasoned Call Center Quality Assurance (QA) expert.

Evaluate the following customer service conversation with two tasks:

1. Rate the agent's performance based on:
  - Empathy
  - Problem-Solving
  - Professionalism

2. Identify the main complaint type from the following list:
- Network Connectivity
- Internet Speed / Data Issues
- Billing & Charges
- Recharge or Balance Problems
- SIM or Number Portability
- Service Activation/Deactivation
- Customer Support Experience
- Account Login / App Issues
- Value-Added Services
- Other

Instructions:
- Assign an overall score from 1 to 5.
- Provide short, constructive feedback.
- Select only one complaint type from the list.
- Respond in this strict JSON format:

{
  "score": <number from 1 to 5>,
  "feedback": "<constructive feedback>",
  "complaint_type": "<one of the categories above>"
}
"""

SYSTEM_PROMPT_REPORT = """
You are a Conversation Reviewer. Your job is to review the conversation and generate detailed feedback for each unique speaker.

Instructions:
- Detect the overall topic of the discussion.
- For each unique speaker, provide feedback focusing on communication effectiveness, clarity, tone, engagement, and any observed issues or strengths.
- Respond ONLY in the following JSON format:

{
  "topic": "<detected topic>",
  "speaker_feedback": {
    "<Speaker1>": "<detailed feedback>",
    "<Speaker2>": "<detailed feedback>"
  }
}
"""

def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to sanitize bad characters
        sanitized = text.replace('\r', '').replace('\t', '\\t').replace('\n', '\\n')

        match = re.search(r'\{.*\}', sanitized, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                return {
                    "score": 0,
                    "feedback": f"Partial JSON parse error after sanitizing: {str(e)}",
                    "complaint_type": "Other"
                }

        return {
            "score": 0,
            "feedback": "No valid JSON found even after sanitizing.",
            "complaint_type": "Other"
        }

def analyze_transcript(transcript):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_QA},
        {"role": "user", "content": f"Transcript:\n{transcript}"}
    ]
    response = client.chat(model='llama3', messages=messages)
    content = response['message']['content']
    return extract_json(content)

def generate_call_report(transcript):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_REPORT},
        {"role": "user", "content": f"Transcript:\n{transcript}"}
    ]
    response = client.chat(model='llama3', messages=messages)
    content = response['message']['content']
    return extract_json(content)
