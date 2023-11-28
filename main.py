from servico_autenticacao import gerar_token
from servico_validador import validar_token

usuario_id = 123
senha = 'exemplo'
token_gerado = gerar_token(usuario_id, senha)

informacoes_do_usuario = validar_token(token_gerado)

if informacoes_do_usuario:
    print("Token validado com sucesso.")
    print("Informações do usuário:", informacoes_do_usuario)
else:
    print("Falha na validação do token.")