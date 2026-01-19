import re


def _row_text(row):
    """
    Convert a row of OCR dicts into a single string.
    """
    return " ".join(
        item.get("text", "") for item in row if isinstance(item, dict)
    ).strip()


# -----------------------------
# Dealer Name
# -----------------------------
def extract_dealer_name(rows):
    for row in rows[:10]:
        text = _row_text(row)

        if len(text) < 10:
            continue

        lower = text.lower()

        if any(x in lower for x in ["quotation", "invoice", "bill"]):
            continue

        if any(k in lower for k in [
            "corporation", "limited", "ltd", "pvt", "company", "industries"
        ]):
            return text

    return ""


# -----------------------------
# Model Name
# -----------------------------
def extract_model_name(rows):
    for row in rows:
        text = _row_text(row)

        if "model" in text.lower():
            text = re.sub(r"model\s*[:\-]?", "", text, flags=re.I)
            text = re.sub(r"\b\d+\s*HP\b", "", text, flags=re.I)
            text = re.sub(r"\s+", " ", text).strip()
            return text

    return ""


# -----------------------------
# Horse Power
# -----------------------------
def extract_hp(rows):
    for row in rows:
        text = _row_text(row)

        match = re.search(r"\b(\d{2,3})\s*HP\b", text, flags=re.I)
        if match:
            return match.group(1)

    return ""


# -----------------------------
# Asset Price
# -----------------------------
def extract_price(rows):
    candidates = []

    for row in rows:
        text = _row_text(row)

        numbers = re.findall(r"\b\d{5,8}\b", text)
        for n in numbers:
            candidates.append(int(n))

    if not candidates:
        return ""

    return str(max(candidates))
