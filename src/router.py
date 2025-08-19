import re
from typing import Literal

DocType = Literal["invoice", "medical_bill", "prescription"]

def rule_based_route(ocr_text: str) -> DocType:
    t = (ocr_text or "").lower()
    if any(k in t for k in ["invoice", "gst", "subtotal", "tax", "amount due"]):
        return "invoice"
    if any(k in t for k in ["medical bill", "patient id", "ipd", "hospital", "discharge"]):
        return "medical_bill"
    if any(k in t for k in ["rx", "prescription", "dosage", "tablet", "mg", "dr."]):
        return "prescription"
    if re.search(r"bill|total", t):
        return "invoice"
    return "prescription"