def test_search_all_documents(client):

    response = client.get("/api/documents/search")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "documents" in data

    assert isinstance(data["documents"], list)

    assert data["count"] == len(data["documents"])


def test_search_by_filename(client):

    response = client.get(
        "/api/documents/search?filename=pdf"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["documents"], list)

    assert data["count"] == len(data["documents"])


def test_search_by_status(client):

    response = client.get(
        "/api/documents/search?status=OK"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["documents"], list)

    assert data["count"] == len(data["documents"])


def test_search_unknown_status(client):

    response = client.get(
        "/api/documents/search?status=INVALID_STATUS"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 0

    assert data["documents"] == []

    assert data["message"] == "No matching documents found."