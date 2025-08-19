import os
import cv2
import numpy as np
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from typing import Tuple, List

# Define supported image extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

def _process_image(path: str) -> Tuple[str, List[np.ndarray]]:
    """
    Extracts text from a single image file using OCR.
    """
    try:
        img = cv2.imread(path)
        if img is None:
            return "", []
        text = pytesseract.image_to_string(img)
        # Return the text and the image itself in a list
        return text, [img]
    except Exception as e:
        print(f"Error processing image {path}: {e}")
        return "", []

def _process_pdf(path: str) -> Tuple[str, List[np.ndarray]]:
    """
    Extracts text from each page of a PDF.
    - Tries direct text extraction first.
    - Falls back to OCR if a page has no selectable text.
    """
    texts = []
    images = []
    try:
        # Use pdf2image to get all pages as PIL images
        pil_images = convert_from_path(path, dpi=300)
        
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Attempt to extract text directly
                extracted_text = page.extract_text() or ""
                
                # If direct extraction fails or is empty, use OCR on the corresponding image
                if not extracted_text.strip():
                    pil_img = pil_images[i]
                    # Convert PIL image to OpenCV format for Tesseract
                    img_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    ocr_text = pytesseract.image_to_string(img_cv)
                    texts.append(ocr_text)
                    images.append(img_cv)
                else:
                    texts.append(extracted_text)
                    # Still add the image for potential display purposes
                    pil_img = pil_images[i]
                    img_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    images.append(img_cv)

    except Exception as e:
        print(f"Error processing PDF {path}: {e}")
        return "", []

    return "\n".join(texts), images

def extract_text_from_document(path: str) -> Tuple[str, List[np.ndarray]]:
    """
    Main function to extract text from a document (PDF or image).
    Routes the file to the appropriate processor based on its extension.
    """
    _, extension = os.path.splitext(path.lower())
    
    if extension == ".pdf":
        return _process_pdf(path)
    elif extension in IMAGE_EXTENSIONS:
        return _process_image(path)
    else:
        print(f"Unsupported file type: {extension}")
        return "", []