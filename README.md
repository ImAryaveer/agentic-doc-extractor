# 📄 Agentic Document Extraction

An AI-powered system that:  
1. 🖼️ Reads **PDFs / images** with OCR  
2. 🔎 Detects document type *(invoice / medical bill / prescription)*  
3. 🤖 Uses OpenAI to extract fields into **structured JSON** (with per-field confidence)  
4. ✅ Validates extracted data (regex, totals check, date rules)  
5. 📊 Computes an **overall confidence score**  
6. 🎨 Provides an interactive **Streamlit UI**  

---

## 🚀 Live Demo
🔗 Streamlit Cloud: [App Link](agentic-doc-extractor-rnaqsgqndngl9qwujav8f7
.streamlit.app)  
💻 GitHub Repo: [agentic-doc-extractor](https://github.com/ImAryaveer/agentic-doc-extractor)  

---

## ⚡ Quickstart (Local)

### 1. Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# or .venv\Scripts\activate # Windows

```

### 2) Install system deps
- **Tesseract** (OCR engine)
  - macOS: `brew install tesseract`
  - Ubuntu: `sudo apt-get update && sudo apt-get install -y tesseract-ocr poppler-utils`
  - Windows: Download Tesseract installer; add to PATH.
- (Optional) **Poppler** for high-quality PDF rendering.

### 3) Install Python deps
```bash
pip install -r requirements.txt
```

### 4) OpenAI key
Create `.env` with:
```
OPENAI_API_KEY=sk-...
```

### 5) Run the app
```bash
streamlit run app.py
```

Upload a PDF/image; see detected type, extracted fields (with confidences), rule checks, and overall score.

---

## Project Structure

```
agentic-doc-extractor/
├─ app.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ .gitignore
├─ src/
│  ├─ __init__.py
│  ├─ router.py
│  ├─ ocr.py
│  ├─ extractor.py
│  ├─ schemas.py
│  ├─ validator.py
│  ├─ confidence.py
│  └─ utils.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_validator.py
│  └─ test_confidence.py
└─ data/
   ├─ raw/        # put your local PDFs/images here (not committed if sensitive)
   ├─ outputs/    # JSON outputs
   └─ samples/    # tiny, license-safe samples
```

### Folder explanations (super short)
- **src/**: all Python logic
- **data/**: your docs + outputs
- **tests/**: tiny unit tests
- **app.py**: Streamlit UI entry
- **requirements.txt**: pip deps
- **.env**: Your secrets (not committed)

📊 Example Output (Invoice)

{
  "doc_type": "invoice",
  "fields": [
    {"name": "InvoiceNumber", "value": "MTFG6YJG0002", "confidence": 0.9},
    {"name": "InvoiceDate", "value": "July 27, 2025", "confidence": 0.9},
    {"name": "Subtotal", "value": "$13.82", "confidence": 0.9},
    {"name": "Tax", "value": null, "confidence": 0.0},
    {"name": "Total", "value": "$8.82", "confidence": 0.9}
  ],
  "overall_confidence": 0.75,
  "qa": {
    "passed_rules": [],
    "failed_rules": ["total_money","InvoiceDate_date","totals_match"],
    "notes": "1 low-confidence fields"
  }
}


🧪 Validation Rules

totals_match → Subtotal + Tax = Total

date_valid → Date parses correctly & is not a future date

required_fields → All expected fields extracted

✅ Submission Checklist

 Regular commits on GitHub

 Public Streamlit Cloud demo link

 At least 3 document types tested (invoice, medical bill, prescription)

 JSON outputs saved in /data/outputs/

 Clear README








