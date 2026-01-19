# src/validation/field_validators.py

import re

def validate_dealer_name(name: str) -> str:
    if not name:
        return ""

    # Remove leading/trailing numbers (IDs, phone, fax, etc.)
    name = re.sub(r'^\d+\s*', '', name)
    name = re.sub(r'\s*\d+$', '', name)

    # Remove excessive internal numbers
    name = re.sub(r'\b\d{4,}\b', '', name)

    name = name.strip()

    low = name.lower()

    # Reject descriptor-only lines
    if low.startswith("(") and low.endswith(")"):
        return ""

    banned = ["undertaking", "division", "subsidiary", "govt"]
    if any(b in low for b in banned) and len(name) < 60:
        return ""

    return name


    return name.strip()

def validate_asset_price(price: str) -> str:
    if not price:
        return ""
    try:
        val = int(price)
    except:
        return ""
    return price if 100_000 <= val <= 2_000_000 else ""
