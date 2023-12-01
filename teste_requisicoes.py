import requests
import json

url = "http://api-sistemasdistribuidos.onrender.com/user"
dados_json = {"id": "1235678", "cpf": "Exemplo", "senha": "25", "nome": "Exemplópolis"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=dados_json, headers=headers)

print(response.text)
