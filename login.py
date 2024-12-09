from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Usuário e senha válidos
USERNAME = "admin"
PASSWORD = "admin123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Verifica credenciais
        if username == USERNAME and password == PASSWORD:
            # Redireciona para o aplicativo Streamlit
            return redirect(url_for("tela"))
        else:
            return render_template("login.html", error="Usuário ou senha inválidos")
    return render_template("login.html", error=None)

@app.route("/streamlit")
def streamlit_app():
    # Redireciona para o Streamlit
    return redirect("http://localhost:8501")

if __name__ == "__main__":
    app.run(debug=True)



      "DataConversa": "2024-11-23T20:12:23Z",
                    "DetalhesConversa": {
                        "UsuarioRespostaAnterior": "rsantos@maclogistic.com",
                        "RespostaAnterior": "O que voce precisa ??",
                        "UsuarioResposta": "vsilva@maclogistic.com",
                        "UsuarioPara": "ealmeida@maclogistic.com",
                        "Resposta": "AAAAAAAAAAAAAAAAAA"
                    }
                },