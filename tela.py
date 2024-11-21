from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
from funcoes import conectar
import pandas as pd
from sqlalchemy import create_engine
import urllib
import json
from certificado import autotenticar
from datetime import datetime
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import sys
from streamlit_option_menu import option_menu
from PIL import Image
import io
import base64
import re

st.set_page_config(
    page_title="Catálogo de Produtos",
    page_icon=":material/edit_note:",
    layout="wide"
)

# Inicialize o estado de login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = ''    

if 'nome_usuario_logado' not in st.session_state:
    st.session_state.nome_usuario_logado = ''    
    
st.session_state.cnpj_raiz = ''

if 'Abertura_Chamados' not in st.session_state:
     st.session_state.Abertura_Chamados = False
  
params = urllib.parse.quote_plus("DRIVER={SQL Server};"
                                  "SERVER=172.36.174.15;"
                                  "DATABASE=EMPRESAS;"
                                  "UID=softcargo;"
                                  "PWD=Sist*sql!@"
                                  )

conexao = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# Função para exibir a tela de login
def login():
  if not st.session_state.logged_in:
    
    # Título
    st.header("Acesso  - Catalogo de Produtos ",divider="blue")

    # Criação de uma caixa de texto para o nome de usuário
    username = st.text_input("Usuário", placeholder="Digite seu usuário", max_chars=20,key="usuario_logado")

    # Criação de uma caixa de senha
    password = st.text_input("Senha", placeholder="Digite sua senha", max_chars=20)

    # Botão para submeter o login
    login_button = st.button("Entrar")

    # Verifica se o botão foi pressionado
    if login_button:
        consulta = """
                      select login,nome 
                      from catalogo.dbo.usuario 
                      where login = '{}' and password = HASHBYTES('SHA2_256','{}')
                   """.format(username,password)
        print(consulta)
        dados    = pd.read_sql(consulta,conexao)   
    
        if dados.empty:
            st.error("Usuário ou senha inválidos. Tente novamente.")
        else:
           st.session_state.nome_usuario_logado = dados['nome'][0]
           st.session_state.logged_in = True
           
# Função para aplicar o estilo
#def apply_custom_styles():
#    st.markdown("""
#        <style>
#            /* Cor de fundo da página */
#            body {
#                background-color: #f7f7f7;
#            }

#            /* Estilo para o título */
#            .css-1v3fvcr {
#                font-size: 2.5em;
#                color: #4CAF50;
#                text-align: center;
#            }

#            /* Estilo para o texto do login */
#            .stTextInput>label {
#                font-size: 1.2em;
#                color: #333;
#            }

#            /* Estilo para o botão */
#            .stButton>button {
#                background-color: #4CAF50;
#                color: white;
#                font-size: 1.2em;
#                border-radius: 5px;
#                padding: 10px;
#                width: 100%;
#            }

#            /* Estilo para o botão ao passar o mouse */
#            .stButton>button:hover {
#                background-color: #45a049;
#            }

#            /* Input do campo de senha */
#            .stPasswordInput>label {
#                font-size: 1.2em;
#                color: #333;
#            }
#        </style>
#    """, unsafe_allow_html=True)

# Aplicando o estilo
#apply_custom_styles()

def Campomensagem():
    print('Mensagem Digitado ' + st.session_state["mensagem_chamado"])

def criar_pdf_tecnico():
    c = canvas.Canvas("pdf_com_cabecalho_rodape.pdf", pagesize=letter)
    
    # Adicionar cabeçalho
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Cabeçalho do Documento")
    
    # Adicionar texto principal
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, "Este é um exemplo simples de PDF gerado com Python.")
    
    # Adicionar rodapé
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(100, 30, "Rodapé do Documento - Página 1")
    
    c.save()
                

@st.cache_data
def lista_emails()-> list:
 listagem_emails = []
 consulta =  """select 'Erivaldo de Almeida (ealmeida@maclogistic.com)' as email 
                union all 
                select 'Rivaildo Santos (rsantos@maclogistic.com)' as email 
                union all 
                select 'Joice Arcanjo (jarcanjo@maclogistic.com)' as email 
                union all 
                select 'Vinicius Feliciano (vfeliciano@maclogistic.com)' as email 
                union all 
                select nome+' ('+email+')' as email from catalogo.dbo.emails where cliente = 1 and email <> '' 
             """
 dados = pd.read_sql(consulta,conexao)
 listagem_emails = dados['email'].tolist()
 return listagem_emails
 return dados
                    
@st.cache_data
def lista_paises()-> list:
 listagem_paises = []
 url = "https://restcountries.com/v3.1/all"
 response = requests.get(url)
    
 if response.status_code == 200:
    countries = response.json()
    
    for country in countries:
        pais   = country.get("name", {}).get("common", "")
        codigo = country.get("cca2", "")
        listagem_paises.append(codigo +"-" + pais)
 else:
    print(f"Erro ao acessar a API. Status code: {response.status_code}")       
 return listagem_paises

def lista_subdivisao(pais) -> list :
 listagem_subdivisao = [] 
 url = "https://iso3166-2-api.vercel.app/api/alpha/{}".format(pais)
 response = requests.get(url)
 if response.status_code == 200:     
    resultado = response['subdivisions'].json()  
    #listagem_subdivisao.append("{first_subdivision_code}")
 else:
    print(f"Erro ao acessar a API. Status code: {response.status_code}")
 return listagem_subdivisao


def consultar_raiz_cnpj(cliente):
    consulta =  """select * from catalogo.dbo.cnpj_raiz where idcliente = {}  
                """.format(cliente)
    dados = pd.read_sql(consulta,conexao)
    return dados

def consultaprodutos(idclassificacao):
    consulta =  """select id,data_cadastro,pedido,item,codigo_produto,codigo_ncm,descricao_tecnica,indice_ncm,marca,modelo,cliente,descricao_cliente from catalogo.dbo.classificacao where id = {}  
                """.format(idclassificacao)
             
    dados = pd.read_sql(consulta,conexao)
    return dados
    
@st.cache_data
def listastatus() -> list:
    consulta = """   select  0,'' as nome
                     union all
                     select  id,nome from catalogo.dbo.status d 
               """
    df = pd.read_sql(consulta,conexao)
    lista_status = df['nome'].tolist()
    return lista_status

@st.cache_data
def listaoperadores():
    consulta = """select substring(cnpj_portal,1,10) as cnpj from catalogo.dbo.exportadores group by substring(cnpj_portal,1,10) """
    dados = pd.read_sql(consulta,conexao)
    lista_operadores = dados['cnpj'].tolist()
    return lista_operadores                           

@st.cache_data
def listaclientes() -> list:
    consulta = """   select  0,'' as nome
                     union all
                     select  id,nome from catalogo.dbo.clientes d 
               """
    df = pd.read_sql(consulta,conexao)
    lista_clientes = df['nome'].tolist()
    return lista_clientes

@st.cache_data
def lista_clientes_raiz(cliente) -> list:
    consulta = """   select b.cnpj from catalogo.dbo.cnpj_raiz b left join catalogo.dbo.clientes a on a.id = b.idcliente where nome = '{}'
               """.format(cliente)
    df = pd.read_sql(consulta,conexao)
    lista_clientes = df['cnpj'].tolist()
    return lista_clientes 

def consultar_bancodados(cliente,status,ncm,pedido):
    sfiltro = ""
    consulta = """
                    select    
                          null as Opcao,
                          d.nome as Status,
                          c.nome as Cliente,
                          a.pedido as Pedido,
                          a.item as Item,
                          a.codigo_produto as Codigo,
                          a.codigo_ncm as NCM,
                          a.descricao_tecnica as Descricao_Tecnica,
                          isnull(case when b.data_prev_fornecedor is null  then b.data_prev_embarque 
                                      when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                      when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                      else b.data_prev_fornecedor
                                 end,'') as Meta,
                         b.leadtime_fabrica as Dtnecessidade,
                         a.id,
                         a.marca,
                         a.modelo,
                         a.cliente,
                         a.nrochamado,
                         a.descricao_cliente
                    from catalogo.dbo.classificacao a
                    left join  planilhas_clientes.dbo.produtos_liberados b on b.pedido = a.pedido and a.item = b.item
                    left join  catalogo.dbo.clientes c on c.id = a.cliente
                    left join  catalogo.dbo.status d on d.id = a.status

               """
    if pedido != '':
       if sfiltro == '':
          sfiltro = sfiltro + " where a.pedido = '{}'".format(pedido)
       else:
          sfiltro = sfiltro + " and a.pedido   = '{}'".format(pedido)

    if cliente != '':
       if sfiltro == '':
          sfiltro = sfiltro + " where c.nome = '{}'".format(cliente)
       else:
          sfiltro = sfiltro + " and c.nome   = '{}'".format(cliente)

    if ncm != '':
       if sfiltro == '':
          sfiltro = sfiltro + " where a.ncm = '{}'".format(ncm)
       else:
          sfiltro = sfiltro + " and a.ncm   = '{}'".format(ncm)

    if status != '':
       if sfiltro == '':
          sfiltro = sfiltro + " where d.nome = '{}'".format(status)
       else:
          sfiltro = sfiltro + " and d.nome   = '{}'".format(status)

    if sfiltro == '':
          sfiltro = sfiltro + " where a.status not in (4)"
    else:
          sfiltro = sfiltro + " and a.status not in (4) "
          
    consulta = consulta + sfiltro
    df = pd.read_sql(consulta,conexao)
    return df                                  
 
def detalhes_produtos():
    print('Detalhes')              
       
