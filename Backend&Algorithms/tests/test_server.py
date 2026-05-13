"""Test suite for PersonalFinancialTracker FastAPI backend."""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient

from server import app


@pytest.fixture
def client():
    """Return a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthCheck:
    """Test root endpoint and API metadata."""

    def test_root_returns_200(self, client: TestClient):
        """GET / should return 200 with API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "version" in data

    def test_docs_available(self, client: TestClient):
        """OpenAPI docs should be accessible."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestHistorial:
    """Test GET /historial endpoint."""

    def test_get_historial_returns_list(self, client: TestClient):
        """GET /historial should return a dict with transacciones key."""
        response = client.get("/historial")
        assert response.status_code == 200
        data = response.json()
        assert "transacciones" in data
        assert isinstance(data["transacciones"], list)

    def test_historial_empty_by_default(self, client: TestClient):
        """Initially, transacciones should be empty."""
        response = client.get("/historial")
        assert response.json()["transacciones"] == []


class TestConversation:
    """Test POST /conversation endpoint."""

    def test_conversation_requires_chat_history(self, client: TestClient):
        """Request without chat_history should return 422."""
        response = client.post("/conversation", json={})
        assert response.status_code == 422

    def test_conversation_accepts_valid_history(self, client: TestClient):
        """Valid chat_history should return 200 with response."""
        payload = {
            "chat_history": [
                {"role": "user", "content": "Hola"}
            ]
        }
        response = client.post("/conversation", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "transacciones_detectadas" in data

    def test_conversation_response_is_string(self, client: TestClient):
        """The response field should be a string."""
        payload = {"chat_history": [{"role": "user", "content": "Hola"}]}
        response = client.post("/conversation", json=payload)
        data = response.json()
        assert isinstance(data["response"], str)


class TestPredict:
    """Test POST /predict endpoint."""

    def test_predict_requires_fields(self, client: TestClient):
        """Request without required fields should return 422."""
        response = client.post("/predict", json={})
        assert response.status_code == 422

    def test_predict_valid_input(self, client: TestClient):
        """Valid input should return predicted values."""
        payload = {
            "ingresos": 50000,
            "hijos": 2,
            "edad": 35,
            "educacion": 3
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "gasto_predicho" in data
        assert "r2" in data

    def test_predict_negative_income_returns_422(self, client: TestClient):
        """Negative income should be rejected."""
        payload = {
            "ingresos": -1000,
            "hijos": 0,
            "edad": 30,
            "educacion": 2
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == 422


class TestMetas:
    """Test POST /metas endpoint."""

    def test_metas_requires_metas_array(self, client: TestClient):
        """Request without metas should return 422."""
        response = client.post("/metas", json={})
        assert response.status_code == 422

    def test_metas_valid_request(self, client: TestClient):
        """Valid metas request should return LLM advice."""
        payload = {
            "metas": [
                {"nombre": "Ahorro", "valor": 10000}
            ]
        }
        response = client.post("/metas", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data

    def test_metas_empty_array(self, client: TestClient):
        """Empty metas array should still return 200."""
        payload = {"metas": []}
        response = client.post("/metas", json=payload)
        assert response.status_code == 200


class TestReset:
    """Test DELETE /reset endpoint."""

    def test_reset_returns_200(self, client: TestClient):
        """DELETE /reset should return 200."""
        response = client.delete("/reset")
        assert response.status_code == 200

    def test_reset_keeps_transacciones_in_db(self, client: TestClient):
        """Reset should not delete DB transactions."""
        # First add something
        client.post(
            "/conversation",
            json={"chat_history": [{"role": "user", "content": "Pagué 500 de comida"}]}
        )
        # Reset
        client.delete("/reset")
        # Historial should still have the transaction
        response = client.get("/historial")
        assert response.status_code == 200


class TestReportes:
    """Test GET /reportes endpoint."""

    def test_get_reportes_returns_list(self, client: TestClient):
        """GET /reportes should return a list."""
        response = client.get("/reportes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)