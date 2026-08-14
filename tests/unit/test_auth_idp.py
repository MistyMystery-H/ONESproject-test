"""Unit tests for ones.auth (App ↔ IdP many-to-many)."""

from ones.auth import AuthService


def test_app_idp_many_to_many():
    svc = AuthService()
    svc.register_idp("google")
    svc.register_idp("azure")
    svc.configure_app("app1", ["google", "azure"])
    svc.configure_app("app2", ["google", "azure"])

    for app_id in ("app1", "app2"):
        for idp in ("google", "azure"):
            result = svc.login(app_id, idp, "fake_auth_code")
            assert result["status"] == 200
            assert "user_id" in result

    svc.set_idp_available("google", False)
    for app_id in ("app1", "app2"):
        assert svc.login(app_id, "azure", "fake_code")["status"] == 200
        assert svc.login(app_id, "google", "fake_code")["status"] == 503