def capturar_condicionantes_ncm(codigo,resultado,valor,idvalor): 
    for x,valores in enumerate(resultado['detalhesAtributos']):
        if valores['codigo'] == codigo:
            if valores['atributoCondicionante'] == True:
               max_colunas_por_linha = 5
               qtdecolunas1 = len(valores['condicionados'])
               
               colunas_condicionantes   = st.columns(qtdecolunas1)
               for t in range(0, len(valores['condicionados'])):   
                   print('Loop ..: '+str(valores['condicionados']))
                   atributo1            = valores['condicionados'][t]['atributo']['codigo']
                   criterioscondicao    = valores['condicionados'][t]['condicao']['valor']
                   listanovos_atributos = valores['condicionados']
                   nome_campo_1         = valores['condicionados'][t]['atributo']['nomeApresentacao']
                   nome_campo11         = valores['condicionados'][t]['atributo']['nome']
                   tipo1                = valores['condicionados'][t]['atributo']['nomeApresentacao']
                   ajuda                = valores.get('orientacaoPreenchimento', None)
                   tipo1                = valores['condicionados'][t]['atributo']['formaPreenchimento']
                   obrigatorio          = valores['condicionados'][t]['obrigatorio']
                   
                   if tipo1 == 'BOOLEANO':
                      if valor == 'SIM':
                         valor ='true' 
                      if valor == 'NAO':
                         valor = 'false'
                         
                      print('Criterio .: '+str(criterioscondicao)+' Valor .: '+str(valor))
                      if valor == criterioscondicao:
                         tipo = 'BOOLEANO'
                         valor = colunas_condicionantes[t].radio("**"+nome_campo_1+"**", ['SIM', 'NAO'], index=0,key=f"{nome_campo_1+'_'+atributo1+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                   else:    
                        print('2 - Valores .: '+str(valor)+' Criterio .: '+criterioscondicao+' Tipo .: '+tipo1+' Linha . '+str(t)) 
                   
                        valor_campo = valor
                        iposicao = str(valor_campo).find('-')
                        if iposicao >= 0:
                           valor_campo = valor_campo[:iposicao]
                    
                        if valor_campo == 'SIM':
                           valor_campo ='true' 
                        if valor_campo == 'NAO':
                           valor_campo = 'false'
                        
                        if valor_campo == criterioscondicao:
                           if tipo1 == 'LISTA_ESTATICA':
                              tipo  = 'LISTA'
                              listaitens = [f"{item['codigo']}-{item['descricao']}" for item in valores['condicionados'][t]['atributo']['dominio']]
                              valor1 = colunas_condicionantes[t].selectbox("**"+nome_campo_1+"**", options=listaitens, index=0,key=f"{nome_campo_1+'_'+atributo1+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                           elif tipo1 == 'BOOLEANO':
                             tipo    = 'BOOLEANO'
                             valor1  = colunas_condicionantes[t].radio("**"+nome_campo_1+"**", ['SIM', 'NAO'], index=0,key=f"{nome_campo_1+'_'+atributo1+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                           elif tipo1 == 'NUMERO_INTEIRO':
                             tipo    =  'NUMERO_INTEIRO'
                             valor1  = colunas_condicionantes[t].number_input("**"+nome_campo_1+"**", value=0,key=f"{nome_campo_1+'_'+atributo1+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                           elif tipo1 == 'NUMERO_REAL':
                             tipo   =  'NUMERO_REAL'
                             valor1  = colunas_condicionantes[t].number_input("**"+nome_campo_1+"**", value=0.00000,key=f"{nome_campo_1+'_'+codigo+'#'+atributo1+'|'+str(obrigatorio)}",help=ajuda)
                           elif tipo1 == 'TEXTO':
                             tipo   = 'TEXTO'
                             valor1  = colunas_condicionantes[t].text_input("**"+nome_campo_1+"**", value='',key=f"{nome_campo_1+'_'+atributo1+'#'+tipo1+'|'+str(obrigatorio)}",help=ajuda)
                        
                        #else: 
                        #   valor  = colunas_condicionantes[t].text_input("**"+nome_campo_1+"**", value='',key=f"{nome_campo_1+'_'+atributo1+'#'+tipo1+'|'+str(obrigatorio)}",help=ajuda)
           
         
def montarcondicionantes(nomecampo,codigo,valor,idvalor):
  #  itotal = len(st.session_state)
  #  for i,(campo,valor) in enumerate(st.session_state.items()):
  #      campo = campo
  #      valor = valor
    
  #  ilocalizar = campo.find('_')
  #  if ilocalizar >= 0:
  #     campo = campo[:ilocalizar]    
  #  if valor == 'SIM':
  #     valor = True
  #  else:
  #     valor = False
    
  #  chaves = st.session_state['chaves_json']
  #  for x,valores in enumerate(chaves):
  #      if valores['Atributo'] == codigo:
  #         if valores['Chave'] == campo:
  #            print(valores['Condicionados'])
  
  print(nomecampo+'#'+codigo+"#")
  
       #qtdecolunas = len(resultado['detalhesAtributos'])
       #max_colunas_por_linha = 5

   #    qtdecolunas1 = len(resultado['condicionados'])
       #colunas2 = st.columns(qtdecolunas1)
       #for t in range(0, len(resultado['condicionados'])):   
       #    atributo1            = resultado['condicionados'][t]
       #    criterioscondicao    = resultado['condicionados'][t]['condicao']
       #    listanovos_atributos = resultado['condicionados'][t]
       #    nome_campo_1         = listanovos_atributos['atributo']['nomeApresentacao']
       #    nome_campo11         = listanovos_atributos['atributo']['nome']
       #    codigo1              = listanovos_atributos['atributo']['codigo']
       #    titulo1              = listanovos_atributos['atributo']['nomeApresentacao']
       #    ajuda1               = listanovos_atributos.get('orientacaoPreenchimento', None)
       #    tipo1                = listanovos_atributos['atributo']['formaPreenchimento']
       #    obrigatorio          = valores['Condicionados'][t]['obrigatorio']
            
       #    valor                = colunas2.text_input("**"+titulo1+"**", value='',key=f"{nome_campo1+'_'+codigo1+'#'+tipo1+"|"+str(obrigatorio)}",help=ajuda1)
 
card_style = """
   <style>
   .card_titulo {
      #  background-color: #FFFFFF;
        padding: 5px;
        margin: 1px 0;
        border-radius: 5px;
        box-shadow: 2px 2px 8px rgba(255, 0, 0, 1);
        text-align: center;
     #   color: #000000;
        textColor=#000000;
    }
    .card {
        background-color: #FFFFFF;
        padding: 5px;
        margin: 1px 0;
        border-radius: 2px;
        box-shadow: 2px 2px 8px  rgba(255, 0, 0, 1);
        text-align: center;
        color:#000000;
        textColor=#000000;
    }   
        
    .card img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-bottom: 20px;
    }
    
    .button-aligned {
        display: flex;
        align-items: center;
        height: 100%;
        margin-top: 27px; /* Ajuste esse valor para alinhar melhor */
    }
    
    .button-aligned-resposta {
        display: flex;
        align-items: center;
        height: 100%;
        margin-top: 27px; /* Ajuste esse valor para alinhar melhor */
    }
    </style>
"""    

st.sidebar.markdown(
    """
    <style>
    .sidebar-img {
        width: 5%;  /* Ajusta para 100% da largura da barra lateral */
       # height: auto; /* Mantém a proporção da imagem */
        height: 10px;  
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Seleciona o botão de submit e altera as cores */
    div.stButton > button {
        background-color: #4CAF50; /* Cor de fundo */
        color: white;              /* Cor do texto */
        border-radius: 8px;        /* Bordas arredondadas */
        width: 100%;               /* Largura do botão */
        height: 25px;              /* Altura do botão */
    }
    
    /* Cor de fundo do botão ao passar o mouse */
    div.stButton > button:hover {
        background-color: #45a049;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Seleciona o botão de submit e altera as cores */
    div.stButton > button {
        background-color: #4CAF50; /* Cor de fundo */
        color: white;              /* Cor do texto */
        border-radius: 8px;        /* Bordas arredondadas */
        width: 100%;               /* Largura do botão */
        height: 25px;              /* Altura do botão */
    }
    
    /* Cor de fundo do botão ao passar o mouse */
    div.stButton > button:hover {
        background-color: #45a049;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Seleciona o botão de submit e altera as cores */
    div.stform_submit_button > button {
        background-color: #4CAF50; /* Cor de fundo */
        color: white;              /* Cor do texto */
        border-radius: 8px;        /* Bordas arredondadas */
        width: 100%;               /* Largura do botão */
        height: 25px;              /* Altura do botão */
    }
    
    /* Cor de fundo do botão ao passar o mouse */
    div.stform_submit_button > button:hover {
        background-color: #45a049;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Altera a fonte da sidebar */
    .css-1d391kg {
        font-family: 'Arial', sans-serif;
        font-size: 8px;
        font-weight: bold;
      #  color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Define o tamanho da fonte padrão para a página */
    html, body, [class*="css"] {
        font-size: 9px; /* Ajuste o tamanho da fonte conforme desejado */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    .small-header {
        font-size: 9px; /* Ajuste o tamanho da fonte aqui */
        color: #333333; /* Cor opcional */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Reduz o tamanho da fonte para st.dataframe */
    .dataframe tbody tr, .dataframe thead tr {
        font-size: 8px; /* Ajuste o tamanho da fonte conforme necessário */
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.example.com/image.jpg");
    }
   </style>
    """,
    unsafe_allow_html=True
)    
    
st.markdown(
    """
    <style>
    .nav-link {
        font-size: 8px !important;  /* Ajuste o tamanho da fonte conforme necessário */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* Altera os botões do radio para ficarem redondos */
    .st.radio div[data-baseweb="radio"] > label {
        border-radius: 50%;
        border: 2px solid #333;
        padding: 8px;
        margin-right: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.5em;
        height: 1.5em;
    }
    /* Estilo do círculo selecionado */
    .st.radio div[data-baseweb="radio"] > label[data-selected="true"] {
        background-color: #4CAF50;
        color: #FFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

consultarncm = ''  

def consultar_atributos_ncm(consultarncm,situacaomodalidade,idvalor) -> list:
    resultado = autotenticar()      
    try:           
        if resultado is None:
           st.subheader("Alerta Sistema", divider=True)
           st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(resultado))
        else:
         for header, value in resultado.items():
           if 'set-token' in header:
               set_token = value
           if 'x-csrf-token' in header:
              x_csrf_token = value
                                     
         url = f"https://val.portalunico.siscomex.gov.br/cadatributos/api/ext/atributo-ncm/{consultarncm}?modalidade={situacaomodalidade}"
         headers = {
              'Authorization': set_token,
              'X-CSRF-Token': x_csrf_token,
              'Content-Type': 'application/json'
         }     
       
         response = requests.get(url, headers=headers)
         resultado = response.json()
             
         montagemjson_lista = []
         if response.status_code != 200:
            st.subheader("Alerta Sistema", divider=True)
            st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(resultado))
   
         else:
            st.subheader("Atributos", divider=True)
            if 'detalhesAtributos' in resultado and isinstance(resultado['detalhesAtributos'], list):
                qtdecolunas = len(resultado['detalhesAtributos'])
                max_colunas_por_linha = 5
  
            for i in range(0, len(resultado['detalhesAtributos']), max_colunas_por_linha):
                colunas = st.columns(min(max_colunas_por_linha, qtdecolunas - i))
                
                for j, coluna in enumerate(colunas):
                    atributo    = resultado['detalhesAtributos'][i + j]['codigo']
                    nome_campo  = resultado['detalhesAtributos'][i + j]['nomeApresentacao']
                    codigo      = resultado['detalhesAtributos'][i + j]['codigo']
                    titulo      = resultado['detalhesAtributos'][i + j]['nomeApresentacao']
                    
                    try:
                        ajuda = resultado['detalhesAtributos'][i + j].get('orientacaoPreenchimento', "")
                    except (IndexError, TypeError, KeyError) as e:
                        ajuda = ""
                        
                    obrigatorio = resultado['detalhesAtributos'][i + j]['obrigatorio']
                 
                    if resultado['detalhesAtributos'][i + j]['formaPreenchimento'] == 'TEXTO':
                       tipo = 'TEXTO'
                       valor = coluna.text_input("**"+titulo+"**", value='',key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                       montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
                    elif resultado['detalhesAtributos'][i + j]['formaPreenchimento'] == 'NUMERO_INTEIRO':
                       tipo =  'NUMERO_INTEIRO'
                       valor = coluna.number_input("**"+titulo+"**", value=0,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                       montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
                    elif resultado['detalhesAtributos'][i + j]['formaPreenchimento'] == 'NUMERO_REAL':
                       tipo =  'NUMERO_REAL'
                       valor = coluna.number_input("**"+titulo+"**", value=0.00000,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                       montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
                    elif resultado['detalhesAtributos'][i + j]['formaPreenchimento'] == 'BOOLEANO':
                       tipo = 'BOOLEANO'
                       valor = coluna.radio("**"+titulo+"**", ['SIM', 'NAO'], index=1,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                       montagemjson = dict(Atributo=codigo, Chave=titulo, Valores=['SIM','NAO'], Tipo=tipo,Obrigatoriedade=obrigatorio)
                       capturar_condicionantes_ncm(codigo,resultado,valor,idvalor)
                    elif resultado['detalhesAtributos'][i + j]['formaPreenchimento'] == 'LISTA_ESTATICA':
                       tipo = 'LISTA'
                       listaitens = [f"{item['codigo']}-{item['descricao']}" for item in resultado['detalhesAtributos'][i + j]['dominio']]
                       valor = coluna.selectbox("**"+titulo+"**", options=listaitens, index=0,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                       capturar_condicionantes_ncm(codigo,resultado,valor,idvalor)
                       montagemjson = dict(Atributo=codigo, Chave=titulo, Valores=listaitens, Tipo=tipo,Obrigatoriedade=obrigatorio)
                    else:
                      valor = None
                      
                    montagemjson_lista.append(montagemjson)
            return montagemjson_lista  
        
    except requests.exceptions.HTTPError as errh:
        st.subheader("Alerta Sistema", divider=True)
        st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(errh))
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        st.subheader("Alerta Sistema", divider=True)
        st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(errt))
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
   
def consultar_atributos_ncm_cadastrado(idclassificacao) -> list:
     montagemjson_lista = []
     st.subheader("Atributos", divider=True)

     consulta = """
                select * from catalogo.dbo.detalhes_classificacao
                where idclassificacao = {}
               """.format(idclassificacao)
               
     bddados   = conectar()
     cursor    = bddados.execute(consulta)
     qtdelinha = len(cursor.fetchall())
     bddados.close()
     
     bddados   = conectar()
     cursor    = bddados.execute(consulta)
     linha     = cursor.fetchone()
     
     max_colunas_por_linha = 5
          
     montagemjson = ''

     while linha:
         for i in range(0, qtdelinha, max_colunas_por_linha):
             colunas = st.columns(min(max_colunas_por_linha, qtdelinha - i))
             for j, coluna in enumerate(colunas):
                 atributo    = linha[2]
                 nome_campo  = linha[3]
                 nome_campo1 = linha[3]
                 codigo      = linha[2]
                 titulo      = linha[3]
                 titulo1     = linha[3]
                 obrigatorio = linha[7]
                 tipo        = linha[5]
                 ajuda       = linha[8]
                
                 if linha[5] == 'TEXTO':
                    tipo = 'TEXTO'
                    valor = coluna.text_input("**"+titulo+"**", value=linha[4],key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                    montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
    
                 elif linha[5] == 'NUMERO_INTEIRO':
                    tipo =  'NUMERO_INTEIRO'
                    valor = coluna.number_input("**"+titulo+"**", value=int(linha[4]),key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                    montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
                            
                 elif linha[5] == 'NUMERO_REAL':
                    tipo =  'NUMERO_REAL'
                    valor = coluna.number_input("**"+titulo+"**", value=float(linha[4]),key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                    montagemjson = dict(Atributo=codigo, Chave=titulo, Valores='', Tipo=tipo,Obrigatoriedade=obrigatorio)
             
                 elif linha[5] == 'BOOLEANO':
                    tipo = 'BOOLEANO'
                    try:
                       if linha[4] == 'SIM':
                          index_selecionado = 0
                       else:
                          index_selecionado = 1
                    except ValueError:
                          index_selecionado = 0  

                    valor = coluna.radio("**"+titulo+"**", ['SIM', 'NAO'], index=index_selecionado,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}",help=ajuda)
                    montagemjson = dict(Atributo=codigo, Chave=titulo, Valores=['SIM', 'NAO'], Tipo=tipo,Obrigatoriedade=obrigatorio)
                 
                 elif linha[5] == 'LISTA':
                      lista = linha[6].split('#')
                      listaitens = lista
                      try:
                         index_selecionado = listaitens.index(linha[4])
                      except ValueError:
                         index_selecionado = 0  
                      tipo = 'LISTA'
                      valor = coluna.selectbox("**"+titulo+"**", options=listaitens, index=index_selecionado,key=f"{nome_campo+'_'+codigo+'#'+tipo+'|'+str(obrigatorio)}")
                      montagemjson = dict(Atributo=codigo, Chave=titulo, Valores=listaitens, Tipo=tipo,Obrigatoriedade=obrigatorio)
                 
                 else:
                    valor = None
                       
                 montagemjson_lista.append(montagemjson)
                 linha = cursor.fetchone()
  
     return montagemjson_lista   
     
def main_content():
    if st.session_state.logged_in:
          st.subheader("Bem-vindo , " + str(st.session_state['nome_usuario_logado']),divider="red") 
          # Carregando a imagem
          image_path = "C:/temp/logo1.jpg"  # Certifique-se de que o caminho está correto
          image = Image.open(image_path)
           
          menu_options = ['Tarefas','Classificação', 'Importar Arquivo', 'Cadastro NCM', 'Operador Estrangeiro','Clientes','Sair']    
          with st.sidebar:
               choice = option_menu("Menu Principal",menu_options,
               icons=["gear","bi-journal-text", "bi-cloud-upload","bi-database-gear", "globe","bi-person-lines-fill"],  
               menu_icon="app-indicator", default_index=0,
               styles={
                        "container": {"padding": "5px", "background-color": "#f0f2f6"},
                        "icon": {"color": "blue", "font-size": "18px"},  # Tamanho dos ícones
                        "nav-link": {"font-size": "10px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#FF0000"},
                         "menu-title": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},  # Ajuste o tamanho da fonte do título aqui
                    }
            )
      
          if choice == 'Tarefas':
             st.markdown(card_style, unsafe_allow_html=True)
             st.markdown(f"""
                            <div class="">
                            <h4><b>Catálogo de Produtos</h4></b>
                            </div>
                           """, 
                            unsafe_allow_html=True)
            
             col1_1,col1_2 = st.columns(2)
             col2_1,col2_2 = st.columns(2)
            
             consulta = """
                            select c.nome as Cliente,
                                d.tipo_pedido as 'Tipo Pedido',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) > 60 then 1
                                end) as 'A Classificar > 60 dias',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) between 30 and 59  then 1
                                end) as 'Classificar - 50 a 30',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) <  1  then 1
                                end) as 'Atrasados > Embarque'
                            from catalogo.dbo.classificacao a
                            left join  planilhas_clientes.dbo.produtos_liberados b on b.pedido = a.pedido and a.item = b.item
                            left join  planilhas_clientes.dbo.produtos  d on d.pedido = a.pedido and d.item = b.item
                            left join  catalogo.dbo.clientes c on c.id = a.cliente
                            where a.status in (0,1,2) 
                            group by c.nome,d.tipo_pedido
                    """
        
             df = pd.read_sql(consulta,conexao)
             st.subheader("Resumo Atividades - Novos Pedidos", divider="red") 
             st.dataframe(df,use_container_width=True,width=300,selection_mode="single-row")   

             st.subheader("Revisão Pedidos - Já Classificados", divider="red")                    
             consulta = """
                            select c.nome as Cliente,
                                d.tipo_pedido as 'Tipo Pedido',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) > 60 then 1
                                end) as 'A Classificar > 60 dias',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) between 30 and 59  then 1
                                end) as 'Classificar - 50 a 30',
                                count(case when (
                                        case when b.data_prev_fornecedor is null       then b.data_prev_embarque 
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor > b.data_prev_embarque then b.data_prev_embarque
                                                when b.data_prev_fornecedor is not null and b.data_prev_fornecedor < b.data_prev_embarque then b.data_prev_fornecedor
                                                else   b.data_prev_fornecedor
                                        end ) <  1  then 1
                                end) as 'Atrasados > Embarque'
                            from catalogo.dbo.classificacao a
                            left join  planilhas_clientes.dbo.produtos_liberados b on b.pedido = a.pedido and a.item = b.item
                            left join  planilhas_clientes.dbo.produtos  d on d.pedido = a.pedido and d.item = b.item
                            left join  catalogo.dbo.clientes c on c.id = a.cliente
                            where a.status = 3 
                            group by c.nome,d.tipo_pedido
                    """
             df = pd.read_sql(consulta,conexao)

             st.dataframe(df,use_container_width=True,width=300,selection_mode="single-row")   
                                        
             with col2_1:
                st.markdown(f"""
                        <div class="card">
                        <img width="300" height="300" align="center" src="https://img.icons8.com/carbon-copy/100/note.png" alt="note"/>
                        <h5><b> CHAMADOS ABERTOS</h5></b>
                        <h7><b>000</h7></b>
                        </div>
                        """, 
                        unsafe_allow_html=True
                        )    
             with col2_2:
                st.markdown(f"""
                        <div class="card">
                        <img width="200" height="200" src="https://img.icons8.com/color/48/about.png" alt="about"/>
                        <h5><b><b> NOVIDADES</h5></b>
                        <h7><b>000</h7></b>
                        </div>
                        """, 
                        unsafe_allow_html=True
                        )  
          if choice == 'Classificação':               
                      #selected_rows = None
                      st.markdown(card_style, unsafe_allow_html=True)
                      st.markdown(f"""
                            <div class="card_titulo">
                            <h4><b>Classificação</h4></b>
                            </div>
                            """, 
                            unsafe_allow_html=True)
                 
                      st.subheader("Filtros", divider="red")
                      coluna1,coluna2,coluna3,coluna4,coluna5,coluna6,coluna7 = st.columns([0.20,0.20,0.20,0.20,0.20,0.20,0.20])  
                      with coluna1:
                           lista_clientes = listaclientes()
                           clientes = st.selectbox("**Cliente:**", options=lista_clientes,index=0)
                      with coluna2:
                           listastatus_processos = listastatus()
                           lista_status = st.selectbox("**Status:**", options=listastatus_processos,index=0)
                      with coluna3:
                           Pedido = st.text_input("**Pedido:**")
                      with coluna4:
                           NCM = st.text_input("**NCM:**")
                      with coluna5:
                           Data_Inicial = st.text_input("**Data Inicial**", value=datetime.today().strftime('%Y-%m-%d'))
                      with coluna6:
                           Data_Final  = st.text_input("**Data Final**", value=datetime.today().strftime('%Y-%m-%d'))   
                      with coluna7:     
                          st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                          pesquisar_cnpj = st.button('Consultar',use_container_width=True,type='primary',icon=":material/search:")
                          st.markdown('</div>', unsafe_allow_html=True)
                  
                      st.subheader("Produtos Classificar", divider="red")     
                      
                      if clientes == None:
                         clientes = ''                  
                      basedados = consultar_bancodados(clientes,lista_status,NCM,Pedido)
                      gb = GridOptionsBuilder.from_dataframe(basedados)
                      gb.configure_column("Opcao", width=50,header_name="Opcao", cellStyle={"textAlign": "center"})
                      gb.configure_column("Pedido", width=50)
                      gb.configure_column("Cliente", width=100) 
                      gb.configure_column("ID", width=20) 
                      gb.configure_default_column(cellStyle={'font-size': '10px'})
                      gb.configure_selection('single', use_checkbox=True)
                      grid_options = gb.build()

                      # Exibe o grid
                      grid_response = AgGrid(basedados, gridOptions=grid_options,enable_enterprise_modules=True, allow_unsafe_jscode=True)          
                      selected_rows = grid_response['selected_rows']                
                     
                      st.subheader("**Cadastrar Produtos**", divider="red")  
                                
                      idclassificacao = 0                    
                        
                      if pesquisar_cnpj:                  
                         basedados = consultar_bancodados(clientes,lista_status,NCM,Pedido)
                         gb = GridOptionsBuilder.from_dataframe(basedados)
                         gb.configure_column("Opcao", width=50,header_name="Opcao", cellStyle={"textAlign": "center"})
                         gb.configure_column("Pedido", width=50)
                         gb.configure_column("Cliente", width=100) 
                         gb.configure_column("ID", width=20) 
                         gb.configure_default_column(cellStyle={'font-size': '10px'})
                         gb.configure_selection('single', use_checkbox=True)
                         grid_options = gb.build()

                            # Exibe o grid
                         grid_response = AgGrid(basedados, gridOptions=grid_options,enable_enterprise_modules=True, allow_unsafe_jscode=True)          
                        
                        #selected_rows = grid_response["selected_rows"]
                      tab1, tab2 = st.tabs(["Classificacao", "Chamados"])
                      with tab1:    
                        if selected_rows is not None:
                            with st.form("Painel_Classificacao"):    
                                
                                idclassificacao = selected_rows['id'].values[0]
                                
                                ## Verificando se ja esta cadastrado essa seleção     
                                lista_exportadores = listaoperadores()                     
                                        
                                modalidade = ['IMPORTACAO','EXPORTACAO']
                            
                                consulta =   """select convert(varchar(2),id)+'-'+nome as situacao from catalogo.dbo.situacao """
                                dados = pd.read_sql(consulta,conexao)
                                        
                                situacao = dados['situacao'].tolist() 
                                
                                consulta = "select convert(varchar(10),0) as codigo,'' as atributo union all select codigo,codigo+'-'+convert(varchar(8000),descricao) as atributo from catalogo.dbo.atualizacao_ncm"
                                                
                                dados = pd.read_sql(consulta,conexao)
                                listancm = dados['atributo'].tolist() 
                                            
                                consulta_produtos = consultaprodutos(idclassificacao) 
                                
                                colunas1,colunas2,colunas3,colunas4,colunas5,colunas6,colunas7,colunas8 = st.columns([0.29,0.35,0.45,0.20,0.20,0.50,0.50,0.50])
                                col1_1,col1_2,col1_3,col1_4,col1_5,col1_6 = st.columns([0.20,0.50,0.25,0.45,0.45,0.45])
                                col2_1,col2_2= st.columns([0.50,0.50])
                                col3_1,col3_2,col3_3,col3_4= st.columns(4)

                                if not consulta_produtos.empty:
                                    with colunas1:
                                        idclassificacao =st.text_input('**ID**',key= idclassificacao,value=str(consulta_produtos['id'].values[0]),disabled=True)
                                    with colunas2:
                                        st.text_input('**Código Portal**',disabled=True)
                                    with colunas3:
                                        cnpjlista = st.selectbox('**CNPJ Responsável:**'+' *',key="cnpjlista",options=lista_exportadores)
                                    with colunas4:
                                        pedidos = st.text_input('**Pedido:**',key="pedidos",value = str(consulta_produtos['pedido'].values[0]))
                                    with colunas5:
                                        itempedido = st.text_input('**Item:**',key="itempedido",value = str(consulta_produtos['item'].values[0]))
                                    with colunas6:
                                        codigoproduto = st.text_input('**Código do produto:**',key="codigoproduto",value = str(consulta_produtos['codigo_produto'].values[0]) if consulta_produtos['codigo_produto'].values[0] is not None else '')
                                    with colunas7:
                                        listasituacao = st.selectbox('**Situação:**',key="listasituacao",options=situacao)
                                    with colunas8:
                                        situacaomodalidade = st.selectbox('**Modalidade de operação:**'+' *',key="situacaomodalidade",options=modalidade)
                                    with col1_1:
                                        ncm_produto = st.text_input('**NCM Cliente:**',key="ncm_produto",value = str(consulta_produtos['codigo_ncm'].values[0]))
                                    with col1_2:
                                        try:
                                            index_selecionado = listancm.index(consulta_produtos['indice_ncm'].values[0])
                                        except ValueError:
                                            index_selecionado = 0  

                                        ncm_classificado = st.selectbox('**NCM Mac:**'+' *',key="ncm_classificacao",options=listancm,index=index_selecionado)
                                    with col1_3:
                                        st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                        pesquisar_ncm   = st.form_submit_button('NCM',use_container_width=True,type='primary',icon=":material/search:") 
                                        st.markdown('</div>', unsafe_allow_html=True)                       
                                
                                    with col1_4:
                                        unidade_medida = st.text_input('**Unidade de medida estatística:**',key="unidade_medida",value='UNIDADE')
                                    with col1_5:
                                        marca = st.text_input('**Marca:**',key="marca",value=str(consulta_produtos['marca'].values[0]) if consulta_produtos['marca'].values[0] is not None else '' )
                                    with col1_6:
                                        modelo = st.text_input('**Modelo:**',key="modelo",value=str(consulta_produtos['modelo'].values[0]) if consulta_produtos['modelo'].values[0] is not None else '' )
                                        
                                    with col2_1:
                                        descricao_ncm = st.text_area('**Denominação Produto:**'+' *',key="descricao_ncm",value = consulta_produtos['descricao_cliente'].values[0] if consulta_produtos['descricao_cliente'].values[0] is not None else '' )
                                    with col2_2:
                                        descricao_Mac = st.text_area('**Descrição Complementar:**'+' *',key="descricao_mac",value = consulta_produtos['descricao_tecnica'].values[0] if consulta_produtos['descricao_tecnica'].values[0] is not None else '' )
                                        
                                    consulta =  """select * from catalogo.dbo.detalhes_classificacao where idclassificacao = '{}' 
                                                """.format(idclassificacao)
                                    dados = pd.read_sql(consulta,conexao)
                
                                else:
                                    codigo_produto = selected_rows['Codigo'].values[0]
                                    with colunas1:
                                        idclassificacao =st.text_input('ID',selected_rows['id'].values[0],disabled=True)
                                    with colunas2:
                                        st.text_input('**Código Portal:**',disabled=True)
                                    with colunas3:
                                        lista_clientes = lista_clientes_raiz(selected_rows['cliente'].values[0]) 
                                        itens = '\n'.join(lista_clientes)   
                                        cnpj_lista = st.selectbox('**CNPJ Responsável:**'+' *',key= "cnpjlista",options=itens)
                                    with colunas4:
                                        pedidos = st.text_input('**Pedido:**',value = selected_rows['Pedido'].values[0])
                                    with colunas5:
                                        itempedido = st.text_input('**Item:**',value =selected_rows['Item'].values[0])
                                    with colunas6:
                                        codigoproduto = st.text_input('**Código do produto:**',value = selected_rows['Codigo'].values[0] if selected_rows['Codigo'].values[0] is not None else '' )
                                    with colunas7:
                                        listasituacao = st.selectbox('**Situação:**',options=situacao)
                                    with colunas8:
                                        situacaomodalidade = st.selectbox('**Modalidade de operação:**'+' *',options=modalidade)
                                    with col1_1:
                                        ncm_produto = st.text_input('**NCM Cliente:**',value = selected_rows['NCM'].values[0])
                                    with col1_2:
                                        ncm_classificado = st.selectbox('**NCM Mac:**'+' *',key="ncm_classificacao",options=listancm)
                                    with col1_3:
                                        st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                        pesquisar_ncm   = st.form_submit_button('NCM',use_container_width=True,type='primary',icon=":material/search:") 
                                        st.markdown('</div>', unsafe_allow_html=True)
                                                            
                                    with col1_4:
                                        unidade_medida = st.text_input('**Unidade de medida estatística:**',value='UNIDADE')
                                    with col1_5:
                                        marca = st.text_input('**Marca:**',key="Marca",value = selected_rows['Marca'].values[0] if selected_rows['Marca'].values[0] is not None else '' )
                                    with col1_6:
                                        modelo = st.text_input('**Modelo:**',key="Modelo",value = selected_rows['Modelo'].values[0] if selected_rows['Moedelo'].values[0] is not None else '' )  
                                                                        
                                    with col2_1:
                                        descricao_ncm = st.text_area('**Denominação Produto:**'+' *',key="descricao_ncm",value = selected_rows['Descricao_cliente'].values[0] if selected_rows['Descricao_cliente'].values[0] is not None else '' )
                                    with col2_2:
                                        descricao_Mac = st.text_area('**Descrição Complementar:**'+' *',key="descricao_mac",value = selected_rows['Descricao_Tecnica'].values[0] if selected_rows['Descricao_Tecnica'].values[0] is not None else '' )
                                with col3_1:
                                    st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                    incluir   = st.form_submit_button('Incluir / Alterar',use_container_width=True,type='primary',icon=":material/save:") 
                                    st.markdown('</div>', unsafe_allow_html=True)
                                with col3_4: 
                                    st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                    enviarportal = st.form_submit_button('Enviar Portal',type='primary',use_container_width=True,icon=":material/web:") 
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                if incluir:
                                    usuario = 'AUT' 
                                    exclusao = """
                                                delete from catalogo.dbo.detalhes_classificacao where idclassificacao = '{}'
                                            """.format(idclassificacao)
                                    bdados = conectar()
                                    bdados.execute(exclusao)
                                    bdados.commit()
                                    bdados.close()     
                                    
                                    descricao_mac_string = descricao_Mac
                                    
                                    descricao_mac_string = descricao_mac_string.replace('\r', '')
                                    
                                    inclusao = """
                                                update catalogo.dbo.classificacao set codigo_produto = '{}',situacao = '{}',modalidade = '{}',ncm_mac = '{}',descricao_tecnica = '{}',usuario = '{}',indice_ncm = '{}',data_cadastro = '{}',marca = '{}',modelo = '{}',cnpj_raiz = '{}',descricao_cliente = '{}'
                                                where id = '{}'
                                            """.format(codigoproduto,listasituacao[:1],situacaomodalidade,ncm_classificado[:10],descricao_mac_string,usuario,ncm_classificado,datetime.today().strftime('%Y-%m-%d'),marca,modelo,cnpjlista,descricao_ncm,idclassificacao)
                                    bdados = conectar()
                                    bdados.execute(inclusao)
                                    print(inclusao)
                                    bdados.commit()
                                    #bdados.close()                            
            
                                    itenscadastro = ''
                                    atributos = []
                                    valor = ''
                                    inclusaoatributos = ''                                             
        
                                    for chave, valor in st.session_state.items():
                                        if 'FormSubmitter' not in chave and 'show_form' not in chave and 'cnpj_raiz' not in chave and 'current_selection' not in chave and 'chaves_json' not in chave and 'values' not in chave and 'classificacao' not in chave and 'listapaise' not in chave and 'bota' not in chave and 'show_dialog' not in chave and 'itempedido' not in chave and 'unidade_medida' not in chave:
                                          #  print('Chave ..: '+str(chave)+' Valor ..: '+str(valor))
                                            
                                            ilocalizar  = chave.find('_ATT_')
                                            
                                            if ilocalizar >=0:
                                               ilocalizar  = chave.find('_')
                                               atributos   = chave[ilocalizar+1:]               
                                               ilocalizar1 = atributos.find('#')
                                               atributos   = atributos[:ilocalizar1]
                        
                                               ilocalizar1 = chave.find('#')
                                               tipo_campo  = chave[ilocalizar1+1:]
                                               ilocalizar4 = tipo_campo.find('|')
                                               tipo_campo  = tipo_campo[:ilocalizar4]
                                             
                                               ilocalizar2  = chave.find('_')
                                               nomecampo    = chave[:ilocalizar2]     
                                            
                                               ajuda = ''
                                            
                                               ilocalizar3 = chave.find('|')
                                               obrigatorio = chave[ilocalizar3+1:]  
                                                                    
                                               dados_chaves_json = []
                                               listadados = []
                                               montagemjson_lista =''
                                               dados_chaves_json = []
                                               itenscadastro = ''    
                                        
                                               dados_chaves_json = st.session_state["chaves_json"]
                                               #print('Chave Json ..: '+str(st.session_state["chaves_json"]))
                                                                                        
                                               if isinstance(dados_chaves_json, list):
                                                  for item in dados_chaves_json:
                                                      if isinstance(item, dict):
                                                         for itenschave, valor_chave in item.items():
                                                             if valor_chave == nomecampo:                                                   
                                                                valores = item.get('Valores', [])
                                                                valores1 = ''
                                                                for valor1 in valores:
                                                                    valores1 = valores1 +valor1+'#'
                                                                montagemjson_lista = montagemjson_lista + valores1  
                                                    
                                               inclusao_ncm = """
                                                            insert into catalogo.dbo.detalhes_classificacao(idclassificacao,atributo,chave,valor,tipo,historico,obrigatorio,ajuda) values ('{}','{}','{}','{}','{}','{}','{}','{}')
                                                            """.format(idclassificacao,atributos,nomecampo,valor,tipo_campo,montagemjson_lista,obrigatorio,ajuda)
                                            
                                              # print(inclusao_ncm)
                                              # print(montagemjson_lista)
                                               montagemjson_lista = ''
                                               bdados = conectar()
                                               bdados.execute(inclusao_ncm)
                                               bdados.commit()
                                               bdados.close()                    
                                            
                                    try:
                                        st.success('Produto Incluído / Alterado com Sucesso !')
                                    except e:
                                        st.warning('Produto não Cadastro , Erro :', e)
                                        
                                    selected_rows = None    

                                if enviarportal: 
                                    usuario = 'AUT'
                                    exclusao = """
                                    #            delete from catalogo.dbo.detalhes_classificacao where idclassificacao = '{}'
                                    #        """.format(idclassificacao)
                                   # bdados = conectar()
                                  #  bdados.execute(exclusao)
                                  #  bdados.commit()
                                  #  bdados.close()     
                                    
                                    inclusao = """
                                                update catalogo.dbo.classificacao set codigo_produto = '{}',situacao = '{}',modalidade = '{}',ncm_mac = '{}',descricao_tecnica = '{}',usuario = '{}',indice_ncm = '{}',data_cadastro = '{}',marca = '{}',modelo = '{}',cnpj_raiz = '{}',descricao_cliente = '{}'
                                                where id = '{}'
                                            """.format(codigoproduto,listasituacao[:1],situacaomodalidade,ncm_classificado[:10],descricao_Mac,usuario,ncm_classificado,datetime.today().strftime('%Y-%m-%d'),marca,modelo,cnpjlista,descricao_ncm,idclassificacao)
                                    bdados = conectar()
                                    bdados.execute(inclusao)
                                #    print(inclusao)
                                    bdados.commit()
                                    bdados.close()                            
            
                                    itenscadastro = ''
                                    atributos = []
                                    valor = ''
                                    inclusaoatributos = ''                                             
        
                                    lista_formatada = [f"{chave}: {valor}" for chave, valor in st.session_state.items()]
                             
                                    for chave, valor in st.session_state.items():
                                        if 'FormSubmitter' not in chave and 'show_form' not in chave and 'cnpj_raiz' not in chave and 'current_selection' not in chave and 'chaves_json' not in chave and 'values' not in chave and 'classificacao' not in chave and 'listapaise' not in chave and 'bota' not in chave and 'show_dialog' not in chave and 'itempedido' not in chave and 'unidade_medida' not in chave:
                                            print('Chave ..: '+str(chave)+' Valor ..: '+str(valor))
                                            
                                            ilocalizar  = chave.find('_ATT_')
                                            
                                            if ilocalizar >=0:                
                                               ilocalizar  = chave.find('_')
                                               atributos   = chave[ilocalizar+1:]               
                                               ilocalizar1 = atributos.find('#')
                                               atributos   = atributos[:ilocalizar1]
                        
                                               ilocalizar1 = chave.find('#')
                                               tipo_campo  = chave[ilocalizar1+1:]
                                               ilocalizar4 = tipo_campo.find('|')
                                               tipo_campo  = tipo_campo[:ilocalizar4]
                                            
                                               ilocalizar2  = chave.find('_')
                                               nomecampo    = chave[:ilocalizar2]     
                                            
                                               ajuda = ''
                                            
                                               ilocalizar3 = chave.find('|')
                                               obrigatorio = chave[ilocalizar3+1:]  
                                               obrigatorio = obrigatorio.strip()                 
                                                                    
                                               dados_chaves_json = []
                                               listadados = []
                                               montagemjson_lista =''
                                               dados_chaves_json = []
                                               itenscadastro = ''    
                                        
                                               dados_chaves_json = st.session_state["chaves_json"]
                                               print('Chave Json ..: '+str(st.session_state["chaves_json"]))
                                                                                        
                                               if isinstance(dados_chaves_json, list):
                                                  for item in dados_chaves_json:
                                                      if isinstance(item, dict):
                                                         for itenschave, valor_chave in item.items():
                                                             if valor_chave == nomecampo:                                                   
                                                                valores = item.get('Valores', [])
                                                                valores1 = ''
                                                                for valor1 in valores:
                                                                    valores1 = valores1 +valor1+'#'
                                                                montagemjson_lista = montagemjson_lista + valores1  
                                                                                                    
                                               listadados = []
                                               montagemjson_lista =''
                                               itenscadastro = ''                                            
                            
                                               if str(obrigatorio) == 'True':                                                                                  
                                            
                                                  if inclusaoatributos != '':
                                                     inclusaoatributos = inclusaoatributos + ',{'+'\n\r'
                                                  else:
                                                     inclusaoatributos = inclusaoatributos + '{'+'\n\r'
                                            
                                                  inclusaoatributos = inclusaoatributos + '"atributo":' +'"' + atributos +'"' + ','+'\n\r'
                                            
                                                  valor_portal =str(valor)
                                                                               
                                                  iposicao = valor_portal.find('-')
                                                  if iposicao >= 0:
                                                     valor_portal = valor[:iposicao]
                                                                                                    
                                                  if tipo_campo == 'BOOLEANO':
                                                     if valor == 'SIM':
                                                         valor_portal = "true"
                                                     elif valor == 'NAO':
                                                         valor_portal = "false"
                                            
                                                  inclusaoatributos = inclusaoatributos + '"valor":' + '"' + str(valor_portal) +'"' + '\n\r'
                                                  inclusaoatributos = inclusaoatributos + '}' + '\n\r'                                                                      
                                                
                                               #inclusao_ncm = """
                                               #                 insert into catalogo.dbo.detalhes_classificacao(idclassificacao,atributo,chave,valor,tipo,historico,obrigatorio,ajuda) values ('{}','{}','{}','{}','{}','{}','{}','{}')
                                               #               """.format(idclassificacao,atributos,nomecampo,valor,tipo_campo,montagemjson_lista,obrigatorio,ajuda)
                                            
                                                  #print(inclusao_ncm)
                                                  #print(montagemjson_lista)
                                                
                                               montagemjson_lista = ''
                                             #  bdados = conectar()
                                             #  bdados.execute(inclusao_ncm)
                                              # bdados.commit()
                                             #  bdados.close()                                          
                                                
                                    resultado = autotenticar() 

                                    for header, value in resultado.items():
                                        if 'set-token' in header:
                                            set_token = value
                                        if 'x-csrf-token' in header:
                                            x_csrf_token = value
                                                                                
                                    url = "https://val.portalunico.siscomex.gov.br/catp/api/ext/produto?modalidade={}".format(situacaomodalidade)
                                    cnpj1 = st.session_state["cnpjlista"]    
                                    cnpj = cnpj1[:10]
                                    cnpj = cnpj.replace('.','')                                                     
                                    ncm  = ncm_classificado
                                    ncm  = ncm.replace('.','')
                                    ncm  = ncm[:8]
                                                
                                    enviarportal = "["+'\n\r'
                                    enviarportal = enviarportal+"{"+'\n\r'
                                    enviarportal = enviarportal+'"seq"'+': 1,'+'\n\r'
                                    
                                    descricao_mac_string = st.session_state["descricao_mac"]
                                    
                                    descricao_mac_string = descricao_mac_string.replace('\r', '')
                                    
                                    descricao_mac_string = re.sub(r'[\x00-\x1F\x7F]', '', descricao_mac_string)
                                    
                                    enviarportal = enviarportal+'"descricao"'+':'  + '"'+ descricao_mac_string +'"' + ","+'\n\r'

                                    descricao_mac = st.session_state["descricao_ncm"]
                                    descricao_mac = descricao_mac[:100]
                                    enviarportal = enviarportal+'"denominacao"'+':'+ '"'+descricao_mac +'"' + ","+'\n\r'
                                    enviarportal = enviarportal+'"cpfCnpjRaiz"'+':'+ '"'+cnpj +'"'+","+'\n\r'
                                    enviarportal = enviarportal+'"situacao"'+':'+ '"'+listasituacao +'"'+ ","+'\n\r'
                                    enviarportal = enviarportal+'"modalidade"'+':'+ '"'+situacaomodalidade +'"'+","+'\n\r'
                                    enviarportal = enviarportal+'"ncm"'+':'+ '"'+ncm +'",'+""+'\n\r'
                                    enviarportal = enviarportal+'"atributos"'+':'+ '['+'\n\r'
                                    enviarportal = enviarportal+ inclusaoatributos+'\n\r'
                                    enviarportal = enviarportal+"],"+'\n\r'
                                    enviarportal = enviarportal+'"atributosMultivalorados"'+':'+" ["+'\n\r'
                                    enviarportal = enviarportal+"{"+'\n\r'
                                    enviarportal = enviarportal+'"valores"'+':'+'['+'\n\r'
                                    enviarportal = enviarportal+'""'+'\n\r'
                                    enviarportal = enviarportal+"],"+'\n\r'
                                    enviarportal = enviarportal+'"atributo"'+':'+'""'+'\n\r' 
                                    enviarportal = enviarportal+"}"+'\n\r'
                                    enviarportal = enviarportal+"],"+'\n\r'
                                    enviarportal = enviarportal+'"atributosCompostos"'+':'+" [],"+'\n\r'
                                    enviarportal = enviarportal+'"atributosCompostosMultivalorados"'+':'+" [],"+'\n\r'
                                    enviarportal = enviarportal+'"codigosInterno"'+':'+" ["+'\n\r'
                                    enviarportal = enviarportal+codigoproduto+'\n\r'
                                    enviarportal = enviarportal+"],"+'\n\r'
                                    enviarportal = enviarportal+'"dataReferencia"'+':'+ '"' + datetime.today().strftime('%Y-%m-%d')+'"' +'\n\r'
                                    enviarportal = enviarportal+"}"+'\n\r'
                                    enviarportal = enviarportal+"]"+'\n\r'
                                                    
                                    print(enviarportal)
                                        
                                    payload1 = enviarportal
                                                                                                    
                                    headers = {
                                                        'Authorization': set_token,
                                                        'X-CSRF-Token': x_csrf_token,
                                                        'Content-Type': 'application/json'
                                               }                       
                                                
                                    response = requests.request("POST", url, headers=headers, data=payload1)
                                                                                                        
                                    if response.status_code == 200:
                                       resultado = response.json()
                                       if resultado[0]['sucesso'] == True:
                                          codigo_portal = resultado[0]['codigo']
                                          url = "https://val.portalunico.siscomex.gov.br/catp/api/ext/fabricante"                      
                                          payload = json.dumps([
                                                                    {
                                                                    "seq": 1,
                                                                    "cpfCnpjRaiz": cnpj,
                                                                    "codigoOperadorEstrangeiro": "BR07358761000169",
                                                                    "cpfCnpjFabricante": "07358761000169",
                                                                    "conhecido": False,
                                                                    "codigoProduto": codigo_portal,
                                                                    "vincular": True,
                                                                    "dataReferencia": datetime.today().strftime('%Y-%m-%d'),
                                                                    "codigoPais": "AA"
                                                                    }
                                                                    ]
                                                                )
                                          headers = {
                                                                'Authorization': set_token,
                                                                'X-CSRF-Token': x_csrf_token,
                                                                'Content-Type': 'application/json'
                                                    }                       
                                                    
                                          response = requests.request("POST", url, headers=headers, data=payload)
                                                    
                                          if response.status_code == 200:
                                            try:
                                                resultado = response.json()
                                                codigo_portal = resultado[0]['codigo']
                                                if resultado[0]['sucesso'] == True:
                                                    st.success('Produto Cadastrado com Sucesso - Codigo Produto = {}'.format(codigo_portal))   
                                                    inclusao = """
                                                                    update catalogo.dbo.classificacao set status = 4,situacao = 2,codigo_portal = '{}',data_classificacao = '{}',codigo_produto = case when codigo_produto = '' then '{}' end 
                                                                    where id = '{}'
                                                                """.format(codigo_portal,datetime.today().strftime('%Y-%m-%d'),codigo_portal,idclassificacao)
                                                    print(inclusao)
                                                    bdados = conectar()
                                                    bdados.execute(inclusao)
                                                    bdados.commit()
                                                    bdados.close() 
                                                else:
                                                    json_bytes = resultado[0]['erros']
                                                    json_str  = json_bytes.decode('utf-8')
                                                    dados = json.loads(json_str)

                                                    for item in dados:
                                                        leitura = f"Seq: {item.get('seq')}"
                                                        leitura = leitura + f"Código: {item.get('codigo')}"
                                                        leitura = leitura +f"Erros: {item.get('erros')}"
                                                        leitura = leitura +f"Sucesso: {item.get('sucesso')}"
                                                        leitura = leitura +f"Versão: {item.get('versao')}"
                                                        
                                                    st.error(st.error('Produto não Incluido , Erros :'+leitura  ))  
                                            except requests.exceptions.HTTPError as errh:
                                                st.subheader("Alerta Sistema", divider=True)
                                                st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(errh))
                                            except requests.exceptions.ConnectionError as errc:
                                                print ("Error Connecting:",errc)
                                            except json.JSONDecodeError as errh:
                                                st.subheader("Alerta Sistema", divider=True)
                                                st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(errh))
                                            except requests.exceptions.Timeout as errt:
                                                st.subheader("Alerta Sistema", divider=True)
                                                st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(errt))
                                            except requests.exceptions.RequestException as a:
                                                st.subheader("Alerta Sistema", divider=True)
                                                st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos"+str(a))
                                          else:
                                                st.subheader("Alerta Sistema", divider=True)
                                                st.error(st.error('Produto não Incluido , Erros :'+ response.json()))  
                                            
                                       else:
                                         st.subheader("Alerta Sistema", divider=True)
                                         st.error(response.json())    
                                    else:
                                      st.subheader("Alerta Sistema", divider=True)
                                      st.warning("Não Esta sendo Possivel , Consultar o Site do Serpro ! , Por favor tente em alguns minutos , "+str(response.status_code)+str(response.text))
           
                            if st.session_state['FormSubmitter:Painel_Classificacao-Incluir / Alterar'] == False:
                                   consulta =  """
                                            select * from catalogo.dbo.detalhes_classificacao where idclassificacao = '{}' 
                                            """.format(idclassificacao)
                                   dados = pd.read_sql(consulta,conexao)
                
                                   if dados.empty:
                                      if ( ncm_classificado != '') and len(ncm_classificado[:10].replace('.','')) == 8:
                                         idvalor = 1 
                                         atributos = consultar_atributos_ncm(ncm_classificado[:10].replace('.',''),situacaomodalidade,idvalor)
                                         st.session_state['chaves_json'] = atributos
                                   else:
                                       idvalor = 2 
                                       atributos = consultar_atributos_ncm_cadastrado(idclassificacao)
                                       st.session_state['chaves_json'] = atributos   
                                   
                                   print('Agora .........'+str(st.session_state))
                                                        
                            elif pesquisar_ncm:
                                   idvalor = 1 
                                   st.session_state['chaves_json'] = ''
                                   #print(ncm_classificado[:10].replace('.',''))
                                   atributos = consultar_atributos_ncm(ncm_classificado[:10].replace('.',''),situacaomodalidade,idvalor)                        
                                   st.session_state['chaves_json'] = atributos                                      
                  
                      with tab2:
                           if tab2:
                              if selected_rows is not None:
                                 idclassificacao = selected_rows['id'].values[0]
                                 st.subheader('Historico Chamados', divider = 'blue')    
                                 coluna6_1, coluna6_2,coluna6_3,coluna6_4,coluna6_5,coluna6_6,coluna6_7,coluna6_8 = st.columns(8)
                                 colunas6_1, colunas6_2,colunas6_3,colunas6_4,colunas6_5,colunas6_6,colunas6_7,colunas6_8 = st.columns([0.25,0.20,0.20,0.20,0.20,0.20,0.20,0.20])
                                 coluna4_1,coluna4_2,coluna4_3,coluna4_4,coluna4_5,coluna4_6,coluna4_7,coluna4_8= st.columns([0.20,0.20,0.20,0.20,0.20,0.20,0.20,0.20])
                                 
                                 if selected_rows['nrochamado'].values[0] is None :
                                    nrochamado = '00000'
                                 else:
                                    nrochamado = selected_rows['nrochamado'].values[0]
                                       
                                 if nrochamado != '00000':
                                    data_for_df = []
                                    url = "https://prod-20.brazilsouth.logic.azure.com:443/workflows/dd6ebf59dead4cf48bfa1499b243dcda/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=_Al596hGW6nWhKXcmvoLRx1S3x4Zcm-BpvsnvSSDid8"
                                    payload = json.dumps({
                                                             "IDHash": selected_rows['nrochamado'].values[0]
                                                         })      
                                    headers = {
                                                   'Content-Type': 'application/json'
                                                 }

                                    response = requests.request("POST", url, headers=headers, data=payload)
                                    response.raise_for_status()
                                    
                                    data = response.json()                                            
                                    if response.status_code == 200 and response.text:       
                                       if 'atividade do' not in data: 
                                           for item in data:
                                               data_for_df.append({
                                                                   "ItemInternalId": item.get("ItemInternalId"),
                                                                    "ID": item.get("ID"),
                                                                    "Title": item.get("Title"),
                                                                    "Created": item.get("Created"),
                                                                    "Author": item["Author"]["DisplayName"],
                                                                    "Resposta": item.get("Resposta"),
                                                                     "Modified": item.get("Modified")
                                                                  })
                                             
                                       df = pd.DataFrame(data_for_df)
                                       col1_1, col1_2, col1_3, col1_4 ,col1_5 = st.columns([0.10,0.25,0.40,0.70,0.30])
                                       with col1_1:
                                          st.write("**Item**")
                                       with col1_2:
                                          st.write("**Data**")
                                       with col1_3:
                                          st.write("**Autor**")
                                       with col1_4:
                                          st.markdown("**Resposta**")
                                       with col1_5:
                                          st.markdown("")  # Coluna vazia
                                           
                                       for i, row in df.iterrows():
                                           spacer_1_2, spacer_2_1, spacer_3_1, spacer_4_1, spacer_5_1 = st.columns([0.10,0.25,0.40,0.70,0.30] )
                                           with spacer_1_2:
                                             st.write(row['ID'])
                                           with spacer_2_1:
                                             st.write(row['Created'])
                                           with spacer_3_1:
                                             st.write(row['Author'])
                                           with spacer_4_1:
                                             if row['Resposta'] is not None:
                                                st.write(row['Resposta'])
                                           with spacer_5_1:
                                             responder_chamados = st.button(f"Responder Chamado: {row['ID']}", key=row['ID'])                                   
                                    
                                   
                                    with colunas6_1:
                                      st.markdown('</div>', unsafe_allow_html=True)
                                      st.markdown('<div class="button-aligned-resposta">', unsafe_allow_html=True)
                                      enviar_chamados = st.button('Enviar Resposta-Chamado',type='primary',use_container_width=False,icon=":material/web:") 
                                      st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    
                                 
                                    if responder_chamados:
                                               with st.form('Resposta de Chamados'):
                                                    st.subheader('Resposta Chamados',divider='blue')
                                                    coluna1,coluna2,coluna3= st.columns([0.50,0.90,0.90])
                                                    coluna1_1,coluna1_2,coluna1_3,coluna1_4,coluna1_5,coluna1_6 = st.columns([0.50,0.90,0.90,0.50,0.50,0.50])
                                                    coluna3_1,coluna3_2 = st.columns([0.50,0.90])
                                                    coluna2_1,coluna2_2 = st.columns([1,0.01])
                                                    emails = lista_emails()
                                       
                                                    with coluna1:
                                                      usuariocriador = st.text_input("**Item Chamado**",key = "itemchamado")                                 
                                                    with coluna2:
                                                      usuariocriador = st.selectbox("**Usuario Chamado (email)**", options=emails,key = "usuariocriador1")
                                                    with coluna3:
                                                      usuarioresponsavel = st.selectbox("**Usuario Responsavel**", options=emails,key = "usuarioresponsavel1")
                                               with coluna2_1:
                                                 mensagem = st.text_area("**Mensagem**", value='',key="mensagem_chamado")
                                                 responders_chamados = st.form_submit_button('',disabled=True) 
                                 
                                    if enviar_chamados:
                                       mensagem = st.session_state["mensagem_chamado"]
                                 
                                       url = 'https://prod-31.brazilsouth.logic.azure.com:443/workflows/e38694cb5d0a48deb7be44bb0099332e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xLipNJEe5xW8li_BGfQX32NJkoDRHmBOhOGVpUhXbmc'
                                                    
                                       headers = {
                                                  'Content-Type': 'application/json'
                                                 }
                                                   
                                       payload_data =  {   "IDHash": selected_rows['nrochamado'].values[0],   "Resposta": mensagem }
                                                    
                                       payload = json.dumps(payload_data, indent=4)
                                                    
                                       print(payload)
                                       resposta = requests.post(url, headers = headers, data=payload)
                                       if resposta.status_code == 200:
                                          resultado = resposta.content
                                          st.success('Resposta Enviada com Sucesso')       
                                       else:
                                          resultado = resposta
                                          st.error(resultado)
             
                                 else:

                                   with coluna6_1:
                                        st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                        chamados = st.button('Abrir Chamado',type='primary',use_container_width=True,icon=":material/web:") 
                                        st.markdown('</div>', unsafe_allow_html=True)
 
                                 if nrochamado == '00000':
                                    if chamados:      
                                       with st.form('Abertura_Chamados'):
                                            aberturas_chamados = st.form_submit_button('')  
                                            st.session_state['FormSubmitter:Abertura_Chamados'] = True
                                            st.subheader('Abertura de Chamados',divider='blue')                                            
                                            coluna1,coluna2,coluna3= st.columns([0.50,0.90,0.90])
                                            coluna2_1,coluna2_2 = st.columns([1,0.01])                                            
                                            coluna1_1,coluna1_2,coluna1_3,coluna1_4,coluna1_5,coluna1_6 = st.columns([0.50,0.90,0.90,0.50,0.50,0.50])
                                            coluna3_1,coluna3_2 = st.columns([0.90,0.01])
                                            emails = lista_emails()
                                     
                                            with coluna1:
                                              usuariocriador = st.text_input("**Item Chamado**",key = "itemchamado")                                 
                                            with coluna2:
                                              usuariocriador = st.selectbox("**Usuario Chamado (email)**", options=emails,key = "usuariocriador1")
                                            with coluna3:
                                              usuarioresponsavel = st.selectbox("**Usuario Responsavel**", options=emails,key = "usuarioresponsavel1")
                                        
                                            mensagem  = st.text_area("**Mensagem**",key="mensagem_chamado")                                                                                    
                                    with colunas6_1:
                                        st.markdown('</div>', unsafe_allow_html=True)
                                        st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                        abertura_chamado = st.button('Enviar Mensagem-Abertura',type='primary',use_container_width=False,icon=":material/web:",key="botao_abertura_chamado") 
                                        st.markdown('</div>', unsafe_allow_html=True)                                      
                                 
                                 
                                 if nrochamado == '00000':
                                    if abertura_chamado:      
                                       #st.session_state.Abertura_Chamados = True
                                       usuariocriador = st.session_state["usuariocriador1"]
                                       
                                       iposicao = usuariocriador.find('(')
                                       if iposicao >= 0:
                                          usuariocriador = usuariocriador[iposicao+1:]
                                          iposicao = usuariocriador.find(')')
                                          usuariocriador = usuariocriador[:iposicao]                                            
                               
                                       usuarioresponsavel = st.session_state["usuarioresponsavel1"]
                                       iposicao = usuarioresponsavel.find('(')
             
                                       if iposicao >= 0:
                                          usuarioresponsavel = usuarioresponsavel[iposicao+1:]
                                          iposicao = usuarioresponsavel.find(')')
                                          usuarioresponsavel = usuarioresponsavel[:iposicao] 
                                             
                                       mensagem_chamado = st.session_state["mensagem_chamado"]
                                    
                                       if usuariocriador and usuarioresponsavel:
                                          datanecessidade = selected_rows['Dtnecessidade'].values[0]
                                          datanecessidade = datanecessidade[:10]
                                          url = "https://prod-26.brazilsouth.logic.azure.com:443/workflows/1643e16be37148d18def445468b3348e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=ScHBEpl2HxgEtykbBb7NvkyUEHrsFY2xssnP5WQor30"
                                                    
                                          payload_data = {
                                                        "IDPedidoItem": f"{selected_rows['Pedido'].values[0]}-{selected_rows['Item'].values[0]}",
                                                        "DataNecessidadeUsina": datanecessidade,
                                                        "NI": codigoproduto,
                                                        "NCMCliente": ncm_produto,
                                                        "NCMMAC": ncm_classificado,
                                                        "Usina": "Usina Central",
                                                        "DescricaoItem": descricao_Mac,
                                                                        "DescricaoChamado": mensagem_chamado,
                                                                        "UsuarioCriador": {
                                                                                            "Email": usuariocriador
                                                                                        },
                                                                        "UsuarioResponsavel": {
                                                                                            "Email": usuarioresponsavel
                                                                                            },
                                                                        "UsuarioChamado": {
                                                                                            "Email": usuariocriador
                                                                                        },
                                                                        "Situacao": "Pendente",
                                                                        "Prioridade": "Alta"
                                                                    }
                                                        
                                          payload = json.dumps(payload_data, indent=4)
                                          headers = {
                                                       'Content-Type': 'application/json'
                                                      }
                                          print(payload)
                                          resposta = requests.post(url, headers = headers, data=payload)
                                                    
                                          if resposta.status_code == 200:
                                             resultado = resposta.headers['IDHash']
                                             atualizar = "update catalogo.dbo.classificacao set nrochamado = '{}',situacao = 1,status = 1  where id = '{}'".format(resultado,selected_rows['id'].values[0])
                                             bdados = conectar()
                                             bdados.execute(atualizar)
                                             bdados.commit()
                                             st.success('Chamado Aberto com Sucessso - Nro '+resultado)       
                                          else:
                                             resultado = resposta
                                             st.error(resultado)
                                 
                                              
          if choice == 'Operador Estrangeiro':
                       st.markdown(card_style, unsafe_allow_html=True)
                       st.markdown(f"""
                                <div class="card_titulo">
                                <h4><b>Operador Estrangeiro</h4></b>
                                </div>
                                """, 
                                unsafe_allow_html=True)

                      
                       st.subheader('**Dados**',divider="red")
            
                       coluna1,coluna2,coluna3 = st.columns([0.50,0.50,0.50])   
                       with st.form(key='Operador Estrangeiro'):        
                            with coluna1:
                                 lista_clientes = listaclientes()
                                 cliente = st.selectbox("**Cliente**",options = lista_clientes)
                            with coluna2:
                                 cnpj = st.text_input("**Codigo Operador**", value=st.session_state.cnpj_raiz)
                            with coluna3:
                                 st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                                 pesquisar_cnpj = st.button('Consultar',type='primary')
                                 st.markdown('</div>', unsafe_allow_html=True)
                
                                 nome = ''
                                 situacao = ''
                                 endereco = ''
                                 bairro = ''
                                 cidade = ''
                                 cep = ''
                                 codigointerno = ''
                                 email = ''
                                 listapaises = ''
                                 st.session_state.botao = True

                            if pesquisar_cnpj:
                               consulta = f"""
                                         SELECT CASE WHEN situacao_portal = 1 then 'ATIVADO' else null END as Situacao,exportador, 
                                        endereco + ',' + isnull(bairro,'') + ',' + isnull(cidade,'') + ',' as Endereco,cidade,
                                        codigo_tin,
                                        codigo_cliente,
                                        email,
                                        cep,
                                        data_cadastro,
                                        codigo_portal,
                                        cnpj_portal,
                                        subdivisao,
                                        cliente
                                        FROM catalogo.dbo.exportadores 
                                        WHERE codigo_cliente = '{cnpj}'
                                        """
                          
                               st.session_state.botao = False
                               bddados = conectar()
                               bddados.execute(consulta)
                               resultado = bddados.fetchone()

                               paises = lista_paises()
                               st.session_state.listapaises = paises                           
                              
                               #listasubdivisao = lista_subdivisao('AR')
                               #print(listasubdivisao)
                        
                               if resultado is not None:
                                
                                  st.session_state.situacao,st.session_state.nome,st.session_state.endereco,st.session_state.cidade,st.session_state.codigotin,st.session_state.codigointerno,st.session_state.email,st.session_state.cep,st.session_state.data_cadastro,st.session_state.codigo_portal,st.session_cnpj_portal,st.session_subdivisao,st.session_state.codigo_cliente = resultado[0],resultado[1],resultado[2],resultado[3],resultado[4],resultado[5],resultado[6],resultado[7],resultado[8],resultado[9],resultado[10],resultado[11],resultado[12]
                                                                                        
                               else:
                                 st.warning('Operador não encontrado.')
                                 st.session_state.situacao, st.session_state.nome ,st.session_state.endereco, st.session_state.codigotin, st.session_state.codigointerno, st.session_state.email, st.session_state.cep, st.session_state.cidade,st.session_state.bairro,st.session_state.data_cadastro,st.session_state.codigo_portal,st.session_cnpj_portal,st.session_subdivisao,st.session_state.codigo_cliente  = 'Nao Ativado', '', '', '', '', '', '', '','','',''
                        
                               bddados.close()
                        
                               # Formulário de informações
                               colunas1_1, colunas1_2, colunas1_3, colunas1_4, colunas1_5,colunas1_6,colunas1_7 = st.columns([0.12,0.10,0.10,0.25,0.10,0.20,0.20])
                               colunas2_1, colunas2_2 = st.columns(2)
                               colunas3_1, colunas3_2, colunas3_3, colunas3_4,colunas3_5 = st.columns([0.25,0.65,0.90,0.90,0.70])

                               with colunas1_1:         
                                   st.text_input('**Data Cadastro:**',value=st.session_state.data_cadastro)                            
                               with colunas1_2:         
                                   st.text_input('**Código Portal:**',key="codigo_portal",value=st.session_state.codigo_portal)                            
                               with colunas1_3:         
                                   st.text_input('**Situação:**', key="situacao",value=st.session_state.situacao)                            
                               with colunas1_4:         
                                   cliente = st.text_input('**Cliente:**',key = "cliente",value =cliente )             
                               with colunas1_5:         
                                   codigo_interno = st.text_input('**Codigo Interno:**',key="codigo_interno", value=st.session_state.codigointerno)             
                               with colunas1_6:
                                    paises = lista_paises()
                                    st.session_state.listapaises = paises   
                                    listapais = st.selectbox('**Pais do Operador:**',key="lista_pais", options=st.session_state.listapaises) 
                               with colunas1_7:         
                                    codigotin = st.text_input('**No de identificação(TIN):**'+' *',key = "codigo_tin", value=st.session_state.codigotin)             
                               with colunas2_1:         
                                    exportador = st.text_area('**Nome:**',key = "exportador", value=st.session_state.nome)             
                               with colunas2_2:         
                                    endereco1 = st.text_area('**Endereço:**'+' *', key = "endereco",value=st.session_state.endereco)             
                               with colunas3_1:         
                                   cep = st.text_input('**Cep:**',key = "cep", value=st.session_state.cep)             
                               with colunas3_2:         
                                   cidade = st.text_input('**Cidade:**',key="cidade", value=st.session_state.cidade)             
                               with colunas3_3:         
                                    lista_subdivisao = ['AR-A', 'AR-B'] 
                                    st.session_state.lista_subdivisao = lista_subdivisao
                                    subdivisao = st.selectbox('**Subdivisão(Estado,Provincia):**'+' *',key = "subdivisao",options=st.session_state.lista_subdivisao)             
                               with colunas3_4:         
                                    email = st.text_input('**Email:**'+' *', value=st.session_state.email)             
                               with colunas3_5:     
                                    lista_clientes = lista_clientes_raiz(cliente) 
                                    itens = '\n'.join(lista_clientes)   
                                    lista_cnpj_cliente = st.text_area('**CPF/CNPJ:**',value = itens,key ="lista_cnpj_cliente" ) 
                                    
                            botao = st.form_submit_button(label='Incluir/Retificar',type='primary',disabled=st.session_state.botao)
                        
                            if botao:
                               lista_itens = st.session_state["lista_cnpj_cliente"].splitlines()
                               subdivisao  = st.session_state.subdivisao
                               pais        = st.session_state.lista_pais[:2]
                            
                               instrucao = """
                                             select id from catalogo.dbo.clientes  where nome ='{}'
                                           """.format(cliente)
                          
                               bdados3 = conectar()
                               bdados3.execute(instrucao)
                               idclientes = bdados3.fetchone()
                               bdados3.close()

                               instrucao = """
                                              delete from catalogo.dbo.exportadores  where codigo_cliente ='{}'
                                              and data_cadastro is not null and cliente = {}
                                           """.format(st.session_state.codigointerno,st.session_state.codigo_cliente)
                               
                               print(instrucao)
                               bdados3 = conectar()
                               bdados3.execute(instrucao)
                               bdados3.commit()
                          
                               for itens in lista_itens:                             
                                   cnpj_raiz_1= itens.replace('.','')                              
                              
                                   if st.session_state.codigo_tin == None:
                                      codigo_tid = ''
                                   else:
                                      codigo_tid = st.session_state.codigo_tin 
                              
                                   if st.session_state.email == None:
                                      email = ''
                                
                                 
                                   resultado = autotenticar()
                              
                                   for header, value in resultado.items():
                                       if 'set-token' in header:
                                           set_token = value
                                       if 'x-csrf-token' in header:
                                           x_csrf_token = value                            
                                    
                                   url = "https://val.portalunico.siscomex.gov.br/catp/api/ext/operador-estrangeiro"
                            
                                   payload = json.dumps([{
                                                   "seq": 1,
                                                   "cpfCnpjRaiz": cnpj_raiz_1,
                                                   "tin": codigo_tid,
                                                   "nome": st.session_state.nome,
                                                   "situacao": 'ATIVADO',
                                                   "logradouro": st.session_state.endereco[:70],
                                                   "nomeCidade": st.session_state.cidade,
                                                   "codigoPais": pais, 
                                                   "codigoSubdivisaoPais": subdivisao,
                                                   "cep": st.session_state.cep,
                                                   "codigoInterno": st.session_state.codigointerno,
                                                   "email": email,
                                                   "dataReferencia": datetime.today().strftime('%Y-%m-%d')
                                                }])      
                                   print(payload) 
                              
                                   headers = {
                                               'Authorization':set_token,
                                               'X-CSRF-Token':x_csrf_token,
                                               'Content-Type': 'application/json'
                                             }
                                    
                                   response = requests.request("POST", url, headers=headers, data=payload)
                        
                                   if response.status_code == 200:
                                      resultado = response.json()
                                      codigo_portal = resultado[0]['codigo']
                                      print(resultado)
                                      if resultado[0]['sucesso'] == True:
                                         instrucao = """
                                                        insert into catalogo.dbo.exportadores(data_cadastro,cliente,codigo_cliente,endereco,cidade,cep,pais,
                                                        email,usuario,exportador,subdivisao,cnpj_portal,situacao_portal,codigo_tin,codigo_portal,versao)
                                                        values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                                     """.format(datetime.today().strftime('%Y-%m-%d'),1,st.session_state.codigointerno,st.session_state.endereco,st.session_state.cidade,st.session_state.cep,'AR',email,'AUT',st.session_state.nome,'AR-B',itens,1,codigo_tid,resultado[0]['codigo'],resultado[0]['versao'])
                                         print(instrucao)       
                                         bdados3 = conectar()
                                         bdados3.execute(instrucao)
                                         bdados3.commit()
                                         st.success('Operador Estrangeiro Cadastrado com Sucesso .. CNPJ_Raiz : '+ cnpj_raiz_1)

                                      else:
                                        st.error(resultado[0]['erros'])
                                   else:
                                     st.error(response.content)                
      
          if choice == "Cadastro NCM":
             st.markdown(card_style, unsafe_allow_html=True)
             st.markdown(f"""
                            <div class="card_titulo">
                            <h4><b>Cadastro NCM</h4></b>
                            </div>
                            """, 
                            unsafe_allow_html=True)
             st.subheader("Filtros", divider="red")
             coluna1,coluna2,coluna3 = st.columns([0.10,0.50,0.10])  
             with coluna1:
                  codigo_produto = st.text_input("**Codigo Produto:**")
             with coluna2:
                  Descricao_Tecnica = st.text_input("**Descricao Técnica:**")
             with coluna3:
                  st.markdown('<div class="button-aligned">', unsafe_allow_html=True)
                  pesquisar = st.button('Consultar',use_container_width=True,type='primary',icon=":material/search:") 
                  st.markdown('</div>', unsafe_allow_html=True)   
             
             st.subheader("Resultado", divider="red")
     
             if pesquisar:
                consulta = """
                                select  a.data_cadastro,
                                        c.nome as Cliente,
                                        a.pedido as Pedido,
                                        a.item as Item,
                                        a.codigo_produto as Codigo,
                                        a.ncm_mac as NCM,
                                        a.descricao_tecnica as Descricao_Tecnica
                                        from catalogo.dbo.classificacao a
                                        left join  catalogo.dbo.clientes c on c.id = a.cliente
                                        where a.descricao_tecnica like '%{}%' and data_cadastro is not null 
                                        order by a.data_cadastro desc
                            """.format(Descricao_Tecnica)
                
                df = pd.read_sql(consulta,conexao)
  
                st.session_state["df"] = df

                #st.dataframe(st.session_state["df"], key="data",on_select="rerun",use_container_width=True)
                
                df1 = pd.DataFrame(df)

                col1_1, col1_2, col1_3, col1_4 ,col1_5,col1_6,col1_7,col1_8 = st.columns([0.25,0.25,0.15,0.20,0.25,0.50,0.50,0.90])
                with col1_1:
                     st.markdown("**Data Cadastro**")
                with col1_2:
                     st.markdown("**Cliente**")
                with col1_3:
                     st.markdown("**Pedido**")
                with col1_4:
                     st.markdown("**Item**")
                with col1_5:
                     st.markdown("**NCM**")
                with col1_6:
                     st.markdown("**Codigo**")
                with col1_7:
                     st.markdown("**Descricao_Tecnica**")
                with col1_8:
                     st.markdown("")
                                                                                    
                for i, row in df.iterrows():
                    col1, col2, col3, col4 ,col5,col6,col7,col8 = st.columns([0.25,0.25,0.15,0.20,0.25,0.50,0.50,0.50])  # Definindo 4 colunas
                    with col1:
                         st.write(row['data_cadastro'])
                    with col2:
                         st.write(row['Cliente'])
                    with col3:
                         st.write(row['Pedido'])
                    with col4:
                         st.write(row['Item'])
                    with col5:
                         st.write(row['NCM'])
                    with col6:
                         st.write(row['Codigo'])
                    with col7:
                         st.write(row['Descricao_Tecnica'])
                    with col8:
                         pdf_tecnico = st.button(f"Visualizar: {row['NCM']+"-"+str(row['Codigo'])}", key=str(row['Pedido'])+str(row['Item']),on_click=criar_pdf_tecnico)  
                    
                        
                
          if choice == "Importar Arquivo":
             st.markdown(card_style, unsafe_allow_html=True)
             st.markdown(f"""
                            <div class="card_titulo">
                            <h4><b>Importar Arquivo</h4></b>
                            </div>
                            """, 
                            unsafe_allow_html=True)
             st.subheader('**Localizar Arquivo**',divider="red")
             uploaded_file = st.file_uploader('**Arquivo**')
             if uploaded_file is not None:
                dataframe = pd.read_excel(uploaded_file,index_col=0)
                st.dataframe(dataframe)
               
                st.subheader('',divider="red")
                
                coluna1,coluna2 = st.columns([0.95,0.25])

                total_linhas = dataframe.shape[0]
                with coluna1:
                     st.markdown("<h3 style='font-size:20px;'>Total de linhas: "+str(total_linhas-1)+"</h3>", unsafe_allow_html=True)
                with coluna2:
                     st.button('Importar Arquivo')
        
          if choice == "Sair":
             st.session_state.logged_in = False
             login()
    else:
       login()
         
def main():
    if st.session_state.logged_in:
        main_content()
    else:
        login() 

if __name__ == '__main__':
   main()

