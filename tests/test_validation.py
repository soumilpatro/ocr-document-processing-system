from app.models.document import Document


def test_validate_document_not_found(client):

    response = client.post(
        "/api/documents/invalid-id/validate"
    )

    assert response.status_code == 404


def test_validate_existing_document(client):

    documents = client.get(
        "/api/documents"
    ).json()

    # Skip if no uploaded documents exist
    if len(documents) == 0:
        return

    document_id = documents[0]["id"]

    response = client.post(
        f"/api/documents/{document_id}/validate"
    )

    assert response.status_code == 200

    body = response.json()

    assert "header" in body
    assert "transactions" in body