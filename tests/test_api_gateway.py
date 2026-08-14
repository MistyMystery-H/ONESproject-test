import pytest
import requests

GATEWAY_A = "http://gateway-a:8080"
GATEWAY_B = "http://gateway-b:8080"
ADMIN_A = "http://gateway-a:8081/admin/routes"

def test_gateway_route_many_to_many():
    # Steps 1-3: baseline route on both gateways
    assert route_works(GATEWAY_A, "/api/orders", "order-service")
    assert route_works(GATEWAY_B, "/api/orders", "order-service")
    assert route_works(GATEWAY_A, "/api/payments", "payment-service")

    # Step 4: add new route only to gatewayA
    add_route(GATEWAY_A, "/api/shipments", "shipment-service")

    # Step 5: verify exclusive route
    resp_a = requests.get(f"{GATEWAY_A}/api/shipments")
    assert resp_a.status_code == 200
    assert "shipment-service" in resp_a.text

    resp_b = requests.get(f"{GATEWAY_B}/api/shipments")
    assert resp_b.status_code == 404

def route_works(gateway_url, path, expected_backend):
    resp = requests.get(f"{gateway_url}{path}")
    assert resp.status_code == 200
    # Check via response header or body (placeholder)
    return True

def add_route(gateway_url, path, backend):
    resp = requests.post(
        f"{ADMIN_A}" if "gateway-a" in gateway_url else f"{ADMIN_A.replace('gateway-a', 'gateway-b')}",
        json={"path": path, "target": backend}
    )
    assert resp.status_code == 201