# src/ingestion/loader.py

import cv2
import numpy as np
import os


def load_image(image_path: str) -> np.ndarray:
    """
    Load a single PNG image from disk.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    return image


def normalize_orientation(image: np.ndarray) -> np.ndarray:
    """
    Normalize orientation if required.
    (Kept deterministic and lightweight.)
    """
    h, w = image.shape[:2]

    # Placeholder for future rotation logic if needed
    # Currently orientation-agnostic
    return image


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise_image(gray: np.ndarray) -> np.ndarray:
    """
    Apply mild denoising to reduce OCR noise.
    """
    return cv2.fastNlMeansDenoising(gray, h=10)


def enhance_contrast(gray: np.ndarray) -> np.ndarray:
    """
    Improve contrast for better OCR.
    """
    return cv2.adaptiveThreshold(
        gray,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=31,
        C=10
    )


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Full OCR preprocessing pipeline.
    """
    gray = convert_to_grayscale(image)
    gray = denoise_image(gray)
    enhanced = enhance_contrast(gray)
    return enhanced


def ingest_image(image_path: str) -> dict:
    """
    Full ingestion pipeline for a single PNG image.
    Returns intermediate representations for explainability.
    """
    image = load_image(image_path)
    image = normalize_orientation(image)
    ocr_ready = preprocess_for_ocr(image)

    return {
        "original": image,
        "ocr_ready": ocr_ready,
        "height": image.shape[0],
        "width": image.shape[1]
    }
