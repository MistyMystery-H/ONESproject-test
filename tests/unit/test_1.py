import pytest
import requests

ORDER_URL = "http://localhost:8080/api/orders"
PROMO_URL = "http://localhost:8080/api/promotions"

@pytest.fixture
def customers():
    return {"custA": "C001", "custB": "C002"}

@pytest.fixture
def promotions():
    return {"promoC": "P10", "promoD": "P05"}

def test_customer_promo_many_to_many(customers, promotions):
    promo_c = promotions["promoC"]
    promo_d = promotions["promoD"]
    cust_a = customers["custA"]
    cust_b = customers["custB"]

    # Step 1: customerA applies both promoC and promoD
    order_a = create_order(cust_a, [promo_c, promo_d])
    assert order_a["status"] == "created"
    assert len(order_a["applied_promotions"]) == 2

    # Step 2: verify discount (placeholder check)
    assert order_a["total_after_discount"] < order_a["subtotal"]

    # Step 3: customerB applies only promoC
    order_b = create_order(cust_b, [promo_c])
    assert order_b["applied_promotions"] == [promo_c]

    # Step 4: check redemption history of promoC
    history = get_promo_redemptions(promo_c)
    assert cust_a in history
    assert cust_b in history

    # Step 5: check promotions on customerA's order
    order_detail = get_order_details(order_a["id"])
    applied = order_detail["applied_promotions"]
    assert promo_c in applied
    assert promo_d in applied

def create_order(customer_id, promo_ids):
    resp = requests.post(
        ORDER_URL,
        json={"customerId": customer_id, "promotionIds": promo_ids, "items": [{"id": "P001", "qty": 2}]}
    )
    assert resp.status_code == 201
    return resp.json()

def get_promo_redemptions(promo_id):
    resp = requests.get(f"{PROMO_URL}/{promo_id}/redemptions")
    assert resp.status_code == 200
    return [r["customerId"] for r in resp.json()]

def get_order_details(order_id):
    resp = requests.get(f"{ORDER_URL}/{order_id}")
    assert resp.status_code == 200
    return resp.json()