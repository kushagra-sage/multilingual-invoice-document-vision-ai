# src/ocr/ocr_engine.py

import os
import numpy as np

# 🔒 HARD disable E2E BEFORE PaddleOCR import
os.environ["PADDLEOCR_E2E"] = "0"

from paddleocr import PaddleOCR
from src.utils.ocr_normalizer import normalize_ocr_text


# ======================================================
# Initialize OCR engine ONCE (global, cached)
# ======================================================
ocr_engine = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    det=True,
    rec=True,
    cls=True,
    show_log=False
)


def run_ocr(ocr_ready_image: np.ndarray) -> list:
    """
    Run OCR on a preprocessed image.

    Returns:
        List[Dict] with:
        - text (normalized)
        - bbox (4-point polygon)
        - confidence (float)
    """

    result = ocr_engine.ocr(ocr_ready_image)

    outputs = []

    if not result or not result[0]:
        return outputs

    for line in result[0]:
        bbox = line[0]                  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        raw_text = line[1][0]
        confidence = float(line[1][1])

        # ✅ APPLY OCR NORMALIZATION HERE (CRITICAL FIX)
        text = normalize_ocr_text(raw_text)

        outputs.append({
            "text": text,
            "bbox": bbox,
            "confidence": confidence
        })

    return outputs
