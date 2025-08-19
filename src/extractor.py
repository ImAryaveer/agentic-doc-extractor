
import os, json
from typing import Dict, Any, List
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv 
from .schemas import ExtractedDoc, FieldKV, QAReport

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _expected_fields(doc_type: str) -> List[str]:
    return {
        "invoice": ["InvoiceNumber","InvoiceDate","VendorName","Subtotal","Tax","Total"],
        "medical_bill": ["PatientName","PatientID","BillDate","HospitalName","Total","Discount"],
        "prescription": ["PatientName","DoctorName","Date","MedicineList","DosageInstructions"]
    }.get(doc_type, ["Total"])

def extract_fields(doc_type: str, full_text: str) -> ExtractedDoc:
    expected = _expected_fields(doc_type)
    system = (
        "You are an extraction engine. Return ONLY JSON with this shape:\n"
        "{ \"fields\": [ { \"name\": str, \"value\": str|null, \"confidence\": float (0-1), "
        "\"source\": { \"page\": int, \"bbox\": [x1,y1,x2,y2] } | null } ] }\n"
        f"Document type: {doc_type}. Include all expected field names even if value is null."
    )
    user = f"Expected fields: {expected}. Document text:\n{full_text[:8000]}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    obj = json.loads(resp.choices[0].message.content or "{}")
    got = { (f.get("name") or ""): f for f in obj.get("fields", []) if isinstance(f, dict) }
    fields = []
    for name in expected:
        f = got.get(name) or {"name": name, "value": None, "confidence": 0.0, "source": None}
        # coerce confidence
        try:
            c = float(f.get("confidence", 0.0))
        except Exception:
            c = 0.0
        f["confidence"] = max(0.0, min(1.0, c))
        fields.append(FieldKV(**f))
    doc = ExtractedDoc(doc_type=doc_type, fields=fields, overall_confidence=0.0, qa=QAReport())
    return doc
