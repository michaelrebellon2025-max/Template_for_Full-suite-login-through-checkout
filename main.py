def test_login():
    status, message= fake_login_api("admin", "secret")

    assert status == 200, f'Expected status code 200, got {status}'
    assert message == "Login successful", f'Expected status code 200, got {message}'


## makes test_login() into parametrize industry standard
## makes reading the test cases easier and independently tests each version with messages

import pytest

@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    [
        ("admin", "secret", "200", "Login successful"),   # valid login
        ("admin", "wrongpass", "401", "Unauthorized"),    # wrong password
        ("guest", "nopass", "500", "Server error")        # unknown user
    ]
)
def test_login(username, password, expected_status, expected_message):
    status, message = fake_login_api(username, password)

    assert status == expected_status, f"Expected status {expected_status}, got {status}"
    assert message == expected_message, f"Expected message '{expected_message}', got '{message}'"

import pytest
@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
 [
    ("admin", "secret", "200", "Login successful"),  # valid
    ("admin", "wrongpass", "401", "Unauthorized"),   # wrong password
    ("guest", "nopass", "500", "Server error"),      # unknown user
    ("guest", "nopass", "200", "Server error")       # intentional fail
]
)
def test_login(username, password, expected_status, expected_message):
    status, message=fake_login_api(username,password)

    assert status == expected_status, f"Expected status {expected_status}, got {status}"
    assert message == expected_message, f"Expected message '{expected_message}', got '{message}'"


#multiple parametrize tests this would be in its own page that will be referenced in tests
# fake_api.py

def fake_login_api(username, password):
    """Simulate login endpoint"""
    if username == "admin" and password == "secret":
        return "200", "Login successful"
    elif username == "admin":
        return "401", "Unauthorized"
    else:
        return "500", "Server error"

def fake_profile_api(username):
    """Simulate profile endpoint"""
    profiles = {
        "admin": {"name": "Admin User", "role": "admin"},
        "guest": {"name": "Guest User", "role": "guest"}
    }
    if username in profiles:
        return "200", profiles[username]
    else:
        return "404", "User not found"


# test_suite.py
import pytest
from fake_api import fake_login_api, fake_profile_api

login_test_cases = [
    ("admin", "secret", "200", "Login successful"),
    ("admin", "wrongpass", "401", "Unauthorized"),
    ("guest", "nopass", "500", "Server error"),
    ("guest", "nopass", "200", "Server error")  # intentional fail
]

profile_test_cases = [
    ("admin", "200", {"name": "Admin User", "role": "admin"}),
    ("guest", "200", {"name": "Guest User", "role": "guest"}),
    ("unknown", "404", "User not found")
]

##TESTS for login
@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    login_test_cases
)
def test_login(username, password, expected_status, expected_message):
    status, message = fake_login_api(username, password)
    assert status == expected_status, f"Login fail: Expected status {expected_status}, got {status}"
    assert message == expected_message, f"Login fail: Expected message '{expected_message}', got '{message}'"

##tests for profiles

@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    profile_test_cases
)
def test_profile(username, expected_status, expected_data):
    status, data = fake_profile_api(username)
    assert status == expected_status, f"Profile fail: Expected status {expected_status}, got {status}"
    assert data == expected_data, f"Profile fail: Expected {expected_data}, got {data}"
## runs tests with this as its response
test_suite.py::test_login[admin-secret-200-Login successful] PASSED
test_suite.py::test_login[admin-wrongpass-401-Unauthorized] PASSED
test_suite.py::test_login[guest-nopass-500-Server error] PASSED
test_suite.py::test_login[guest-nopass-200-Server error] FAILED
test_suite.py::test_profile[admin-200-Admin User] PASSED
test_suite.py::test_profile[guest-200-Guest User] PASSED
test_suite.py::test_profile[unknown-404-User not found] PASSED

"""
    Intentional login fail shows up clearly
    Other tests run independently — fail in one doesn’t stop the others
    Pytest gives a clean report with pass/fail per test case
"""


def test_login(username,password):
    if username == "admin" and password == "secret":
        return "200", "Login successful"
    elif username == "admin" and password == "wrongpass":
        return "401", "Unauthorized"
    else:
        return "500", "Server error"

@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
 [
    ("admin", "secret", "200", "Login successful"),  # valid
    ("admin", "wrongpass", "401", "Unauthorized"),   # wrong password
    ("guest", "nopass", "500", "Server error"),      # unknown user
    ("guest", "nopass", "200", "Server error")       # intentional fail
]
)
def test_fake_login(username,password,expected_status,expected_message):
    status,message = test_login(username, password)
    assert status == expected_status, f"Expected status {expected_status}, got {status}"
    assert message == expected_message, f"Expected message '{expected_message}', got '{message}'"




"""
NEW parametrize tests from chatgbt test
"""



import pytest

def fake_test_login_api(username, password):
    if username == "admin" and password == "secret":
        return 200, "Login Successful"
    elif username == "guest" and password == "nopass":
        return 200, "Login Successful"
    elif username == "blocked" :
        return 403, "Blocked user"
    else:
        return 401, "Unauthorized"

@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    [
        ("admin", "secret", 200, "Login Successful"), #valid
        ("guest", "nopass", 200, "Login Successful"),
        ("admin", "wrongpass", 401, "Unauthorized"), #wrong password
        ("blocked", "blocked", 403, "Blocked user")
    ]
)

def test_login(username, password, expected_status, expected_message):
    status, message = fake_test_login_api(username, password)
    assert status == expected_status, f'Expected status {expected_status} and got {status}'
    assert message == expected_message, f"Expected message '{expected_message}', got '{message}'"



import pytest
def fake_add_cart_api(user,items_to_add):
    if user == "blocked":
        return 403, 0
    if items_to_add <=0:
        return 400, 0
    return 200, items_to_add

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
    status_code, cart_total= fake_add_cart_api (user, items_to_add)
    assert status_code == expected_status, f"Expected status {expected_status}, got {status_code}"
    assert cart_total==expected_cart_total, f"Expected total {expected_cart_total}, got {cart_total}"


import pytest
def fake_checkout_api(user, cart_total):
    if user == "blocked":
        return 403, "Checkout denied"
    if cart_total <= 0:
        return 400, "Cart empty"
    return 200, "Order confirmed"

@pytest.mark.parametrize(
    "user, cart_total, expected_status, expected_message",
    [
        ("admin", 2, 200, "Order confirmed"),
        ("guest", 1, 200, "Order confirmed"),
        ("blocked", 0, 403, "Checkout denied")
    ]

)
def test_checkout(user, cart_total, expected_status, expected_message):
    status, message = fake_checkout_api (user, cart_total)
    assert status == expected_status, f"Expected status {expected_status} and got {status}"
    assert message == expected_message, f"Expected message '{expected_message}', got '{message}'"
