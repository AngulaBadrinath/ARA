from ollama import chat


def analyze_resume(resume_text: str):
    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze this resume.

Return:
1. Summary
2. Key Skills
3. Missing Skills
4. ATS Score out of 100

Resume:

{resume_text}
""",
            }
        ],
    )

    return response["message"]["content"]