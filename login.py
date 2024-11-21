import streamlit as st

# Função para exibir a tela de login
def login():
    # Título
    st.title("Login - Sistema Moderno")

    # Criação de uma caixa de texto para o nome de usuário
    username = st.text_input("Usuário", placeholder="Digite seu usuário", max_chars=20)

    # Criação de uma caixa de senha
    password = st.text_input("Senha", placeholder="Digite sua senha", max_chars=20)

    # Botão para submeter o login
    login_button = st.button("Entrar")

    # Verifica se o botão foi pressionado
    if login_button:
        if username == "admin" and password == "admin123":
            st.success("Login bem-sucedido!")
            # Redirecionar ou exibir outra parte da aplicação
            st.write("Bem-vindo ao sistema!")
        else:
            st.error("Usuário ou senha inválidos. Tente novamente.")

# Função para aplicar o estilo
def apply_custom_styles():
    st.markdown("""
        <style>
            /* Cor de fundo da página */
            body {
                background-color: #f7f7f7;
            }

            /* Estilo para o título */
            .css-1v3fvcr {
                font-size: 2.5em;
                color: #4CAF50;
                text-align: center;
            }

            /* Estilo para o texto do login */
            .stTextInput>label {
                font-size: 1.2em;
                color: #333;
            }

            /* Estilo para o botão */
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 1.2em;
                border-radius: 5px;
                padding: 10px;
                width: 100%;
            }

            /* Estilo para o botão ao passar o mouse */
            .stButton>button:hover {
                background-color: #45a049;
            }

            /* Input do campo de senha */
            .stPasswordInput>label {
                font-size: 1.2em;
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)

# Aplicando o estilo
apply_custom_styles()

# Exibindo a tela de login
login()
