import streamlit as st
from PIL import Image

# Caminho da imagem
image_path = "C:/temp/logo1.jpg"  # Certifique-se de que o caminho está correto

# Função a ser chamada após autenticação bem-sucedida
def funcao_pos_login():
    st.success("Login realizado com sucesso!")
    st.write("Bem-vindo ao sistema de classificação de mercadorias!")

# Dicionário de usuários e senhas para autenticação
usuarios_validos = {
    "admin": "1234",
    "usuario": "senha123"
}

try:
    coluna1, coluna2, coluna3 = st.columns([0.50, 0.20, 0.50])
    with coluna2:
        image = Image.open(image_path)
        st.image(image, width=150)
except Exception as e:
    st.error(f"Erro ao carregar a imagem: {e}")

# Quadro de login
st.markdown(
    """
    <div style="
        margin: auto; 
        width: 80%; 
        padding: 30px; 
        border: 1px solid red; 
        border-radius: 10px; 
        box-shadow: 30px 30px 8px rgba(20, 0, 0, 0.5); 
        background-color: red; 
        text-align: center;
    ">
        <h2 style="color: white;">CLASSIFICAÇÃO MERCADORIAS</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# Formulário de login
with st.form("login_form"):
    coluna5_1,coluna5_2,coluna5_3,coluna5_4 = st.columns([0.50,0.90,0.70,0.90])
    coluna1,coluna2,coluna3,coluna4         = st.columns([0.70,0.90,0.30,0.20])
    coluna2_1,coluna2_2,coluna2_3,coluna2_4 = st.columns([0.70,0.90,0.30,0.20])
    coluna3_1,coluna3_2,coluna3_3,coluna3_4 = st.columns([0.70,0.90,0.30,0.20])
    coluna4_1,coluna4_2,coluna4_3,coluna4_4 = st.columns([0.90,0.90,0.70,0.90])
    with coluna2:
         username = st.text_input("**Usuário**", placeholder="Digite seu usuário", max_chars=20)
    with coluna2_2:
         password = st.text_input("**Senha**", placeholder="Digite sua senha", max_chars=20, type="password")
    with coluna3_2:
         login_button = st.form_submit_button("**Entrar**",use_container_width=True,type="primary")
        
    if login_button:
       consulta = """
                             SELECT login, nome, email
                             FROM catalogo.dbo.usuario
                             WHERE login = '{}' AND password = HASHBYTES('SHA2_256', '{}')
                  """.format(username, password)


# Validação de credenciais
if login_button:
    if username in usuarios_validos and usuarios_validos[username] == password:
        funcao_pos_login()
    else:
        st.error("Usuário ou senha inválidos.")
