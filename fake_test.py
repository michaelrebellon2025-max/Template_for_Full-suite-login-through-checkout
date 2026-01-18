# test_suite.py

import pytest
from fake_api import fake_login_api, fake_add_cart_api, fake_checkout_api


# ----------------------
# LOGIN TESTS
# ----------------------
@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    [
        ("admin", "secret", 200, "Login Successful"),
        ("guest", "nopass", 200, "Login Successful"),
        ("admin", "wrongpass", 401, "Unauthorized"),
        ("blocked", "blocked", 403, "Blocked user"),
    ]
)
def test_login(username, password, expected_status, expected_message):
    status, message = fake_login_api(username, password)
    assert status == expected_status, f"Expected {expected_status}, got {status}"
    assert message == expected_message, f"Expected '{expected_message}', got '{message}'"


# ----------------------
# ADD TO CART TESTS
# ----------------------
@pytest.mark.parametrize(
    "user, items_to_add, expected_cart_total, expected_status",
    [
        ("admin", 2, 2, 200),
        ("admin", 0, 0, 400),
        ("guest", 1, 1, 200),
        ("blocked", 1, 0, 403),
    ]
)
def test_add_to_cart(user, items_to_add, expected_cart_total, expected_status):
    status_code, cart_total = fake_add_cart_api(user, items_to_add)
    assert status_code == expected_status, f"Expected {expected_status}, got {status_code}"
    assert cart_total == expected_cart_total, f"Expected {expected_cart_total}, got {cart_total}"


# ----------------------
# CHECKOUT TESTS
# ----------------------
@pytest.mark.parametrize(
    "user, cart_total, expected_status, expected_message",
    [
        ("admin", 2, 200, "Order confirmed"),
        ("guest", 1, 200, "Order confirmed"),
        ("blocked", 0, 403, "Checkout denied"),
        ("admin", 0, 400, "Cart empty"),
    ]
)
def test_checkout(user, cart_total, expected_status, expected_message):
    status, message = fake_checkout_api(user, cart_total)
    assert status == expected_status, f"Expected {expected_status}, got {status}"
    assert message == expected_message, f"Expected '{expected_message}', got '{message}'"
