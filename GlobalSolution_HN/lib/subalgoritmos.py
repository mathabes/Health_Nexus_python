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

def cadastro_geral(tipo_cadastro, d: dict) -> dict:
    cabecalho(f'CADASTRO {tipo_cadastro}')
    for k in d.keys():
        d[k] = validacoes(k)
    return d

def confirmar_dados(tipo_cadastro, d: dict) -> dict:
    alterar = "N"
    while alterar.upper() == 'N':
        os.system('cls')
        cont = 0
        opc_alterar = 0
        valores = []
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
        if alterar.upper() == "N":
            menu("ALTERAR DADOS", valores)
            while True:
                opc_alterar = int(tratar_erro_numero("Digite a opção que deseja alterar: "))
                if opc_alterar in [1, 2, 3]:
                    break
                else:
                    exibir_erro()
            for k in d.keys():
                cont += 1
                if opc_alterar == cont:
                    d[k] = validacoes(k)
                    tipo_dado = k
                    novo_dado = d[k]
            update_bd(tipo_cadastro, tipo_dado, novo_dado)
        if alterar.upper() == "S":
            os.system("cls")
    return d

def criar_json(dados: dict, nome_arquivo: str):
    with open(f'{nome_arquivo}.json', 'w') as arq_json:
        json.dump(dados, arq_json, indent=4)

def validacoes(dado) -> None:
    if dado == 'Email':
        return validar_email()
    elif dado == 'CPF':
        return validar_cpf()
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