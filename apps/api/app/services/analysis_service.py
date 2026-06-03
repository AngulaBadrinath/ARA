from app.services.resume_parser import extract_text_from_pdf
from app.services.ollama_service import analyze_resume


def analyze_pdf(file_path: str):
    text = extract_text_from_pdf(file_path)

    result = analyze_resume(text)

    return {
        "resume_text": text,
        "analysis": result,
    }