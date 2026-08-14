"""Microservice ↔ Database (many-to-many) connection management."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DatabaseRegistry:
    """Tracks which services have opened connections to which databases."""

    connections: dict[str, set[str]] = field(default_factory=dict)

    def record(self, db_name: str, service_name: str) -> None:
        self.connections.setdefault(db_name, set()).add(service_name)

    def count_services(self, db_name: str) -> int:
        return len(self.connections.get(db_name, set()))


@dataclass
class Connection:
    db_name: str
    service_name: str
    closed: bool = False

    def cursor(self) -> "Cursor":
        if self.closed:
            raise RuntimeError("connection is closed")
        return Cursor()

    def close(self) -> None:
        self.closed = True


@dataclass
class Cursor:
    def execute(self, sql: str) -> None:
        self._sql = sql

    def fetchone(self) -> tuple:
        if getattr(self, "_sql", "") == "SELECT 1":
            return (1,)
        return (None,)


@dataclass
class ServiceDatabaseManager:
    """Allows a service to connect to multiple databases (in-memory stub)."""

    registry: DatabaseRegistry = field(default_factory=DatabaseRegistry)
    allowed: dict[str, set[str]] = field(default_factory=dict)

    def allow(self, service_name: str, db_names: list[str]) -> None:
        self.allowed[service_name] = set(db_names)

    def connect(self, db_name: str, service_name: str) -> Connection:
        allowed_dbs = self.allowed.get(service_name, set())
        if db_name not in allowed_dbs:
            raise PermissionError(
                f"Service {service_name} is not allowed to access {db_name}"
            )
        self.registry.record(db_name, service_name)
        return Connection(db_name=db_name, service_name=service_name)

    def count_service_connections(self, db_name: str) -> int:
        return self.registry.count_services(db_name)
