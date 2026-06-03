from app.services.resume_parser import extract_text_from_pdf
from app.services.ollama_service import analyze_resume

print("Reading PDF...")
text = extract_text_from_pdf(
    r"C:\Projects\ARA\backend\uploads\AB Resume.pdf"
)

print("PDF extracted successfully")
print(f"Characters: {len(text)}")

print("Sending to Ollama...")
result = analyze_resume(text)

print("=== ANALYSIS ===")
print(result)