import io
import fitz  # PyMuPDF
from docx import Document

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file."""
    text = ""
    try:
        # Open the PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise Exception(f"Error parsing PDF: {e}")
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts text from a DOCX file."""
    text = ""
    try:
        # Load the DOCX from bytes
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise Exception(f"Error parsing DOCX: {e}")
    return text.strip()

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Extracts text from a file based on its extension.
    Supported extensions: .pdf, .docx
    """
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
