# 📑 Document AI for Invoice Field Extraction

An end-to-end **Document AI system** that extracts structured information from **multilingual invoice images** using a combination of **OCR, Computer Vision, and NLP**, designed with **accuracy, explainability, and low-cost deployment** in mind.

This project simulates real-world **banking and financial document automation** workflows, handling noisy, scanned, photographed, and handwritten invoice documents.

---

##  Key Features

- Multilingual OCR-based text extraction
- Layout-aware key–value field detection
- Visual detection of dealer signatures and stamps
- Rule-based validation and semantic consistency checks
- Explainable outputs with confidence scoring
- Low-cost, CPU-friendly inference pipeline
- Reproducible, modular, production-style codebase

---

## 📌 Fields Extracted

For each invoice document, the system extracts:

- **Dealer Name** (fuzzy-matched)
- **Model Name** (exact match)
- **Horse Power (HP)** (numeric)
- **Asset Cost** (numeric)
- **Dealer Signature** (presence + bounding box)
- **Dealer Stamp** (presence + bounding box)

The final output is a structured JSON with confidence scores, processing time, and cost estimation.

---

## 🏗️ System Architecture

The system follows a modular, explainable pipeline:

1. **Image Ingestion & Preprocessing**
2. **OCR & Layout Extraction**
3. **Visual and Textual Understanding**
4. **Field Detection & Entity Recognition**
5. **Semantic Reasoning & Validation**
6. **Confidence Scoring**
7. **Structured JSON Output**

Each component is independently evaluated to balance accuracy, latency, and cost.

---

## 🔍 Explainability

Explainability is a core design principle of this system:

- Each extracted field is traceable to its **source text region**
- Bounding box coordinates are preserved
- OCR confidence and detection scores are stored
- Rule-based decisions are explicitly logged

This ensures transparency, debuggability, and production readiness.

---

## 📊 Exploratory Data Analysis (EDA)

Separate EDA notebooks analyze:
- Document types (scanned, photographed, digital)
- Language distribution
- OCR confidence patterns
- Field-wise error trends
- Latency and cost distributions

These insights guide system design and optimization.

---

## ⚙️ Tech Stack

- **OCR:** PaddleOCR (multilingual, CPU-friendly)
- **Computer Vision:** YOLO (lightweight model for stamp/signature detection)
- **NLP:** Rule-based + fuzzy matching + optional small language models
- **Language:** Python
- **Deployment:** CPU-first, low-cost inference

---

## 📂 Project Structure

```text
multilingual-invoice-document-vision-ai/
│
├── executable.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── explore/           # ~50 invoices (EDA & inspection)
│   │   ├── dev/               # ~350 invoices (development)
│   │   └── holdout/           # ~95 invoices (internal evaluation)
│   │
│   ├── samples/               # 2–3 demo images
│   │
│   └── README.md
│
├── eda/
│   └── eda.ipynb
│
├── src/
│   ├── ingestion/
│   ├── ocr/
│   ├── layout/
│   ├── extraction/
│   ├── vision/
│   ├── validation/
│   └── utils/
│
├── models/
│   └── yolo.pt
│
└── sample_output/
    └── result.json

````

---

## ▶️ How to Run

```bash
python executable.py <input_image_folder>
```

The system processes all images in the folder and generates a structured JSON output.

---

## 📈 Evaluation Metrics

* **Document-Level Accuracy (DLA)**
* **Inference Latency**
* **Estimated Cost per Document**
* **Explainability & Robustness**

---

## 📌 Notes

* Designed for real-world deployment constraints
* Modular and extensible for additional document types
* Emphasizes system reliability over black-box modeling

---
