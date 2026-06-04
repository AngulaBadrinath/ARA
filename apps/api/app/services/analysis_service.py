from app.services.resume_parser import extract_text_from_pdf
from app.services.ollama_service import analyze_resume


def analyze_text(text: str):
    return analyze_resume(text)