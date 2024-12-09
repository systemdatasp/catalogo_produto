import streamlit as st
from PIL import Image

# Caminho da imagem
image_path = "C:/temp/logo1.jpg"  # Certifique-se de que o caminho está correto

# Interface com Streamlit
try:
    col1, col2, col3 = st.columns([0.50, 0.20, 0.50])
    with col2:
        image = Image.open(image_path)
        st.image(image, width=150)
except Exception as e:
    st.error(f"Erro ao carregar a imagem: {e}")

# Formulário de login com campos de entrada do Streamlit
st.markdown("""
<div style="
    margin: auto; 
    width: 80%; 
    padding: 1px; 
    border: 1px solid red; 
    border-radius: 10px; 
    box-shadow: 15px 15px 8px rgba(20, 0, 0, 0.5); 
    background-color: red; 
    text-align: center;
">
    <h2 style="color: white;">CLASSIFICAÇÃO MERCADORIAS</h2>
</div>
""", unsafe_allow_html=True)

# CSS para estilizar os campos de entrada
st.markdown(
    """
    <style>
    .custom-input {
        background-color: red !important; /* Fundo vermelho */
        color: white !important; /* Texto branco */
        border: 1px solid white; /* Borda branca */
        border-radius: 5px; /* Bordas arredondadas */
        padding: 10px; /* Espaçamento interno */
        width: 100%; /* Largura total */
        font-size: 16px; /* Tamanho da fonte */
    }
    </style>
    """,
    unsafe_allow_html=True
)

coluna5_1,coluna5_2,co
luna5_3,coluna5_4 = st.columns([0.50,0.90,0.70,0.90])
coluna1,coluna2,coluna3,coluna4         = st.columns([0.70,0.90,0.30,0.20])
coluna2_1,coluna2_2,coluna2_3,coluna2_4 = st.columns([0.70,0.90,0.30,0.20])
coluna3_1,coluna3_2,coluna3_3,coluna3_4 = st.columns([0.70,0.90,0.30,0.20])
coluna4_1,coluna4_2,coluna4_3,coluna4_4 = st.columns([0.90,0.90,0.70,0.90])
with st.form("Tela_Login"):
     with coluna2:
       username = st.text_input("**Usuário**", placeholder="Digite seu usuário", max_chars=20)
     with coluna2_2:
       password = st.text_input("**Senha**", placeholder="Digite sua senha", max_chars=20, type="password")
     with coluna3_2:
       login_button = st.button("**Entrar**",use_container_width=True,type="primary")
        
     if login_button:
        consulta = """
                             SELECT login, nome, email
                             FROM catalogo.dbo.usuario
                             WHERE login = '{}' AND password = HASHBYTES('SHA2_256', '{}')
                          """.format(username, password)
            
        try:
          dados = pd.read_sql(consulta, conexao)
          if dados.empty:
             st.error("Usuário ou senha inválidos. Tente novamente.")
          else:
             st.session_state.nome_usuario_logado = dados['nome'][0]
             st.session_state.usuario_logado = dados['login'][0]
             st.session_state.email_logado = dados['email'][0]
                     
             inserir = " insert into catalogo.dbo.login_sistema values ( '{}','{}','Login') ".format(datetime.today().strftime('%Y-%m-%d %H:%M'),username)
             dados = conectar()
             dados.execute ( inserir)
             dados.commit()
             dados.close()
                     
             st.session_state.logged_in = True
        except Exception as e:
          st.error(f"Erro ao conectar ao banco de dados: {e}")
          # Link de recuperação de senha
     with coluna4_2:
          st.markdown('<a href="#" style="color: #007bff; font-size: 12px;">Esqueceu sua senha?</a>', unsafe_allow_html=True)

