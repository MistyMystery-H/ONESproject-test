import pytest
import requests

APP1_URL = "http://app1.com/auth"
APP2_URL = "http://app2.com/auth"
IDP_GOOGLE = "google"
IDP_AZURE = "azure"

def test_idp_app_many_to_many():
    # Steps 1-4: each app logs in with each IdP
    for app_url in (APP1_URL, APP2_URL):
        for idp in (IDP_GOOGLE, IDP_AZURE):
            resp = requests.post(f"{app_url}/login", json={"idp": idp, "code": "fake_auth_code"})
            assert resp.status_code == 200
            assert "user_id" in resp.json()

    # Step 5: simulate Google unavailable (using a mock context)
    with mock_idp_unavailable(IDP_GOOGLE):
        for app_url in (APP1_URL, APP2_URL):
            # Azure should still work
            resp = requests.post(f"{app_url}/login", json={"idp": IDP_AZURE, "code": "fake_code"})
            assert resp.status_code == 200
            # Google should fail with 503
            resp = requests.post(f"{app_url}/login", json={"idp": IDP_GOOGLE, "code": "fake_code"})
            assert resp.status_code == 503

def mock_idp_unavailable(idp):
    # Context manager placeholder to simulate IdP outage
    class MockContext:
        def __enter__(self):
            # Set environment variable or override internal client
            return self
        def __exit__(self, *args):
            pass
    return MockContext()
