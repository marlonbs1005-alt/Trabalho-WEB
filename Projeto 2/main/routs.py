from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'

# Dicionario para armazenar os usuarios cadastrados no formato -> "usuario": "senha"
# Já deixamos o "admin" cadastrado por padrão
USUARIOS_DB = {
    "marlin": "asdffdsa"
}

PRODUTOS = [
    {"id": 1, "nome": "Gabinete Gamer RGB", "preco": "R$ 450,00", "badge": "Destaque"},
    {"id": 2, "nome": "Geladeira com IA", "preco": "R$ 4.200,00", "badge": "Destaque"},
    {"id": 3, "nome": "Notebook 15''", "preco": "R$ 3.100,00", "badge": "Destaque"},
    {"id": 4, "nome": "TV 60'' 4K", "preco": "R$ 2.800,00", "badge": "Destaque"},
    {"id": 5, "nome": "Celular 128 GB", "preco": "R$ 1.500,00", "badge": "Promoção"},
    {"id": 6, "nome": "Fone Bluetooth", "preco": "R$ 250,00", "badge": "Promoção"},
    {"id": 7, "nome": "Smartwatch 2026", "preco": "R$ 600,00", "badge": "Promoção"}
]

@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form.get("username")
        senha = request.form.get("password")

        # Verifica se o usuário existe no dicionário e se a senha está correta
        if usuario in USUARIOS_DB and USUARIOS_DB[usuario] == senha:
            session["usuario_logado"] = usuario
            return redirect(url_for("loja"))
        else:
            erro = "Usuário ou senha incorretos."

    return render_template("login.html", erro=erro)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")

        # Validações simples
        if senha != confirmar_senha:
            erro = "As senhas não coincidem!"
            return render_template("cadastro.html", erro=erro)
        
        # Usaremos o e-mail ou nome para fazer login
        usuario_login = email.split('@')[0] if email else nome.lower().replace(" ", "")

        if usuario_login in USUARIOS_DB:
            erro = "Este usuário já está cadastrado!"
            return render_template("cadastro.html", erro=erro)

        # SALVA O NOVO USUÁRIO NO BANCO DE DADOS EM MEMÓRIA
        USUARIOS_DB[usuario_login] = senha

        # Redireciona para o login informando o nome de usuário criado
        return redirect(url_for("login"))

    return render_template("cadastro.html", erro=erro)

@app.route("/loja")
def loja():
    if "usuario_logado" not in session:
        return redirect(url_for("login"))
    
    return render_template("homepage.html", produtos=PRODUTOS, usuario=session["usuario_logado"])

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    return redirect(url_for("login"))

