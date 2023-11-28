import jwt
import datetime

def gerar_token(usuario_id, senha):
    chave_secreta = 'bp7jD9xR2sLpN4qA8v'
    timestamp_expiracao = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    json_token = {
        'user_id': usuario_id,
        'senha': senha,
        'exp': timestamp_expiracao
    }
    token = jwt.encode(json_token, chave_secreta, algorithm='HS256')
    return token