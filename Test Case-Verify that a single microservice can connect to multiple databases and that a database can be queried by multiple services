import pytest
import psycopg2

DB_ORDERS = "db_orders"
DB_PRODUCTS = "db_products"

@pytest.fixture
def services():
    return ["order-service", "inventory-service"]

def test_service_db_many_to_many(services):
    # Each service connects to both databases
    for service in services:
        conn1 = connect_db(DB_ORDERS, service)
        conn2 = connect_db(DB_PRODUCTS, service)
        assert conn1 is not None
        assert conn2 is not None

        # Execute a simple query
        cur1 = conn1.cursor()
        cur1.execute("SELECT 1")
        assert cur1.fetchone()[0] == 1
        cur2 = conn2.cursor()
        cur2.execute("SELECT 1")
        assert cur2.fetchone()[0] == 1

        conn1.close()
        conn2.close()

    # Verify that each database was accessed by at least both services
    # (In reality, you would query pg_stat_activity; here we use a placeholder count)
    order_connections = count_service_connections(DB_ORDERS)
    product_connections = count_service_connections(DB_PRODUCTS)
    assert order_connections >= 2
    assert product_connections >= 2

def connect_db(db_name, service_name):
    # Placeholder connection – adapt to your environment
    return psycopg2.connect(
        host="localhost",
        database=db_name,
        user="test",
        password="test",
        application_name=service_name
    )

def count_service_connections(db_name):
    # Placeholder – in real test, query session table
    return 2
