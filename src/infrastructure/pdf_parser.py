import pdfminer.high_level

def parse_pdf(file_path: str) -> str:
    text = pdfminer.high_level.extract_text(file_path)
    return text