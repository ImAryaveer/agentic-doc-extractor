import re
from typing import Literal

# Use a more flexible type hint that allows for an "unknown" category
DocType = Literal["invoice", "medical_bill", "prescription", "unknown"]

# Define keyword sets for clarity and efficiency
# Using more specific and less ambiguous terms
INVOICE_KEYWORDS = {"invoice", "invoice #", "gstin", "subtotal", "amount due", "bill to"}
MEDICAL_BILL_KEYWORDS = {"medical bill", "patient id", "hospital", "discharge summary", "ward", "diagnosis"}
PRESCRIPTION_KEYWORDS = {"rx", "prescription", "dosage", "tablet", "capsule", "dr."}

def rule_based_route(ocr_text: str) -> DocType:
    """
    Routes a document based on a keyword scoring system to improve accuracy.
    """
    if not ocr_text:
        return "unknown"

    t = ocr_text.lower()
    
    # Calculate a score for each document type
    scores = {
        "invoice": sum(1 for keyword in INVOICE_KEYWORDS if keyword in t),
        "medical_bill": sum(1 for keyword in MEDICAL_BILL_KEYWORDS if keyword in t),
        "prescription": sum(1 for keyword in PRESCRIPTION_KEYWORDS if keyword in t)
    }
    
    # Find the document type with the highest score
    # The max function with a key is a clean way to find the winner
    best_match = max(scores, key=scores.get)
    
    # Only return a classification if it has a meaningful score (more than one keyword match)
    # This avoids classifying based on a single stray word.
    if scores[best_match] > 1:
        return best_match
        
    # If no category scores high enough, classify as unknown
    return "unknown"
