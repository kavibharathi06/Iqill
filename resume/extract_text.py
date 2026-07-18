import io
import pdfplumber


def extract_resume_text(pdf_file) -> str:
    """
    Extract text from every page of the uploaded resume.

    Supports:
    - Streamlit UploadedFile
    - bytes
    - file-like object

    Returns:
        Extracted resume text as a single string.
    """

    extracted_text = ""

    try:

        # If bytes are passed, convert to file object
        if isinstance(pdf_file, bytes):
            pdf_file = io.BytesIO(pdf_file)

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += page_text + "\n"

    except Exception as e:

        print(f"PDF Extraction Error : {e}")

    return extracted_text.strip()