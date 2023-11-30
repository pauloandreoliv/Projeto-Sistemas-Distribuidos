import requests
data = {
    "key1": "value1",
    "key2": "value2"
}
response = requests.post("https://127.0.0.1/login", data=data)

print(response.text)
