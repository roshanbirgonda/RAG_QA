import fitz  # PyMuPDF
from bs4 import BeautifulSoup
from docx import Document
import markdown
import os

def extract_text(file_path):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return extract_pdf(file_path)
    elif ext == ".docx":
        return extract_docx(file_path)
    elif ext == ".txt":
        return extract_txt(file_path)
    elif ext == ".html":
        return extract_html(file_path)
    elif ext == ".md":
        return extract_md(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_html(path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text()

def extract_md(path):
    with open(path, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
