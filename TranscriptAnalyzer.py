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
You are a Conversation reviewer. Your job is to review the conversation and generate feedback for all unique speakers.
The conversation data consists of sentiment as well. Detect the topic of discussion and provide feedback for each speaker.
Respond in a clear text or JSON format.
Conversation:
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


def _call_llm(prompt, transcript):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Transcript:\n{transcript}"}
    ]
    try:
        response = client.chat(model='llama3', messages=messages)
        content = response['message']['content']
        return content
    except Exception as e:
        return f"Error calling LLM: {str(e)}"


def analyze_transcript(transcript):
    """Call center QA evaluation with scoring and complaint type."""
    content = _call_llm(SYSTEM_PROMPT_QA, transcript)
    return extract_json(content)


def generate_call_report(transcript):
    """Conversation review with speaker feedback and topic detection."""
    content = _call_llm(SYSTEM_PROMPT, transcript)
    # Optionally you can try to parse JSON, or just return raw content
    # If you want JSON parsing here, uncomment below:
    # return extract_json(content)
    return content


# Example usage:
if __name__ == "__main__":
    sample_transcript = """
    Agent: Hello, how can I assist you today?
    Customer: My internet speed has been very slow recently.
    Agent: I'm sorry to hear that. Let me check your connection status.
    """
    qa_result = analyze_transcript(sample_transcript)
    print("QA Result:", qa_result)

    review_result = generate_call_report(sample_transcript)
    print("Conversation Review:", review_result)
