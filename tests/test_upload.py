import os


def test_upload_invalid_file(client):

    response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "sample.txt",
                b"hello world",
                "text/plain"
            )
        },
    )

    assert response.status_code == 400


def test_upload_empty_file(client):

    response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf"
            )
        },
    )

    assert response.status_code in [400, 422]