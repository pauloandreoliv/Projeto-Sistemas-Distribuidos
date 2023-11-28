import jwt

def validar_token(token):
    chave_secreta = 'bp7jD9xR2sLpN4qA8v'

    try:
        token_decodificado = jwt.decode(token, chave_secreta, algorithms=['HS256'])
        return token_decodificado
    except jwt.ExpiredSignatureError:
        print("Token expirado. Por favor, faça login novamente.")
    except jwt.InvalidTokenError:
        print("Token inválido. Autenticação falhou.")
    
    return None