"""PDF loading with error handling."""
from pathlib import Path
import fitz  # PyMuPDF
from clauselens.utils.logger import get_logger

log = get_logger(__name__)

def load_pdf(pdf_path: str | Path) -> list[dict]:
    """Load PDF, return list of {page_num, text}."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF: {pdf_path}")
    log.info(f"Loading PDF: {pdf_path.name}")
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF: {e}")
    if doc.needs_pass:
        doc.close()
        raise ValueError("Password-protected PDFs are not supported.")
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({"page_num": i + 1, "text": text})
    doc.close()
    if not pages:
        raise ValueError("No extractable text. Might be a scanned PDF (OCR not supported in v1).")
    log.info(f"Extracted {len(pages)} pages")
    return pages