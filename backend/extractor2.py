import PyPDF2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from keybert import KeyBERT

# Function to extract text from PDF using PyPDF2 (for text-based PDFs)
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF using PyPDF2: {e}")
    
    # If PyPDF2 failed to extract text, fall back to OCR
    if not text:
        print("Text extraction failed, attempting OCR...")
        text = ocr_from_pdf(file_path)
    
    return text

# Function to extract text from image-based PDFs using Tesseract OCR
def ocr_from_pdf(file_path):
    text = ""
    try:
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error during OCR extraction: {e}")
    return text

# Function to extract keywords using KeyBERT
def extract_keywords_from_text(text, top_n=15):
    try:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, top_n=top_n, stop_words='english')
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# Main function to process the CV and extract both text and keywords
def process_cv(file_path):
    # Step 1: Extract text
    text = extract_text_from_pdf(file_path)
    if not text:
        return {"error": "No text extracted from CV"}
    
    # Step 2: Extract keywords
    keywords = extract_keywords_from_text(text)
    if not keywords:
        return {"error": "No keywords extracted"}
    
    return {
        "extracted_text": text[:500],  # Preview of first 500 chars
        "keywords": keywords
    }
