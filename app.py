from flask import Flask, session, redirect, url_for, render_template, request
import requests
import json

app = Flask(__name__)
app.secret_key = 'aA4s6dfl8kj90sif'

@app.route("/")
def index():
    return_request = requests.get("https://api-sistemasdistribuidos.onrender.com/item")
    if return_request.status_code == 200:
        itens = json.loads(return_request.text)
        return render_template("itens.html", itens=itens)
    else:
        return f"{return_request.status_code} : {return_request.text}"

@app.route('/entrar')
def entrar():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    session.pop('token', None)
    data = {
        "id" : str(request.form["cpf"]),
        "cpf" : str(request.form["cpf"]),
        "senha" : str(request.form["senha"])
    }
    return_request = requests.post("http://api-sistemasdistribuidos.onrender.com/login", json=data)
    if return_request.status_code == 200:
        token = return_request.json()
        session['token'] = token
        return 'Login realizado com sucesso. <a href="/">Página Inicial</a>'
    else:
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/entrar'>Tentar novamente</a>"
 
@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastro.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    data = {
        "id" : str(request.form["cpf"]),
        "cpf" : str(request.form["cpf"]),
        "nome" : str(request.form["nome"]),
        "senha" : str(request.form["senha"])
    }
    return_request = requests.post("http://api-sistemasdistribuidos.onrender.com/user", json=data)

    if return_request.status_code == 200:
        return 'Cadastro realizado com sucesso. <a href="/">Página Inicial</a>'
    else:
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/cadastrar'>Tentar novamente</a>"
        
@app.route('/cadastrar_admin')
def cadastrar_admin():
    return render_template("cadastro_admin.html")

@app.route('/create_admin', methods=["POST"])
def create_admin():
    data = {
        "id" : str(request.form["cpf"]),
        "cpf" : str(request.form["cpf"]),
        "nome" : str(request.form["nome"]),
        "senha" : str(request.form["senha"])
    }
    token = session.get('token')['token'] if session.get('token') != None else None
    headers = {"Authorization": token}
    return_request = requests.post("http://api-sistemasdistribuidos.onrender.com/admin", json=data, headers=headers)
    if return_request.status_code == 200:
        return 'Cadastro realizado com sucesso. <a href="/">Página Inicial</a>'
    else:
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/entrar'>Fazer login</a>"

@app.route('/cadastrar_item')
def cadastrar_item():
    return render_template("cadastro_item.html")

@app.route('/create_item', methods=["POST"])
def create_item():
    data = {
        "nome": request.form["item"],
        "endereco": request.form["endereco"],
        "data": str(request.form["data"]),
        "cpf": request.form["cpf"],
        "id_creator": request.form["cpf"],
        "contato": request.form["contato"],
        "img": request.form["urlImagem"]
    }
    token = session.get('token')['token'] if session.get('token') != None else None
    headers = {"Authorization": token}
    return_request = requests.post("http://api-sistemasdistribuidos.onrender.com/item", json=data, headers=headers)
    if return_request.status_code == 200:
        return 'Cadastro de item realizado com sucesso. <a href="/">Página Inicial</a>'
    else:
        return f"{return_request.status_code} : {return_request.text} <br> <a href='/entrar'>Fazer login</a>"

@app.route('/excluir_item')
def excluir_item():
    return_request = requests.get("https://api-sistemasdistribuidos.onrender.com/item")
    if return_request.status_code == 200:
        itens = json.loads(return_request.text)
        return render_template("excluir_item.html", itens=itens)
    else:
        return f"{return_request.status_code} : {return_request.text}"

@app.route('/delete_item', methods=["POST"])
def delete_item():
    token = session.get('token')['token'] if session.get('token') != None else None
    headers = {"Authorization": token}
    linha_id = request.form.get('linha_id')
    data = {
        "id" : linha_id
    }
    return_request = requests.delete("https://api-sistemasdistribuidos.onrender.com/item", json=data, headers=headers)
    if return_request.status_code == 200:
        return excluir_item()
    else:
        return f"{return_request.status_code} : {return_request.text} <br> <a href='/entrar'>Fazer login</a>"

@app.route('/atualizar_item')
def atualizar_item():
    return_request = requests.get("https://api-sistemasdistribuidos.onrender.com/item")
    if return_request.status_code == 200:
        itens = json.loads(return_request.text)
        return render_template("atualizar_item.html", itens=itens)
    else:
        return f"{return_request.status_code} : {return_request.text}"

@app.route('/update_item', methods=["POST"])
def update_item():
    token = session.get('token')['token'] if session.get('token') != None else None
    headers = {"Authorization": token}
    linha_id = request.form.get('linha_id')
    linha_id_creator = request.form.get('linha_id_creator')
    data = {
        "id" : linha_id,
        "id_creator" : linha_id_creator
    }
    return_request = requests.put("https://api-sistemasdistribuidos.onrender.com/item", json=data, headers=headers)
    if return_request.status_code == 200:
        return atualizar_item()
    else:
        return f"{return_request.status_code} : {return_request.text} <br> <a href='/entrar'>Fazer login</a>"

@app.route('/logout')
def logout():
    session.pop('token', None)
    return 'Logout realizado com sucesso. <a href="/">Página Inicial</a>'

if __name__ == "__main__":
    app.run()