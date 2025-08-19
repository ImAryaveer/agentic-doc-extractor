
from src.schemas import ExtractedDoc, FieldKV, QAReport
from src.confidence import compute_confidence

def test_conf_boost():
    doc = ExtractedDoc(
        doc_type="invoice",
        fields=[FieldKV(name="Total", value="100", confidence=0.8)],
        overall_confidence=0.0,
        qa=QAReport(passed_rules=["totals_match"], failed_rules=[]),
    )
    out = compute_confidence(doc)
    assert out.overall_confidence >= 0.8
