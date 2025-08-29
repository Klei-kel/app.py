import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session
# Importando bibliotecas necessárias

app = Flask(__name__)
app.secret_key = "chave_secreta"  # necessário para sessão

# Usuários válidos
valid_users = ["Cleyton", "Fernanda", "Beatriz", "Caio"]
valid_password = "12345"

# Garante que o arquivo CSV tenha um cabeçalho
def inicializa_csv():
    if not os.path.exists("triagem.csv"):
        with open("triagem.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Tipo", "Nome", "Idade", "Responsavel", "Queixa Principal",
                "Tempo de Sintomas", "Sintomas Graves", "Doencas Cronicas/Diagnosticadas",
                "Medicamentos", "Alergias"
            ])

# Página inicial (login)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        if username in valid_users and password == valid_password:
            session["username"] = username
            return redirect(url_for("escolha"))
        else:
            error_message = "Usuário ou senha inválidos."
            return render_template("login.html", error=error_message)

    return render_template("login.html")


# Escolher tipo de questionário
@app.route("/escolha")
def escolha():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("escolha.html", username=session["username"])


# Questionário Adulto
@app.route("/adulto", methods=["GET", "POST"])
def adulto():
    if "username" not in session:
        return redirect(url_for("login"))
        
    if request.method == "POST":
        dados = [
            "Adulto",
            request.form.get("nome"),
            request.form.get("idade"),
            "",  # Campo responsável em branco para adulto
            request.form.get("queixa"),
            request.form.get("tempo"),
            request.form.get("sintomas"),
            request.form.get("doencas"),
            request.form.get("medicamentos"),
            request.form.get("alergias"),
        ]

        with open("triagem.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(dados)

        return render_template("sucesso.html", message="✅ Registro de Adulto concluído!")

    return render_template("adulto.html")


# Questionário Criança
@app.route("/crianca", methods=["GET", "POST"])
def crianca():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        dados = [
            "Criança",
            request.form.get("nome"),
            request.form.get("idade"),
            request.form.get("responsavel"),
            request.form.get("queixa"),
            request.form.get("tempo"),
            request.form.get("sintomas"),
            request.form.get("doencas"),
            request.form.get("medicamentos"),
            request.form.get("alergias"),
        ]

        with open("triagem.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(dados)

        return render_template("sucesso.html", message="✅ Registro Infantil concluído!")

    return render_template("crianca.html")

if __name__ == "__main__":
    inicializa_csv()
    # O Railway usa a variável de ambiente PORT para definir a porta
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)