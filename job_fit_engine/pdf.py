from __future__ import annotations

from io import BytesIO
from typing import Protocol

try:
    from pypdf import PdfReader
except ModuleNotFoundError:  # pragma: no cover - exercised through runtime error handling
    PdfReader = None


class UploadedPdfLike(Protocol):
    def getvalue(self) -> bytes:
        ...


def extract_text_from_pdf(uploaded_file: UploadedPdfLike) -> str:
    if PdfReader is None:
        raise RuntimeError(
            "PDF uploads require pypdf. Install project dependencies to enable PDF extraction."
        )

    reader = PdfReader(BytesIO(uploaded_file.getvalue()))
    page_text = [(page.extract_text() or "").strip() for page in reader.pages]
    return "\n".join(text for text in page_text if text).strip()
