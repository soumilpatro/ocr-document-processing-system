import os
import tempfile

import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Creates a FastAPI TestClient
    for all API tests.
    """
    return TestClient(app)


@pytest.fixture
def sample_pdf():

    """
    Creates a temporary PDF file.

    Used for upload testing.
    """

    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<<>>\n"
        b"endobj\n"
        b"trailer\n"
        b"<<>>\n"
        b"%%EOF"
    )

    fd, path = tempfile.mkstemp(
        suffix=".pdf"
    )

    with os.fdopen(fd, "wb") as f:
        f.write(pdf_bytes)

    yield path

    if os.path.exists(path):
        os.remove(path)