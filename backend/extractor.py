from transformers import pipeline
import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    print(f"Extracted text from page: {text}")
    return text

# Initialize BERT-based model for summarization and NER (Named Entity Recognition)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def extract_keywords(text):
    # Use NER model to extract entities (e.g., job titles, skills, locations)
    entities = ner_model(text)
    keywords = set()  # Using a set to avoid duplicates
    for entity in entities:
        keywords.add(entity['word'])
    return list(keywords)

def extract_summary(text, max_length=150):
    # Generate a summary using BART (or any model you choose)
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def extractor_cv(pdf_path):
    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Preprocess Text (remove unwanted content like page numbers, headers)
    text = re.sub(r'\d{1,2}[\n\s]*[A-Za-z]+\s*Page\s*\d+[\n\s]*', '', text)  # Simple regex to clean
    text = text.replace('\n', ' ').strip()

    # Step 3: Extract keywords (NER)
    keywords = extract_keywords(text)

    # Step 4: Extract a summary
    summary = extract_summary(text)

    return {
        "summary": summary,
        "keywords": keywords,
        "full_text": text
    }

