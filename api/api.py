from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from servico_autenticacao import gerar_token
from servico_validador import validar_token

app = Flask(__name__)

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "sistemasdistribuidos-100c6",
  "private_key_id": "a5b430d2fba3ccc2c8871fd44044be5513cf2032",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCpeJXaxoDv5fNv\nss0mRmZehdqLrdR9qL9M/rEsxxCYEIWC5SWl7CQffWpAbfFI6N8o/yyklF/SgRXU\nzy0F3ghkoF2oXwWkuuVjfZLlhdsR3USj0kC8ldaZd4+4DyT81Sdg/0HeQcnBawid\nrQ8KgHGSQyhP4GBDsGuyudF7lsV0Uj0TvkWF6vqWp28cFjUjcQD4bVwQZ6HJnt7X\ndgPtJRbgBOe2vOSIKSNTz/E7K3v5tAUk8Z2WfpwZZegUDxNs3tq0GUzgVdp0BTce\nh5ja6VL3V34VgqoRZD2MyRbTjECw3ntG6jEZXWbBGSGfDE4/tEH/pSsT6J2llkmV\np8s9x2U9AgMBAAECggEAJSnmNOKEindDJerQLbVRBCf219wwJblQcD5HFMJ3q10u\nJhkBo0vwVP6AAy6I89vrejZRMCtAgy1fH/qpzShWb1iyiTaDSo9Yt/Nk+BPdSWLc\nR0+XdjOmqqNrPyoFCrPkrZL0exyytYl3C3rUulEV9sTm7XNPMPDagUhZ/a//z4TQ\nQF5Yut7tFriYlyGYYajBb8k1Ns0wefVp9FSFsotPzSx4vP0iH6oNa/ay6HIbv0oQ\nLW26ySD+j5Mm0KIKofmsTyZcAaYtA58a9Shwq83YJGpjaR/NIMBDdqZ0CbE4JM8s\nNfuJ0FCdk1RuuG+/geRNBNWu9DzQL+JjfvkgrPh90QKBgQDsJuVfipprQmVhHovX\nztMEWFj+ckjkpnK3qqi9oo83W4kFngZJIynY0yVDdJYmc75FBfpgqTrJ8mx8U95Z\n4oV+wFrt9Yz3H59/FiL14iC9ObWguAAYaZQHreRsMgnbbSBo7JWo3k6loUI4CN0R\n2nwHUcwN1HrjfNPEEf7A98JQkQKBgQC3tvdrMLXCVnM9KvSGEpZew4Y4XLfKKQoN\nV5sytH/uOyhNkf97NwmKbFup8qbXLfEX0U3QG2Gr8VYeyk5Z+9il9nK7D+vGmM82\nnBkYjJtJwqnxAOptDvAEA6/YEGlHMRiHXurAHufoI8DyzpyAConaaGbPL1bG3pmE\nzwc3wa1f7QKBgQDEy9lEmIX9MrS3jbQuYT57FYD8cpMKcSeSpda/SfQdxttWYg2M\n74/VEIiyQTtLyhLbBJNV8FF8r9j2dxIKR/rF2Vktiv8xhhnt163EyPBNoQUabZwu\nu/VPvPtpqv2J7dQffGFv++sAnnVHqyNH2JKZqvHo6JSMdZ8oe3KYryAw8QKBgAbF\nEEL77Ya2xtJXNeGG59GgJN8I06D4eC1bsBVjP1+ZAHgzTBXPRmO6cHpHvcwqHjtB\ndDuZ9rRuVT0XOWHpfOdIuJuaD5cm5GPfxrD35XUHXlnKLdlM9p0/QYiVujtsXLoI\nTmA8A1Gzl5Wa9XtmaAQLWtaBqRH0+/U/58UvNuNVAoGBALYwWhAfYZxkzXLZvsZh\nBpHbuP4cZAgkiI0fNZo0gfRY3drJ5+bqZc2RDayMSvbE1DUCBnu1OGARkuwG9HaH\n1LL7yTFNgw1BmO24scSWg1u2EANcSuw6W5X4pSwKZjlNbxxfNQXJHHtsBFgXUXGJ\n3PlLjEdVtuE47TFpzsZNj6Cz\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-uhcx9@sistemasdistribuidos-100c6.iam.gserviceaccount.com",
  "client_id": "112552935575985542686",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-uhcx9%40sistemasdistribuidos-100c6.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
default_app = initialize_app(cred) 
db = firestore.client() 
user_ref = db.collection('user')
item_ref = db.collection('item')

@app.route('/user', methods=['GET'])
def get_user():
    try:
        id = request.args.get('id')    
        if id:
            user_id = user_ref.document(id).get()
            return jsonify(user_id.to_dict()), 200
        else:
            all_id = [doc.to_dict() for doc in user_ref.stream()]
            return jsonify(all_id), 200
    except Exception as e:
        return f"An Error Occured: {e}"
        
@app.route('/user', methods=['POST'])
def create_user():
    try:
        id = request.json['id']
        request_completa = request.json
        request_completa['cargo'] = 'user'
        user_ref.document(id).set(request_completa)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/item', methods=['GET'])
def get_items():
    try:
        all_id = [doc.to_dict() for doc in item_ref.stream()]
        return jsonify(all_id), 200
    except Exception as e:
        return f"An Error Occured: {e}"

#Qualquer um que estiver logado pode criar um item
@app.route('/item', methods=['POST'])
def create_items():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            item_ref.document().set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        return f"An Error Occured: {e}"

#Apenas administrador pode deletar item
@app.route('/item', methods=['DELETE'])
def delete_items():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)

        if token and token['cargo'] == "admin":
                id = request.args.get('id')
                item_ref.document(id).delete()
                return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        return f"An Error Occured: {e}"

#Apenas administrador pode criar administrador
@app.route('/admin', methods=['POST'])
def create_admin():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)

        if token and token['cargo'] == "admin":
            id = request.json['id']
            request_completa = request.json
            request_completa['cargo'] = 'admin'
            user_ref.document(id).set(request_completa)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        return f"An Error Occured: {e}"

#Apenas quem criou o item pode atualizar seu status
@app.route('/item', methods=['PUT'])
def update_items():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token and token['id'] == request.json['id_creator']:
            id = request.json['id']
            item_ref.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/login', methods=['POST'])
def login():
    try:
        id = request.json['id']
        senha = request.json['senha']
        userid_ref = user_ref.document(id)
        dados = userid_ref.get().to_dict()
        
        if dados and dados.get('senha') == senha:
            id_autenticado = dados.get('cpf')
            cargo_autenticado = dados.get('cargo')

            token = gerar_token(id_autenticado, cargo_autenticado)
            return jsonify({"token": token, "cargo": cargo_autenticado}), 200
        else:
            return jsonify({"error": "Acesso negado. Dados inválidos."}), 401
    except Exception as e:
        return f"An Error Occured: {e}"

if __name__ == "__main__":
    app.run()