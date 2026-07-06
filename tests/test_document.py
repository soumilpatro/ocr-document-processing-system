from app.models.document import Document


def test_get_all_documents(client):

    response = client.get("/api/documents")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_get_document_not_found(client):

    response = client.get("/api/documents/invalid-id")

    assert response.status_code == 404

    body = response.json()

    assert body["errorCode"] == "HTTP_ERROR"
    assert body["message"] == "Document not found"