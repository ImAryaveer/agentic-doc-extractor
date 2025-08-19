
import re
from typing import Tuple
from .schemas import ExtractedDoc

_money = re.compile(r"^\s?\d+(\.\d{1,2})?\s?$")
_date  = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b")

def _get(doc: ExtractedDoc, name: str):
    for f in doc.fields:
        if f.name.lower() == name.lower():
            return f.value
    return None

def run_rules(doc: ExtractedDoc) -> Tuple[list,list,list]:
    passed, failed, notes = [], [], []

    # money format
    if (v:=_get(doc,"Total")) and _money.match(str(v)):
        passed.append("total_money")
    else:
        failed.append("total_money")

    # date fields
    for candidate in ["InvoiceDate","BillDate","Date"]:
        v = _get(doc, candidate)
        if v is None:
            continue
        if _date.match(str(v)):
            passed.append(f"{candidate}_date")
        else:
            failed.append(f"{candidate}_date")

    # subtotal + tax ~= total
    sub, tax, total = _get(doc,"Subtotal"), _get(doc,"Tax"), _get(doc,"Total")
    try:
        if sub and tax and total and abs((float(sub) + float(tax)) - float(total)) < 0.05:
            passed.append("totals_match")
        else:
            failed.append("totals_match")
    except Exception:
        failed.append("totals_match")

    return passed, failed, notes
