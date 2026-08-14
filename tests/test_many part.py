import pytest
import requests

SUPPLIER_URL = "http://localhost:8080/api/suppliers"
PART_URL = "http://localhost:8080/api/parts"
ORDER_URL = "http://localhost:8080/api/purchase-orders"

def test_supplier_part_many_to_many():
    supplier_a = "SUP_A"
    supplier_b = "SUP_B"
    part_x = "PRT_X"
    part_y = "PRT_Y"

    # Step 1: assign partX and partY to supplierA
    assign_part_to_supplier(supplier_a, part_x)
    assign_part_to_supplier(supplier_a, part_y)

    # Step 2: assign partX to supplierB
    assign_part_to_supplier(supplier_b, part_x)

    # Step 3: query supplierA catalog
    catalog_a = get_supplier_catalog(supplier_a)
    assert part_x in catalog_a
    assert part_y in catalog_a

    # Step 4: query partX suppliers
    suppliers_for_x = get_part_suppliers(part_x)
    assert supplier_a in suppliers_for_x
    assert supplier_b in suppliers_for_x

    # Step 5: place order for partX with supplierB
    order = place_order(part_x, supplier_b)
    assert order["supplierId"] == supplier_b
    assert order["partId"] == part_x

def assign_part_to_supplier(supplier_id, part_id):
    resp = requests.post(
        f"{SUPPLIER_URL}/{supplier_id}/parts",
        json={"partId": part_id}
    )
    assert resp.status_code == 200

def get_supplier_catalog(supplier_id):
    resp = requests.get(f"{SUPPLIER_URL}/{supplier_id}/catalog")
    assert resp.status_code == 200
    return [p["id"] for p in resp.json()]

def get_part_suppliers(part_id):
    resp = requests.get(f"{PART_URL}/{part_id}/suppliers")
    assert resp.status_code == 200
    return [s["id"] for s in resp.json()]

def place_order(part_id, supplier_id):
    resp = requests.post(
        ORDER_URL,
        json={"partId": part_id, "supplierId": supplier_id, "quantity": 100}
    )
    assert resp.status_code == 201
    return resp.json()