import io
import PyPDF2


def extract_text(file_bytes: bytes) -> str:
    """Extract plain text from a PDF.

    Args:
        file_bytes: The binary content of the uploaded PDF.

    Returns:
        A single string containing the concatenated text of all pages.
    """
    try:
        # PyPDF2 expects a file-like object
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text_chunks = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            # extract_text can return None for some pages; guard against that
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
        return "\n".join(text_chunks)
    except Exception as e:
        # In a production app you would log this error
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
