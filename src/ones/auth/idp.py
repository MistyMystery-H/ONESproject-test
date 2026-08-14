"""Application ↔ Identity Provider (many-to-many) support."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IdentityProvider:
    name: str
    available: bool = True


@dataclass
class AuthService:
    """Maps applications to one or more IdPs and the reverse."""

    app_idps: dict[str, set[str]] = field(default_factory=dict)
    idps: dict[str, IdentityProvider] = field(default_factory=dict)

    def register_idp(self, name: str) -> IdentityProvider:
        idp = IdentityProvider(name=name)
        self.idps[name] = idp
        return idp

    def configure_app(self, app_id: str, idp_names: list[str]) -> None:
        for name in idp_names:
            if name not in self.idps:
                raise KeyError(f"Unknown IdP: {name}")
        self.app_idps[app_id] = set(idp_names)

    def login(self, app_id: str, idp_name: str, code: str) -> dict:
        if app_id not in self.app_idps:
            raise KeyError(f"Unknown application: {app_id}")
        if idp_name not in self.app_idps[app_id]:
            raise PermissionError(f"IdP {idp_name} is not configured for {app_id}")

        idp = self.idps[idp_name]
        if not idp.available:
            return {"status": 503, "error": f"{idp_name} unavailable"}

        if not code:
            return {"status": 400, "error": "missing auth code"}

        return {"status": 200, "user_id": f"{app_id}:{idp_name}:user"}

    def set_idp_available(self, idp_name: str, available: bool) -> None:
        if idp_name not in self.idps:
            raise KeyError(f"Unknown IdP: {idp_name}")
        self.idps[idp_name].available = available
