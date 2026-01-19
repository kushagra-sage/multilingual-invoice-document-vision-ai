import re

def normalize_ocr_text(text: str) -> str:
    """
    Fix common OCR mistakes safely.
    """
    # O → 0 only when surrounded by digits or before HP
    text = re.sub(r'(?<=\d)O(?=\s*HP)', '0', text)
    text = re.sub(r'(?<=\d)O(?=\d)', '0', text)

    # Extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
