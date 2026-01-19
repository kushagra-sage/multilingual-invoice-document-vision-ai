# src/vlm/consistency_checker.py

from transformers import AutoProcessor, AutoModelForVision2Seq
import torch

class VLMConsistencyChecker:
    def __init__(self, model_name="Qwen/Qwen2.5-VL-2B"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )

    def check(self, image, fields):
        """
        Returns a score in [0,1] based on semantic consistency.
        """

        prompt = f"""
You are validating extracted invoice fields.

Dealer name: {fields.get("dealer_name")}
Model name: {fields.get("model_name")}
Horse power: {fields.get("horse_power")}
Asset cost: {fields.get("asset_cost")}

For each field, answer Yes or No if it looks valid and consistent.
Respond in JSON with keys:
dealer_valid, model_valid, hp_valid, price_valid
"""

        inputs = self.processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        ).to(self.device)

        output = self.model.generate(
            **inputs,
            max_new_tokens=200
        )

        response = self.processor.batch_decode(
            output,
            skip_special_tokens=True
        )[0]

        # Simple parsing
        score = 0
        if "dealer_valid" in response and "Yes" in response:
            score += 0.25
        if "model_valid" in response and "Yes" in response:
            score += 0.25
        if "hp_valid" in response and "Yes" in response:
            score += 0.25
        if "price_valid" in response and "Yes" in response:
            score += 0.25

        return score
