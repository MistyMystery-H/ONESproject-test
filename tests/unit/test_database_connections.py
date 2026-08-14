"""Unit tests for ones.database (Service ↔ DB many-to-many)."""

from ones.database import ServiceDatabaseManager


def test_service_db_many_to_many():
    mgr = ServiceDatabaseManager()
    services = ["order-service", "inventory-service"]
    for service in services:
        mgr.allow(service, ["db_orders", "db_products"])

    for service in services:
        conn1 = mgr.connect("db_orders", service)
        conn2 = mgr.connect("db_products", service)
        assert conn1 is not None
        assert conn2 is not None

        cur1 = conn1.cursor()
        cur1.execute("SELECT 1")
        assert cur1.fetchone()[0] == 1
        cur2 = conn2.cursor()
        cur2.execute("SELECT 1")
        assert cur2.fetchone()[0] == 1

        conn1.close()
        conn2.close()

    assert mgr.count_service_connections("db_orders") >= 2
    assert mgr.count_service_connections("db_products") >= 2
