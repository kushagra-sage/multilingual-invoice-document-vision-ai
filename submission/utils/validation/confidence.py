def compute_confidence(
    ocr_output,
    fields,
    visual_elements,
    vlm_consistency=None
):
    """
    Confidence is derived from:
    - OCR certainty
    - Field completeness
    - Visual evidence presence
    - Optional VLM reasoning
    """

    if not ocr_output:
        return 0.0

    # 1️⃣ OCR confidence
    avg_ocr_conf = sum(w["confidence"] for w in ocr_output) / len(ocr_output)

    # 2️⃣ Field completeness
    required = ["dealer_name", "model_name", "horse_power", "asset_cost"]
    completeness = sum(bool(fields.get(k)) for k in required) / len(required)

    # 3️⃣ Visual evidence
    visual_score = 0.0
    if visual_elements["signature"]["present"]:
        visual_score += 0.5
    if visual_elements["stamp"]["present"]:
        visual_score += 0.5

    # 4️⃣ Optional VLM semantic check
    vlm_score = 0.0
    if vlm_consistency is not None:
        vlm_score = vlm_consistency  # already ∈ [0,1]

    confidence = (
        0.45 * avg_ocr_conf +
        0.30 * completeness +
        0.15 * visual_score +
        0.10 * vlm_score
    )

    return round(min(confidence, 0.95), 2)
