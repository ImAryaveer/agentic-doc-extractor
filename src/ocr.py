# pytesseract wala code hai ye 

# import pdfplumber, pytesseract, cv2, numpy as np
# from pdf2image import convert_from_path

# def pdf_to_text_and_images(path: str):
#     texts, images = [], []
#     try:
#         with pdfplumber.open(path) as pdf:
#             for i, page in enumerate(pdf.pages):
#                 t = page.extract_text() or ""
#                 if not t.strip():
#                     pil_img = convert_from_path(path, first_page=i+1, last_page=i+1, dpi=300)[0]
#                     img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
#                     ocr = pytesseract.image_to_string(img)
#                     texts.append(ocr)
#                     images.append(img)
#                 else:
#                     texts.append(t)
#                     pil_img = convert_from_path(path, first_page=i+1, last_page=i+1, dpi=200)[0]
#                     images.append(cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))
#     except Exception:
#         # If it's actually an image file, OCR directly
#         img = cv2.imread(path)
#         ocr = pytesseract.image_to_string(img) if img is not None else ""
#         texts.append(ocr)
#         images.append(img)
#     return "\n".join(texts), images ,

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pdfplumber
from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

def pdf_to_text_and_images(path: str):
    texts, images = [], []
    try:
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                t = page.extract_text() or ""
                if not t.strip():
                    pil_img = convert_from_path(path, first_page=i+1, last_page=i+1, dpi=300)[0]
                    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                    ocr = " ".join(reader.readtext(np.array(pil_img), detail=0))
                    texts.append(ocr)
                    images.append(img)
                else:
                    texts.append(t)
                    pil_img = convert_from_path(path, first_page=i+1, last_page=i+1, dpi=200)[0]
                    images.append(cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))
    except Exception:
        img = cv2.imread(path)
        if img is not None:
            ocr = " ".join(reader.readtext(img, detail=0))
            texts.append(ocr)
            images.append(img)
    return "\n".join(texts), images

