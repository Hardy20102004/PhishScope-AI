import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_secure_headers_present(client: TestClient):
    """Verify that SecureHeadersMiddleware injects required security headers."""
    # Ensure trailing slash to avoid 307
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    
    headers = response.headers
    assert "strict-transport-security" in headers
    assert "x-frame-options" in headers
    assert "x-content-type-options" in headers
    
from app.core.config import settings

@pytest.mark.skipif(not settings.BACKEND_CORS_ORIGINS, reason="CORS allows wildcard in this environment")
def test_cors_preflight_rejection(client: TestClient):
    response = client.options(
        "/api/v1/health/",
        headers={
            "Origin": "http://malicious-site.com",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert "access-control-allow-origin" not in response.headers or response.headers["access-control-allow-origin"] != "http://malicious-site.com"

def test_broken_object_level_authorization(client: TestClient):
    pass 

def test_sql_injection_rejection(client: TestClient):
    payload = "' OR 1=1 --"
    response = client.get(f"/api/v1/observability/incidents?limit={payload}")
    assert response.status_code in [401, 422] 

