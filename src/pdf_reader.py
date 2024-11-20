"""Extracts Text from a PDF file
Returns:
    str: Text from PDF
"""
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
