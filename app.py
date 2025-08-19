
import os, json, streamlit as st
from dotenv import load_dotenv
from src.ocr import pdf_to_text_and_images
from src.router import rule_based_route
from src.extractor import extract_fields
from src.validator import run_rules
from src.confidence import compute_confidence
from src.schemas import ExtractedDoc
from src.utils import save_json

load_dotenv()
st.set_page_config(page_title="Agentic Document Extraction", layout="wide")
st.title("Agentic Document Extraction")

uploaded = st.file_uploader("Upload PDF or image", type=["pdf","png","jpg","jpeg"])
field_hint = st.text_area("Optional: custom fields (comma separated)", "")

if uploaded:
    raw_path = f"data/raw/{uploaded.name}"
    with open(raw_path, "wb") as f: f.write(uploaded.read())

    with st.spinner("Reading / OCR…"):
        text, images = pdf_to_text_and_images(raw_path)

    st.subheader("Preview")
    st.write((text[:1500] + "…") if len(text) > 1500 else text)

    doc_type = rule_based_route(text)
    st.info(f"Detected document type: **{doc_type}**")

    if field_hint.strip():
        text = f"[FIELDS:{field_hint}]\n" + text

    with st.spinner("Extracting with LLM…"):
        doc: ExtractedDoc = extract_fields(doc_type, text)

    passed, failed, notes = run_rules(doc)
    doc.qa.passed_rules = passed
    doc.qa.failed_rules = failed
    doc.qa.notes = f"{len([f for f in doc.fields if (f.confidence or 0)<0.5])} low-confidence fields"

    doc = compute_confidence(doc)

    st.subheader("Results (JSON)")
    st.code(json.dumps(doc.model_dump(), indent=2), language="json")

    st.subheader("Confidence")
    st.metric("Overall", f"{doc.overall_confidence:.2f}")
    for f in doc.fields:
        st.progress(min(max(f.confidence or 0, 0), 1.0), text=f"{f.name}: {f.confidence or 0:.2f}")

    if st.button("Save JSON"):
        out = f"data/outputs/{os.path.splitext(uploaded.name)[0]}.json"
        save_json(doc.model_dump(), out)
        st.success(f"Saved to {out}")
