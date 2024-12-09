import streamlit as st
from PIL import Image

# Caminho da imagem
image_path = "C:/temp/logo1.jpg"  # Certifique-se de que o caminho está correto

# HTML e CSS para o quadro de login
html_code = """
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
    <form action="" method="post">
        <div style="margin-bottom: 15px;">
            <input type="text" name="username" placeholder="Usuário" style="
                width: 95%; 
                padding: 10px; 
                margin-top: 10px; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            ">
        </div>
        <div style="margin-bottom: 15px;">
            <input type="password" name="password" placeholder="Senha" style="
                width: 95%; 
                padding: 10px; 
                margin-top: 10px; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            ">
        </div>
        <button type="submit" style="
            background-color: red; 
            width: 95%; 
            color: white; 
            padding: 10px 20px; 
            border: 1px solid white; 
            border-radius: 5px; 
            cursor: pointer;
        ">Entrar</button>        
    </form>
    <div style="margin-top: 20px;">
        <a href="#" style="
            color: white; 
            font-size: 14px; 
            text-decoration: underline;
        ">Esqueceu a senha?</a>
    </div>
</div>
"""

try:
    coluna1,coluna2,coluna3 = st.columns([0.50,0.20,0.50])
    with coluna2:
       image = Image.open(image_path)
       st.image(image, width=150)
except Exception as e:
    st.error(f"Erro ao carregar a imagem: {e}")

# Exibe o HTML no Streamlit
st.markdown(html_code, unsafe_allow_html=True)
coluna1,coluna2,coluna3 = st.columns([0.50,0.20,0.90])
coluna3_1,coluna3_2,coluna3_3 = st.columns([0.50,0.20,0.90])
with coluna3:
     st.write('**Version 2.0**')
