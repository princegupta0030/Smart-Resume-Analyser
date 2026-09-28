import pytest
import io
import fitz  # PyMuPDF
from docx import Document
from src.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_text

def create_mock_pdf(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes

def create_mock_docx(text: str) -> bytes:
    doc = Document()
    doc.add_paragraph(text)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    return file_stream.getvalue()

def test_extract_text_from_pdf():
    expected_text = "This is a mock PDF resume."
    pdf_bytes = create_mock_pdf(expected_text)
    extracted = extract_text_from_pdf(pdf_bytes)
    assert expected_text in extracted

def test_extract_text_from_docx():
    expected_text = "This is a mock DOCX resume."
    docx_bytes = create_mock_docx(expected_text)
    extracted = extract_text_from_docx(docx_bytes)
    assert expected_text in extracted

def test_extract_text_router():
    pdf_bytes = create_mock_pdf("PDF content")
    docx_bytes = create_mock_docx("DOCX content")

    assert "PDF content" in extract_text(pdf_bytes, "resume.pdf")
    assert "DOCX content" in extract_text(docx_bytes, "resume.docx")

    with pytest.raises(ValueError, match="Unsupported file format"):
        extract_text(b"some bytes", "resume.txt")
