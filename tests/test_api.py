import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)


class TestHealthAPI:
    """Тесты для health check API"""
    
    def test_health_check(self, client):
        """Тест основного health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_detailed_health_check(self, client):
        """Тест детального health check"""
        response = client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "components" in data


class TestContactAPI:
    """Тесты для contact API"""
    
    def test_send_message_success(self, client):
        """Тест успешной отправки сообщения"""
        response = client.post(
            "/api/v1/contact/send",
            data={
                "telegram": "test_user",
                "message": "Test message"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    
    def test_send_message_missing_fields(self, client):
        """Тест отправки сообщения с отсутствующими полями"""
        response = client.post(
            "/api/v1/contact/send",
            data={"telegram": "test_user"}
        )
        assert response.status_code == 422
    
    def test_legacy_send_message(self, client):
        """Тест legacy endpoint"""
        response = client.post(
            "/send-message",
            data={
                "telegram": "test_user",
                "message": "Test message"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data


class TestProductsAPI:
    """Тесты для products API"""
    
    def test_get_products(self, client):
        """Тест получения списка продуктов"""
        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert "total" in data
    
    def test_get_categories(self, client):
        """Тест получения категорий"""
        response = client.get("/api/v1/products/categories/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_products(self, client):
        """Тест поиска продуктов"""
        response = client.get("/api/v1/products/search/?q=tshirt")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestWebPages:
    """Тесты для веб-страниц"""
    
    def test_home_page(self, client):
        """Тест главной страницы"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_acne_page(self, client):
        """Тест страницы Acne"""
        response = client.get("/acne")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_hphealth_page(self, client):
        """Тест страницы HP Health"""
        response = client.get("/hphealth")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_zip_page(self, client):
        """Тест страницы Zip"""
        response = client.get("/zip")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_poizon_page(self, client):
        """Тест страницы Poizon"""
        response = client.get("/poizon")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__])
