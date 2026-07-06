def test_search_all_documents(client):

    response = client.get("/api/documents/search")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_by_filename(client):

    response = client.get(
        "/api/documents/search?filename=pdf"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_by_status(client):

    response = client.get(
        "/api/documents/search?status=OK"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_unknown_status(client):

    response = client.get(
        "/api/documents/search?status=INVALID_STATUS"
    )

    assert response.status_code == 200
    assert response.json() == []