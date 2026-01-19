# 📊 Error Analysis – Field Extraction 

## 🔍 Objective

Analyze extraction errors across multiple invoice layouts to:

* Understand failure patterns
* Justify heuristic-based approach
* Guide iterative improvements

---

## 🧪 Sample-wise Comparison Table

| Document ID              | Dealer Name (Extracted)                            | Model Name (Extracted)                    | HP (Extracted) | Price (Extracted) | Key Issues Observed                                                            |
| ------------------------ | -------------------------------------------------- | ----------------------------------------- | -------------- | ----------------- | ------------------------------------------------------------------------------ |
| **172561841_pg1.png**    | ❌ *(A Govt. of Odisha Undertaking)*                | ⚠️ *Model:-DI-745 IIl HDM+4WD 5O HP*      | ❌              | ✅ *2570687*       | Dealer tagline picked instead of company name; HP embedded inside model string |
| **172566189_1_pg10.png** | ✅ *LEADING AGRI EVOLUTION*                         | ❌                                         | ✅ *55*         | ❌                 | Model name missing; price not explicitly labeled                               |
| **172585685_3_pg1.png**  | ⚠️ *mahindra Authorised Dealer-Mahindra Tractors…* | ⚠️ *Mahindra Tractor Model YuN.D.TE.C.H…* | ❌              | ❌                 | Dealer name noisy; HP absent or embedded; price in table format                |

---

## 🧠 Observations (What We Learned)

### 1️⃣ Dealer Name

* Works well when **clearly stated**
* Fails when:

  * Government taglines appear above company name
  * “Authorised Dealer” lines mix brand + address

📌 **Root cause:** Header ambiguity + multiple long text candidates

---

### 2️⃣ Model Name

* Sometimes includes **HP inside the model string**
* OCR merges model + specs due to layout proximity

📌 **Root cause:** No post-processing to split composite strings

---

### 3️⃣ Horse Power (HP)

* Extracted only when **explicitly labeled**
* Missed when:

  * Embedded inside model name
  * Written as `5O HP` (OCR misread `50`)

📌 **Root cause:** OCR noise + limited regex patterns

---

### 4️⃣ Asset Price

* Works when keywords like **TOTAL / AMOUNT** exist
* Fails when price appears:

  * Inside tables
  * Without currency keywords

📌 **Root cause:** Layout-dependent numeric extraction

---

## 🛠️ Planned Improvements (Iterative Strategy)

| Issue                    | Planned Fix                                            |
| ------------------------ | ------------------------------------------------------ |
| Dealer tagline confusion | Penalize phrases like “Govt. of”, “Authorised Dealer”  |
| HP inside model          | Post-process model string → extract embedded HP        |
| OCR errors (5O vs 50)    | Digit normalization (`O → 0`)                          |
| Price in tables          | Row-based numeric clustering + largest-value heuristic |

> ⚠️ These improvements are **rule-based by design** to maintain explainability.

---
