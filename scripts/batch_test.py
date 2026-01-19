# scripts/batch_test.py

import subprocess
import sys
from pathlib import Path

IMAGE_DIR = Path("data/raw/explore")

images = list(IMAGE_DIR.glob("*.png"))
print(f"Found {len(images)} images")

python_executable = sys.executable  # 🔥 THIS IS THE KEY FIX

for img in images:
    print(f"\nRunning OCR on: {img.name}")
    print("=" * 60)

    subprocess.run(
        [python_executable, "executable.py", str(img)],
        check=False
    )
