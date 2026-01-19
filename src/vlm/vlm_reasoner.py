# src/vlm/vlm_reasoner.py

import json

class VLMReasoner:
    def __init__(self):
        self.available = False

        try:
            import torch
            from transformers import AutoProcessor, AutoModelForVision2Seq

            MODEL_ID = "Qwen/Qwen2.5-VL-2B-Instruct"

            self.processor = AutoProcessor.from_pretrained(MODEL_ID)
            self.model = AutoModelForVision2Seq.from_pretrained(
                MODEL_ID,
                torch_dtype=torch.float16,
                device_map="auto"
            ).eval()

            self.available = True

        except Exception as e:
            # VLM not available locally (CPU / Windows)
            self.available = False

    def reason(self, image, ocr_rows):
        if not self.available:
            return {}

        ocr_text = "\n".join(
            [" ".join([w["text"] for w in row]) for row in ocr_rows]
        )

        prompt = f"""
Extract the following fields from the invoice.
Return ONLY valid JSON. If missing, return empty string.

Fields:
- dealer_name
- model_name
- horse_power
- asset_price

OCR TEXT:
{ocr_text}
"""

        inputs = self.processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=256)

        decoded = self.processor.batch_decode(output, skip_special_tokens=True)[0]

        try:
            s = decoded.find("{")
            e = decoded.rfind("}") + 1
            return json.loads(decoded[s:e])
        except Exception:
            return {}
