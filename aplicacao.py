from flask import Flask

app = Flask(__name__)

@app.route('/logout')
def logout():
    return 'Logout realizado com sucesso. <a href="/">Página Inicial</a>'

if __name__ == "__main__":
    app.run()