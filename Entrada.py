from Back import *
import pymysql
from selenium import webdriver
#Criar conexão
conexao = pymysql.connect(host='localhost',port=3306,database='gerenciador_senhas',
                          user='root',password='root@123',autocommit=True)
#cursor
while True:
    print('-' + '==-' * 8)
    menu = '''      MENU INICIAL
-==-==-==-==-==-==-==-==-
[1] Adicionar nova senha
[2] Acessar senhas
[3] Deletar senha
[4] Sair'''
    print(f'\033[1m{menu}') #Exibição de opções
    print('-' + '==-' * 8)
    print('\033[;1m')
    c = 0

    escolha = int(input("O que você deseja fazer? "))
    while True:
        if escolha == 1 or escolha == 2 or escolha == 3 or escolha == 4:
            break
        #Caso o usuário tente fugir das possibilidades
            escolha = int(input("Digite uma opção válida: "))
        print()
    #CRIAR NOVA SENHA
    if escolha == 1:
        descricao = str(input("Digite o nome da plataforma: ").upper())
        login_user = str(input("Digite o login da plataforma: "))
        password_user = str(input("Digite a senha: "))

        criar_plataforma(descricao, login_user, password_user)
        print('\n\033[;32mSeu novo cadastro obteve sucesso.\033[;1m\n') #Confirmação de cadastro

    #VISUALIZAR OU EXCLUIR SENHAS JÁ CADASTRADAS
    if escolha ==2 or escolha == 3:
        select()
        if quantidade() < 1: #Se for menor que 1, é porque não possui nenhum registro no banco de dados
            print()
            print("\033[;31mVocê ainda não possui senhas! Volte ao menu para cadastrar!\033[;1m") #CASO NÃO TENHA SENHAS ELE NÃO CONTINUA
            print()
        else:
            print("\nPLATAFORMAS DISPONÍVEIS:\n") #Exibição das possibilidades
            for linha in select():
                print(f"[{linha[3]}]", linha[0])
            print()
            consulta = ("select * from table_user")
            cursor.execute(consulta)
            linhas = cursor.fetchall()
            if escolha == 2:
                plataforma_desejada = int(input("Qual você quer acessar? "))
                for linha2 in select():
                    if plataforma_desejada == linha2[3]: #Comparando, para quando o valor varrido for o desejado pelo usuário, exibir após o if
                        print()
                        print("Plataforma:", linha2[0])
                        print("Login:", linha2[1])
                        print("Senha: *******")
                        #2print("Senha:", linha2[1])
                        print()
                        deseja_acessar = input('Deseja acessar automaticamente à plataforma? [s/n] ').lower()
                        if deseja_acessar == 's': #automação
                            driver = webdriver.Chrome(executable_path=r"C:\Users\jenni\chromedriver\chromedriver")
                            try:
                                driver.get(f'https://www.{linha2[0]}.com.br')
                                campo_login = driver.find_element(By.CSS_SELECTOR, "#email")
                                campo_login.send_keys(linha2[1])

                                campo_password = driver.find_element(By.CSS_SELECTOR, '#pass')
                                campo_password.send_keys(linha2[2] + Keys.RETURN)
                            except:
                                driver.find_element(By.XPATH,'//*[@id="details-button"]').click()
                                driver.find_element(By.XPATH,'//*[@id="proceed-link"]').click()
                                driver.get(f'https://www.{linha2[0]}.com.br')
                                campo_login = driver.find_element(By.CSS_SELECTOR, "#email")
                                campo_login.send_keys(linha2[1])
                                campo_password = driver.find_element(By.CSS_SELECTOR, '#pass')
                                campo_password.send_keys(linha2[2] + Keys.RETURN)
                        else:
                            pass
            else:
                plataforma_desejada = int(input("Qual você quer deletar? "))
                confirmacao = str(input("\033[;31mRealmente deseja deletar o registro? A ação será permanente: [s/n] \033[;1m").lower())
                if confirmacao == "s":
                    for linha2 in select():
                        if plataforma_desejada == linha2[3]: #Comparando, para quando o valor varrido for o desejado pelo usuário
                            deletar(linha2, linhas, plataforma_desejada)
                            print('\n\033[;32mDeletado com sucesso!\033[;1m\n')
                            reset()
    elif escolha == 4:
        print('\n\033[;32mAté breve!') #Encerrar programa
        break
    desejo = str(input("Deseja voltar ao menu inicial? [s/n] ").lower())
    print()

    if desejo == "n":
        print("\033[;32mAté breve!") #Encerrar programa
        conexao.close() #fechar conexão
        break
