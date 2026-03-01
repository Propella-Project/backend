import requests

def test_login_api():
    url = "https://propella-api.vercel.app/api/accounts/token/"
    data = {
        "email": "admin@gmail.com",
        "password": "123456@Ad"
    }
    Headers = {
        "Content-Type": "application/json"
        ""
    }