from lib.subalgoritmos import *
import os
from time import sleep

itens_cadastro = ['Usuário', 'Especialista']
itens_moderador = ['Deletar conta', 'Visualizar todas as contas (.json)', 'Finalizar programa']
dados_conta = {'Nome': '', 'Email': '', 'Senha': ''}
dados_especialista = {'CPF': '', 'CRM': '', 'Profissão': ''}
dados_json = {}
usuarios_json = {}
especialistas_json = {}
erro_login = False
opc_json = 0
opc_moderador = 0
opc_deletar = 0

while True:
    os.system('cls')
    print(f"""
    {linha(43)}
    || Programa responsável pelo cadastro de ||
    || contas no site Health Nexus.          ||
    || Desenvolvido por: Nexus               ||
    {linha(43)}
    """)
    sleep(3)

    menu('Cadastrar-se como:', itens_cadastro)
    cabecalho('Já possui uma conta?')
    print('3 - Login')
    print(linha(40))
    opc_menu = int(tratar_erro_numero('Escolha uma opção: '))
    match opc_menu:
        case 1:
            # Cadastro usuário
            dados_conta = cadastro_geral('DA CONTA', dados_conta)
            insert_bd('conta', dados_conta)
            insert_bd('usuario', dados_conta)

            # Atualizar dados do cadastro
            dados_conta = confirmar_dados('DA CONTA', dados_conta)
            os.system('cls')
            cabecalho("Cadastro concluído!!!")

            # Criar .json com os dados cadastrados
            while True:
                opc_json = input("Exportar seus dados para um arquivo .json? (Digite 'S' para sim ou 'N' para não): ")
                if opc_json.upper() == 'N':
                    break
                elif opc_json.upper() == 'S':
                    # Insere os dados da tabela conta no arquivo
                    dados_json['Conta'] = select_dados('conta')

                    # Insere os dados da tabela email no arquivo
                    dados_json['Email'] = select_dados('email')

                    # Insere os dados da tabela usuario no arquivo
                    dados_json['Usuario'] = select_dados('usuario')

                    criar_json(dados_json, dados_json['Conta']['nome'])
                    cabecalho(f"Arquivo {dados_json['Conta']['nome']}.json criado!!!")
                    break
                else:
                    exibir_erro()
            break
        case 2:
            # Cadastro Email/Senha
            dados_conta = cadastro_geral('DA CONTA', dados_conta)
            insert_bd('conta', dados_conta)
            
            # Atualizar dados do cadastro
            dados_conta = confirmar_dados('DA CONTA', dados_conta)

            # Cadastro especialista
            dados_especialista = cadastro_geral('ESPECIALISTA', dados_especialista)
            insert_bd('especialista', dados_especialista)
            
            # Atualizar dados do cadastro
            dados_especialista = confirmar_dados('ESPECIALISTA', dados_especialista)
            os.system('cls')
            cabecalho("Cadastro concluído!!!")

            # Criar .json com os dados cadastrados
            while True:
                opc_json = input("Exportar seus dados para um arquivo .json? (Digite 'S' para sim ou 'N' para não): ")
                if opc_json.upper() == 'N':
                    break
                elif opc_json.upper() == 'S':
                    # Insere os dados da tabela conta no arquivo
                    dados_json['Conta'] = select_dados('conta')

                    # Insere os dados da tabela email no arquivo
                    dados_json['Email'] = select_dados('email')

                    # Insere os dados da tabela especialista no arquivo
                    dados_json['Especialista'] = select_dados('especialista')

                    criar_json(dados_json, dados_json['Conta']['nome'])
                    cabecalho(f"Arquivo {dados_json['Conta']['nome']}.json criado!!!")
                    break
                else:
                    exibir_erro()
            break
        case 3:
            # Login Email/Senha
            while True:
                os.system('cls')
                if erro_login:
                    print("\033[031m--> Login não encontrado. Dados podem estar incorretos.\033[m\n")
                cabecalho("LOGIN")
                email_login = validar_email()
                senha_login = validar_senha()
                nome_encontrado, tipo_conta = select_login(email_login, senha_login)
                if nome_encontrado == '' and tipo_conta == '':
                    erro_login = True
                else:
                    break
            cabecalho("Login concluído!!!")
            sleep(2)
            os.system('cls')

            # Login como Moderador
            if tipo_conta == 'MODERADOR':
                cabecalho("Conta de moderador encontrada!!!")
                while True:
                    # Menu de operações disponíveis
                    menu("Ações disponíveis: ", itens_moderador)
                    opc_moderador = int(tratar_erro_numero('Escolha uma opção: '))
                    match opc_moderador:
                        case 1:

                            # Deletando contas do banco de dados
                            while True:
                                menu('Qual o tipo de conta que deseja deletar?', itens_cadastro)
                                opc_deletar = int(tratar_erro_numero('Escolha uma opção: '))
                                match opc_deletar:
                                    case 1:
                                        
                                        # Deletar usuário
                                        while True:
                                            print("Digite o email do usuário que deseja deletar")
                                            email = validacoes('Email')
                                            resultado_delete = delete_bd('usuario', email)
                                            if resultado_delete:
                                                break
                                        break
                                    case 2:
                                        
                                        # Deletar especialista
                                        while True:
                                            print("Digite o CPF do especialista que deseja deletar")
                                            cpf = validacoes('CPF')
                                            resultado_delete = delete_bd('especialista', cpf)
                                            if resultado_delete:
                                                break
                                        break
                                    case _:
                                        exibir_erro()
                            os.system('cls')
                            cabecalho("Conta deletada!!!")

                        case 2:
                            os.system('cls')
                            # Colocando todos os usuários em um arquivo .json
                            usuarios_json = select_todos_dados('usuario')
                            criar_json(usuarios_json, 'Usuarios')
                            cabecalho("Arquivo Usuarios.json criado!!!")

                            # Colocando todos os especialistas em um arquivo .json
                            especialistas_json = select_todos_dados('especialista')
                            criar_json(especialistas_json, 'Especialistas')
                            cabecalho("Arquivo Especialistas.json criado!!!")
                        case 3:
                            break
                        case _:
                            exibir_erro()
            
            # Login como Usuário
            else:
                cabecalho(f"Olá, {nome_encontrado}")
            break
        
        case _:
            exibir_erro()
cabecalho("Finalizando programa...")
cabecalho("Desenvolvido por: Nexus")