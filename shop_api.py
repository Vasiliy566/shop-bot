import requests

API_URL = "http://127.0.0.1:8000"
API_KEY = "1234"


def is_user_registered(telegram_id):
    r = requests.get(f"{API_URL}/users/", params={"user_id": telegram_id, "api_key": API_KEY})
    r.raise_for_status()
    return r.text == "true"


def register_user(telegram_id):
    r = requests.post(f"{API_URL}/users/", params={"user_id": telegram_id, "api_key": API_KEY})
    r.raise_for_status()
    return r.text == "true"


def get_products():
    r = requests.get(f"{API_URL}/products/", params={"api_key": API_KEY})
    r.raise_for_status()
    return r.json()


def purchase(user_id, product_id, price):
    r = requests.post(f"{API_URL}/purchase/", json={
        "user_id": user_id,
        "product_id": product_id,
        "price": price
    }, params={"api_key": API_KEY})
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    print(purchase(1, 335371241, 300))
