
from pydantic import BaseModel, Field
from typing import List, Optional

class SourceRef(BaseModel):
    page: int
    bbox: List[float]  # [x1,y1,x2,y2]

class FieldKV(BaseModel):
    name: str
    value: Optional[str] = None
    confidence: float = 0.0
    source: Optional[SourceRef] = None

class QAReport(BaseModel):
    passed_rules: List[str] = []
    failed_rules: List[str] = []
    notes: Optional[str] = None

class ExtractedDoc(BaseModel):
    doc_type: str
    fields: List[FieldKV]
    overall_confidence: float
    qa: QAReport
