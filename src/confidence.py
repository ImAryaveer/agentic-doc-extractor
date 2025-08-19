
from statistics import mean
from .schemas import ExtractedDoc

def compute_confidence(doc: ExtractedDoc) -> ExtractedDoc:
    base = [f.confidence for f in doc.fields if (f.confidence or 0) > 0]
    model_score = mean(base) if base else 0.0
    rule_bonus = 0.05 * len(doc.qa.passed_rules) - 0.05 * len(doc.qa.failed_rules)
    overall = max(0.0, min(1.0, model_score + rule_bonus))
    doc.overall_confidence = overall
    return doc
