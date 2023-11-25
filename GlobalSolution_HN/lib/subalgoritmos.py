import os
import json
from lib.conexoes import *

def linha(tam) -> str:
    return '=' * tam

def cabecalho(txt) -> None:
    print("")
    print(linha(40))
    print(txt.center(40))
    print(linha(40))

def menu(titulo: str, itens: list) -> None:
    cabecalho(titulo)
    c = 1
    for i in itens:
        print(f'{c} - {i}')
        c += 1
    print(linha(40))

# Tratamento de erro para o input de dados numéricos
def tratar_erro_numero(msg: str) -> float:
    n = 0
    while True:
        try:
            n = float(input(msg))
            break
        except ValueError:
            print("\033[031m--> ERRO: Por favor, digite um número.\033[m\n")
            continue
    return n

def exibir_erro() -> None:
    print("\033[031m--> ERRO: Por favor, digite uma opção válida.\033[m\n")

# Organiza os dados digitados em um dicionário e para sua validação
def cadastro_geral(tipo_cadastro, d: dict) -> dict:
    cabecalho(f'CADASTRO {tipo_cadastro}')
    for k in d.keys():
        d[k] = validacoes(k)
    return d

# Permite a atualização dos dados digitados 
# tanto em um dicionário quanto no banco de dados
def confirmar_dados(tipo_cadastro, d: dict) -> dict:
    alterar = "N"
    while alterar.upper() == 'N':
        os.system('cls')
        cont = 0
        opc_alterar = 0
        valores = []

        # Menu para confirmar ou atualizar dados
        cabecalho(f'CADASTRO {tipo_cadastro}')
        for k, v in d.items():
            print(f"{k}: {v}")
            valores.append(f"{k}: {v}")
        print(linha(50))
        while True:
            alterar = input("Suas informações estão corretas? Digite 'S' para sim ou 'N' para não: ")
            if alterar.upper() == 'S' or alterar.upper() == 'N':
                break
            else:
                exibir_erro()

        # Menu para escolher o dado que será alterado
        if alterar.upper() == "N":
            menu("ALTERAR DADOS", valores)
            while True:
                opc_alterar = int(tratar_erro_numero("Digite a opção que deseja alterar: "))
                if opc_alterar in [1, 2, 3]:
                    break
                else:
                    exibir_erro()

            # Seleciona o dado a ser alterado e insere seu novo valor
            for k in d.keys():
                cont += 1
                if opc_alterar == cont:
                    d[k] = validacoes(k)
                    tipo_dado = k
                    novo_dado = d[k]
            
            # Atualiza no banco de dados
            update_bd(tipo_cadastro, tipo_dado, novo_dado)
        
        if alterar.upper() == "S":
            os.system("cls")
    return d

def criar_json(dados: dict, nome_arquivo: str):
    with open(f'{nome_arquivo}.json', 'w') as arq_json:
        json.dump(dados, arq_json, indent=4)

# Organiza as validações para cada tipo de dado
def validacoes(dado) -> None:
    if dado == 'Email':
        return validar_email()
    elif dado == 'CPF':
        return validar_cpf()
    elif dado == 'Senha':
        return validar_senha()
    elif dado == 'CRM':
        return validar_crm()
    else:
        while True:
            valor = input(f"{dado}: ")
            if valor == '':
                print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
            else:
                break
        return valor

def validar_email() -> str:
    caracteres_especiais = ('[!#$%^&*()_+}{=[\-<>?~/|],;:~`')
    validacao = False
    while not validacao:
        email = input("Email: ")
        if email == '':
            print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
        elif email.find('@') == -1:
            print("\033[031m--> ERRO: Seu email não possui um '@'.\033[m\n")
        else:
            validacao = True
            for x in email:
                for y in caracteres_especiais:
                    if x == y:
                        print("\033[031m--> ERRO: Não são permitidos caracteres especiais em um email.\033[m\n")
                        validacao = False
    return email

def validar_cpf():
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while True:
        numeros_cpf = ''
        cpf = input("CPF: ")
        if cpf == '':
            print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
        else:
            # Remove caracteres não numéricos do CPF
            for char in cpf:
                if char in numeros:
                    numeros_cpf += str(char)

            # Verifica se o CPF tem 11 dígitos
            if len(numeros_cpf) != 11:
                print("\033[031m--> ERRO: CPF não possui a quantidade de dígitos necessária.\033[m\n")
            else:
                # Calcula o primeiro dígito verificador
                total = 0
                for i in range(9):
                    total += int(numeros_cpf[i]) * (10 - i)
                resto = total % 11
                if resto < 2:
                    dv1 = 0
                else:
                    dv1 = 11 - resto

                # Calcula o segundo dígito verificador
                total = 0
                for i in range(10):
                    total += int(numeros_cpf[i]) * (11 - i)
                resto = total % 11
                if resto < 2:
                    dv2 = 0
                else:
                    dv2 = 11 - resto

                # Verifica se os dígitos verificadores calculados coincidem com os dígitos no CPF
                if int(numeros_cpf[9]) == dv1 and int(numeros_cpf[10]) == dv2:
                    break
                else:
                    print("\033[031m--> ERRO: CPF inválido.\033[m\n")
    return cpf

def validar_senha():
    validacao = False
    numeros = '1234567890'
    while not validacao:
        senha = input('Senha: ')
        if senha == '':
            print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
        elif len(senha) < 6:
            print("\033[031m--> A senha deve conter, no mínimo, 6 caracteres.\033[m\n")    
        else:
            for x in numeros:
                for y in senha:
                    if x == y:
                        validacao = True
            if validacao == False:
                print("\033[031m--> A senha deve conter, no mínimo, um algarismo.\033[m\n")  
    return senha

def validar_crm():
    while True:
        crm = tratar_erro_numero('CRM (apenas números): ')
        uf = validacoes('UF')

        # Leva as informações à API e corrige a escrita do valor digitado
        if crm_api(crm, uf):
            crm_inteiro = f'{crm}-{uf}'
            break
        
        else:
            print("\033[031m--> CRM inválido. Tente novamente.\033[m\n")
    return crm_inteiro