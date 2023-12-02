import jwt
import datetime

def gerar_token(id, cargo):
    chave_secreta = 'bp7jD9xR2sLpN4qA8v'
    timestamp_expiracao = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    json = {
        'id': id,
        'cargo': cargo,
        'exp': timestamp_expiracao
    }
    token = jwt.encode(json, chave_secreta, algorithm='HS256')
    return token