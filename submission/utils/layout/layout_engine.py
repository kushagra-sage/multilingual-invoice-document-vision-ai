# src/layout/layout_engine.py

from typing import List, Dict

def normalize_bbox(bbox):
    """
    Convert 4-point bbox to (x_min, y_min, x_max, y_max)
    """
    xs = [p[0] for p in bbox]
    ys = [p[1] for p in bbox]
    return min(xs), min(ys), max(xs), max(ys)


def sort_by_vertical_position(ocr_lines: List[Dict]) -> List[Dict]:
    """
    Sort OCR lines from top to bottom using bbox y_min.
    """
    for line in ocr_lines:
        x_min, y_min, x_max, y_max = normalize_bbox(line["bbox"])
        line["x_min"] = x_min
        line["y_min"] = y_min
        line["x_max"] = x_max
        line["y_max"] = y_max

    return sorted(ocr_lines, key=lambda x: x["y_min"])


def group_lines_into_rows(
    ocr_lines: List[Dict],
    y_threshold: int = 15
) -> List[List[Dict]]:
    """
    Group OCR lines into horizontal rows based on vertical proximity.
    """
    rows = []
    current_row = []

    for line in ocr_lines:
        if not current_row:
            current_row.append(line)
            continue

        prev_line = current_row[-1]

        if abs(line["y_min"] - prev_line["y_min"]) <= y_threshold:
            current_row.append(line)
        else:
            rows.append(current_row)
            current_row = [line]

    if current_row:
        rows.append(current_row)

    return rows
