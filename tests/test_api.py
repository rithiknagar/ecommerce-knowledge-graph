from fastapi.testclient import TestClient

from app.main import app


def test_query_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question": "Which Nike products are supplied by TechSupply?"
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["question"]
        assert data["answer"]
        assert data["cypher"]
        assert data["retrieved_data"]

        product_names = {
            item["product_name"]
            for item in data["retrieved_data"]
        }

        assert "Air Max 90" in product_names
        assert "banana" in product_names