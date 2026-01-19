from ultralytics import YOLO
from PIL import Image

# Load once (CPU-safe)
_model = YOLO("yolov8n.pt")

def detect_signature_and_stamp(image_path):
    """
    Detects visual regions using YOLO and conservatively assigns
    them to signature / stamp based on spatial evidence.
    """

    img = Image.open(image_path)
    width, height = img.size
    img_area = width * height

    signature = {"present": False, "bbox": []}
    stamp = {"present": False, "bbox": []}

    results = _model(image_path, conf=0.4, device="cpu")

    candidates = []

    for r in results:
        if r.boxes is None:
            continue

        for b in r.boxes:
            x1, y1, x2, y2 = map(int, b.xyxy[0])
            area = (x2 - x1) * (y2 - y1)

            # Reject page-level detections
            if area / img_area > 0.35:
                continue

            # Bottom half only
            if y1 < height * 0.55:
                continue

            candidates.append((x1, y1, x2, y2))

    # Sort bottom-up
    candidates = sorted(candidates, key=lambda b: b[1])

    if len(candidates) >= 1:
        stamp = {
            "present": True,
            "bbox": list(candidates[0])
        }

    if len(candidates) >= 2:
        signature = {
            "present": True,
            "bbox": list(candidates[1])
        }

    return {
        "signature": signature,
        "stamp": stamp
    }
