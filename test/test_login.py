import requests
import json

BASE_URL = "http://localhost:5000"

def test_registration():
    registration_data = {
        "username": "thanhnp12",
        "email": "thanhnp12@gmail.com",
        "password": "abc123"
    }
    response = requests.post(f"{BASE_URL}/register", json=registration_data)
    print("Registration Response:", response.status_code)
    print(response.json())

def test_login():
    login_data = {
        "username_or_email": "thanhnp12",
        "password": "abc123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print("Login Response:", response.status_code)
    print(response.json())

if __name__ == "__main__":
    print("Testing Registration API:")
    test_registration()
    print("\nTesting Login API:")
    test_login()