import sys
import json
import time
import os
from PIL import Image

from src.ingestion.loader import ingest_image
from src.ocr.ocr_engine import run_ocr
from src.layout.layout_engine import (
    sort_by_vertical_position,
    group_lines_into_rows
)

from src.extraction.field_extractor import (
    extract_dealer_name,
    extract_model_name,
    extract_hp,
    extract_price
)

from src.validation.field_validators import (
    validate_dealer_name,
    validate_asset_price
)

from src.vision.yolo.detector import detect_signature_and_stamp
from src.validation.confidence import compute_confidence
from src.vlm.consistency_checker import VLMConsistencyChecker


# ===================== CONFIG =====================
OUTPUT_DIR = "final_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# =================================================


def estimate_cost_usd():
    # Offline inference, no paid APIs
    return 0.0


def main():
    if len(sys.argv) < 2:
        print("Usage: python executable.py <path_to_image.png>")
        sys.exit(1)

    image_path = sys.argv[1]
    start_time = time.time()

    # -------------------------------
    # STEP 4: Ingestion
    # -------------------------------
    ingested = ingest_image(image_path)

    # -------------------------------
    # STEP 5: OCR
    # -------------------------------
    ocr_output = run_ocr(ingested["ocr_ready"])

    # -------------------------------
    # STEP 6: Layout
    # -------------------------------
    sorted_lines = sort_by_vertical_position(ocr_output)
    rows = group_lines_into_rows(sorted_lines)

    # -------------------------------
    # STEP 7: Field extraction
    # -------------------------------
    dealer_raw = extract_dealer_name(rows)
    model_raw = extract_model_name(rows)
    hp_raw = extract_hp(rows)
    price_raw = extract_price(rows)

    dealer_name = validate_dealer_name(dealer_raw)
    asset_cost = validate_asset_price(price_raw)

    fields = {
        "dealer_name": dealer_name,
        "model_name": model_raw,
        "horse_power": int(hp_raw) if str(hp_raw).isdigit() else None,
        "asset_cost": int(asset_cost) if str(asset_cost).isdigit() else None
    }

    # -------------------------------
    # STEP 8: CV (YOLO) bbox detection
    # -------------------------------
    visual_elements = detect_signature_and_stamp(image_path)

    # -------------------------------
    # STEP 9: VLM-based confidence
    # -------------------------------
    image_pil = Image.open(image_path)
    vlm_checker = VLMConsistencyChecker()
    vlm_score = vlm_checker.check(image_pil, fields)

    confidence = compute_confidence(
        ocr_output=ocr_output,
        fields=fields,
        visual_elements=visual_elements,
        vlm_consistency=vlm_score
    )

    # -------------------------------
    # FINAL OUTPUT
    # -------------------------------
    result = {
        "doc_id": os.path.basename(image_path),
        "fields": {
            **fields,
            "signature": visual_elements["signature"],
            "stamp": visual_elements["stamp"]
        },
        "confidence": confidence,
        "processing_time_sec": round(time.time() - start_time, 3),
        "cost_estimate_usd": estimate_cost_usd()
    }

    output_path = os.path.join(
        OUTPUT_DIR,
        os.path.splitext(os.path.basename(image_path))[0] + ".json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Saved → {output_path}")


if __name__ == "__main__":
    main()
