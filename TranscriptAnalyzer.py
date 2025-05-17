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


SYSTEM_PROMPT = """
 You are Conversation reviewer. Your Job is to review the conversation based on the review. Generate the Feedback of all unique speakers.
        The conversation data consists of sentiment as well. So you need to detect the topic of discussion and feedback for each speaker.
        conversation:

"""



def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e:
                return {
                    "score": 0,
                    "feedback": f"Partial JSON parse error: {str(e)}",
                    "complaint_type": "Other"
                }
        return {
            "score": 0,
            "feedback": "No valid JSON found in LLM response.",
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

def Generate_Call_Report(transcript):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Transcript:\n{transcript}"}
    ]

    response = client.chat(model='llama3', messages=messages)
    content = response['message']['content']

    return extract_json(content)
