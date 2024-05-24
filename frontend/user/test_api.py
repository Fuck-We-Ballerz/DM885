import requests

url = "http://192.168.1.70:5050/api/login"
data = {
    "username": "admin",
    "password": "admin"
}

response = requests.post(url, json=data)
print(response.json())
