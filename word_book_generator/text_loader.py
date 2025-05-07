import fitz  # PyMuPDF
import re

def load_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().lower()
    

def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    doc = fitz.open(pdf_path)
    text = ""
    
    # 페이지 범위 계산
    if end_page is None:
        end_page = len(doc)  # 전체 페이지까지

    for page_num in range(start_page, min(end_page, len(doc))):
        page = doc[page_num]
        text += page.get_text()
        text += "\n"
    
    return text.lower()

def extract_words(text):
    return re.findall(r'\b[a-z]+\b', text)