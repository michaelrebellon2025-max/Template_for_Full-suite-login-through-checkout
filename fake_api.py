# api.py

def fake_login_api(username, password):
    if username == "admin" and password == "secret":
        return 200, "Login Successful"
    elif username == "guest" and password == "nopass":
        return 200, "Login Successful"
    elif username == "blocked":
        return 403, "Blocked user"
    else:
        return 401, "Unauthorized"


def fake_add_cart_api(user, items):
    if user == "blocked":
        return 403, 0
    if items <= 0:
        return 400, 0
    return 200, items


def fake_checkout_api(user, cart_total):
    if user == "blocked":
        return 403, "Checkout denied"
    if cart_total <= 0:
        return 400, "Cart empty"
    return 200, "Order confirmed"

def fake_apply_discount_api(user, cart_total, discount_code):
    if user == "blocked":
        return 403, cart_total  # blocked users cannot apply discounts
    if cart_total <= 0:
        return 400, cart_total  # can't apply discount to empty cart
    if discount_code == "SUMMER10":
        return 200, cart_total * 0.9  # 10% off
    else:
        return 400, cart_total  # invalid discount code

def fake_remove_from_cart_api(user, current_cart_total, items_to_remove):
    if user == "blocked":
        return 403, current_cart_total  # cannot remove anything
    if items_to_remove > current_cart_total:
        return 400, current_cart_total  # invalid removal, cart stays the same
    return 200, current_cart_total - items_to_remove
