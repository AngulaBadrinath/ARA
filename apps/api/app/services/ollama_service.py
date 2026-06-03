from ollama import chat
import json


def analyze_resume(resume_text: str):
    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze this resume.

IMPORTANT:
Return ONLY raw JSON.
Do NOT wrap JSON in markdown.
Do NOT use ```json.
Do NOT provide explanations.

Format:

{{
    "summary": "short summary",
    "skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "ats_score": 0
}}

Resume:

{resume_text}
"""
            }
        ],
    )

    content = response["message"]["content"]

    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    try:
        return json.loads(content)

    except Exception:
        return {
            "summary": "Parsing failed",
            "skills": [],
            "missing_skills": [],
            "ats_score": 0,
            "raw": content,
        }