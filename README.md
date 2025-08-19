
# Agentic Document Extraction (Starter)

A minimal, no-notebook Python project that:
1) Reads a PDF/image → OCR
2) Routes doc type (invoice / medical_bill / prescription)
3) Uses OpenAI to extract fields into **structured JSON** with per-field confidence
4) Validates with rules (regex/date/totals)
5) Computes an **overall confidence**
6) Shows everything in **Streamlit**

## Quickstart

### 1) Python + venv
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
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
- **.env**: your secrets (not committed)

### Git Tips (first time)
```bash
git init
git add -A
git commit -m "chore: init project"
# Create an empty GitHub repo, then:
git branch -M main
git remote add origin https://github.com/<you>/agentic-doc-extractor.git
git push -u origin main
```

**Regular commits** example:
```
feat: add OCR
feat: router
feat: OpenAI extraction
feat: validation + confidence
feat: Streamlit UI
docs: README
```

### Invite reviewers on GitHub
Repo → Settings → Collaborators → Add their email/username → Send invite.
(Or keep repo public and share the link.)

### Deploy to Streamlit Cloud (free)
- Connect GitHub → New app → pick repo, branch, `app.py`
- Set Secrets:
```
OPENAI_API_KEY="sk-..."
```
- Deploy.

### Submission
Send your Streamlit URL + GitHub link in email.
