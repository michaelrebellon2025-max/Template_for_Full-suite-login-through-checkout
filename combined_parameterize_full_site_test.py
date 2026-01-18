import pytest
from fake_api import fake_login_api, fake_add_cart_api, fake_checkout_api, fake_apply_discount_api, \
    fake_remove_from_cart_api


@pytest.mark.parametrize(
    "username, password, items_to_add, expected_login_status, expected_login_message, "
    "expected_cart_status, expected_cart_total, "
    "items_to_remove, expected_remove_status, expected_cart_after_remove, "
    "discount_code, expected_discount_status, expected_discount_total, "
    "expected_checkout_status, expected_checkout_message",
    [
        # ---------------------- HAPPY PATH ----------------------
        ("admin", "secret", 2, 200, "Login Successful",      # login
         200, 2,                                           # add to cart
         0, 200, 2,                                       # remove items
         "SUMMER10", 200, 1.8,                             # discount
         200, "Order confirmed"),                           # checkout

        # ---------------------- GUEST USER ----------------------
        ("guest", "nopass", 1, 200, "Login Successful",     # login
         200, 1,                                           # add to cart
         0, 200, 1,                                       # remove items
         "SUMMER10", 200, 0.9,                             # discount
         200, "Order confirmed"),                           # checkout

        # ---------------------- BLOCKED USER ----------------------
        ("blocked", "blocked", 1, 403, "Blocked user",      # login
         403, 0,                                           # add to cart (skipped)
         0, 403, 0,                                       # remove items (skipped)
         "SUMMER10", 403, 0,                               # discount (skipped)
         403, "Checkout denied"),                           # checkout (skipped)

        # ---------------------- INVALID DISCOUNT ----------------------
        ("admin", "secret", 2, 200, "Login Successful",     # login
         200, 2,                                           # add to cart
         0, 200, 2,                                       # remove items
         "WINTER50", 400, 2,                               # discount fails
         200, "Order confirmed"),                           # checkout skipped if discount_status!=200

        # ---------------------- REMOVE TOO MANY ITEMS ----------------------
        ("admin", "secret", 2, 200, "Login Successful",     # login
         200, 2,                                           # add to cart
         3, 400, 2,                                       # remove items fails, cart stays 2
         "SUMMER10", 200, 1.8,                             # discount skipped if remove fails
         200, "Order confirmed"),                           # checkout skipped if remove fails
        # ---------------------- Empty  cart ----------------------
        ("admin", "secret", 0, 200, "Login Successful",     # login
         400, 0,                                           # add to cart
         1, 200, 2,                                       # remove items
         "SUMMER10", 200, 1.8,                             # discount skipped if remove fails
         200, "Order confirmed"),                           # checkout skipped if remove fails
        # ---------------------- missing password----------------------
        ("admin", "", 2, 401, "Unauthorized",     # login
         200, 2,                                           # add to cart
         1, 200, 2,                                       # remove items
         "SUMMER10", 200, 1.8,                             # discount skipped if remove fails
         200, "Order confirmed"),                           # checkout skipped if remove fails
    ]
)
def test_full_workflow(username,password,
                       items_to_add,expected_login_status,expected_login_message,
                       expected_cart_status,expected_cart_total,
                       expected_checkout_status,expected_checkout_message,
                       discount_code,expected_discount_status,expected_discount_total,items_to_remove, expected_remove_status, expected_cart_after_remove):

    # Step 1: Login
    login_status, login_message = fake_login_api(username, password)
    assert login_status == expected_login_status, f"Login status: expected {expected_login_status}, got {login_status}"
    assert login_message == expected_login_message, f"Login message: expected '{expected_login_message}', got '{login_message}'"

    # Step 2: Add to Cart (only if login is successful)
    if login_status == 200:
        cart_status, cart_total = fake_add_cart_api(username, items_to_add)
        assert cart_status == expected_cart_status, f"Cart status: expected {expected_cart_status}, got {cart_status}"
        assert cart_total == expected_cart_total, f"Cart total: expected {expected_cart_total}, got {cart_total}"
    else:
        cart_status, cart_total = None, None  # skip cart step for blocked/failed login
#addition for apply discount

    if cart_status == 200:
        discount_status, discount_total = fake_apply_discount_api(username, cart_total, discount_code)
        assert discount_status == expected_discount_status, f'Discount status: expected {expected_discount_status}, got {discount_status}'
        assert discount_total == expected_discount_total, f'Discount total: expected {expected_discount_total}, got {discount_total}'
    else:
        discount_status, discount_total = None, cart_total

#remove items
    if cart_status == 200:
        remove_status, cart_after_remove = fake_remove_from_cart_api(username, cart_total, items_to_remove)
        assert remove_status == expected_remove_status, f"Remove status: expected {expected_remove_status}, got {remove_status}"
        assert cart_after_remove == expected_cart_after_remove, f"Cart after remove: expected {expected_cart_after_remove}, got {cart_after_remove}"
    else:
        remove_status, cart_after_remove = None, cart_total

    # Step 3: Checkout (only if login and cart are valid)
    if login_status == 200 and cart_status == 200 and discount_status == 200:
        checkout_status, checkout_message = fake_checkout_api(username, cart_total)
        assert checkout_status == expected_checkout_status, f"Checkout status: expected {expected_checkout_status}, got {checkout_status}"
        assert checkout_message == expected_checkout_message, f"Checkout message: expected '{expected_checkout_message}', got '{checkout_message}'"
    else:
        checkout_status, checkout_message = None, None  # skip checkout if previous steps failed
