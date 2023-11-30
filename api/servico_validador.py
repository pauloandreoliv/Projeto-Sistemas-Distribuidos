import jwt

def validar_token(token):
    chave_secreta = 'bp7jD9xR2sLpN4qA8v'
    try:
        token_decodificado = jwt.decode(token, chave_secreta, algorithms=['HS256'])
        return token_decodificado
    except jwt.ExpiredSignatureError as e:
        raise ValueError("Token expirado. Por favor, faça login novamente.")
    except jwt.InvalidTokenError as e:
        raise ValueError("Token inválido. Autenticação falhou.")
    return False