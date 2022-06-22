import pymysql
from Entrada import *
#Criar conexão
conexao = pymysql.connect(host='localhost',port=3306,database='gerenciador_senhas',
                          user='root',password='root@123',autocommit=True)
#cursor
cursor = conexao.cursor()

def criar_senha(descricao, password_user):
    comando = ("INSERT INTO table_user (description, password) values (%s, %s)")  # INSERIR NA TABELA A PLATAFORMA E SUA SENHA
    val = (descricao, password_user)  # criada tupla, para inserir dados na coluna
    cursor.execute(comando, val)  # execução

def select():
    consulta = ("select * from table_user")  # selecionar a tabela, para poder visualiza-la
    cursor.execute(consulta)
    linhas = cursor.fetchall()  # contar quantas linhas existem nas colunas
    return linhas

def quantidade():
    contador_linhas = 0
    for quantidade_linhas in select():
        contador_linhas += 1
    return contador_linhas

def deletar(linha2,linhas,plataforma_desejada):
    for linha2 in linhas:
        if plataforma_desejada == linha2[2]:  # Comparando, para quando o valor varrido for o desejado pelo usuário
            excluir = ('DELETE FROM table_user WHERE id_description = (%s)')
            valor_excluir = linha2[2]
            cursor.execute(excluir, valor_excluir)

def reset():
    if quantidade() >= 0:
        resetar_id = ('ALTER TABLE table_user AUTO_INCREMENT = 1')  # Resetar o ID, quando não houver mais senhas
        cursor.execute(resetar_id)
