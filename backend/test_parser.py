from app.parser import extract_text_from_pdf

text = extract_text_from_pdf(
    "uploads/AB Resume.pdf"
)

print(text[:3000])