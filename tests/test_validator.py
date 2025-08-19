
from src.schemas import ExtractedDoc, FieldKV, QAReport
from src.validator import run_rules

def test_totals_match():
    doc = ExtractedDoc(
        doc_type="invoice",
        fields=[
            FieldKV(name="Subtotal", value="90", confidence=0.8),
            FieldKV(name="Tax", value="10", confidence=0.8),
            FieldKV(name="Total", value="100", confidence=0.9),
        ],
        overall_confidence=0.0,
        qa=QAReport(),
    )
    p, f, _ = run_rules(doc)
    assert "totals_match" in p
