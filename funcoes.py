import pyodbc 

def conectar():
 server   = '172.36.174.15'
 database = 'mantra_mac'
 username = 'softcargo'
 password = 'Sist*sql!@'
 conexao  = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
 conexao1 = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
 cursor = conexao.cursor()
 return  cursor
