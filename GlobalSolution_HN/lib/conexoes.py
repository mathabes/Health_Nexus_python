import requests
import os
import cx_Oracle

def insert_bd(tabela: str, dados: dict):
    try:
        if tabela == 'conta':
            # Monta a instrução SQL de cadastro em uma string
            cadastro_conta = f""" INSERT INTO t_hn_conta (nm_completo, ds_senha) 
            VALUES ('{dados['Nome']}', '{dados['Senha']}') """
            
            # Executa e grava o Registro na Tabela
            inst_cadastro.execute(cadastro_conta)
            conn.commit()

            consulta_max_id = f'SELECT MAX(id_conta) FROM t_hn_conta'
            inst_consulta.execute(consulta_max_id)
            # Obtém o máximo ID da tabela t_hn_conta
            id_conta = inst_consulta.fetchone()[0]

            cadastro_email = f""" INSERT INTO t_hn_email (ds_email, st_email, fk_id_conta) 
            VALUES ('{dados['Email']}', 'A', {id_conta}) """
            inst_cadastro.execute(cadastro_email)
            conn.commit()

        elif tabela == 'usuario':
            consulta_max_id = f'SELECT MAX(id_conta) FROM t_hn_conta'
            inst_consulta.execute(consulta_max_id)
            id_conta = inst_consulta.fetchone()[0]

            cadastro_usuario = f""" INSERT INTO t_hn_usuario (tp_conta, fk_id_conta) 
            VALUES ('USUARIO', {id_conta}) """
            inst_cadastro.execute(cadastro_usuario)
            conn.commit()
        else:
            consulta_max_id = f'SELECT MAX(id_conta) FROM t_hn_conta'
            inst_consulta.execute(consulta_max_id)
            id_conta = inst_consulta.fetchone()[0]

            cadastro_espec = f""" INSERT INTO t_hn_especialista (nr_cpf, ds_crm, nm_profissao, fk_id_conta) 
            VALUES ('{dados['CPF']}','{dados['CRM']}', '{dados['Profissão']}', {id_conta}) """
            inst_cadastro.execute(cadastro_espec)
            conn.commit()
    except:
        print("\033[031m--> Erro no cadastro dos dados.\033[m\n")

def update_bd(tabela: str, dado_antigo: int, novo_dado):

    # Convertendo para o nome da coluna no banco
    if dado_antigo == 'Nome':
        dado_antigo = 'nm_completo'
    if dado_antigo == 'Senha':
        dado_antigo = 'ds_senha'
    if dado_antigo == 'Email':
        dado_antigo = 'ds_email'
    if dado_antigo == 'CPF':
        dado_antigo = 'nr_cpf'
    if dado_antigo == 'CRM':
        dado_antigo = 'ds_crm'
    if dado_antigo == 'Profissão':
        dado_antigo = 'nm_profissao'
    
    if tabela == 'DA CONTA':
        tabela = 'conta'
    else:
        tabela = tabela.lower()

    if dado_antigo == 'ds_email':
        tabela = 'email'
    
    consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_hn_{tabela}'
    inst_consulta.execute(consulta_max_id)
    id_exclusao = inst_consulta.fetchone()[0]

    alteracao = f""" UPDATE t_hn_{tabela} SET {dado_antigo} ='{novo_dado}' WHERE id_{tabela}={id_exclusao}"""
    inst_alteracao.execute(alteracao)
    conn.commit()

def select_login(email, senha) ->str:
    try:
        consulta_login = f'''SELECT c.nm_completo, u.tp_conta
        FROM t_hn_conta c
        JOIN t_hn_email e ON c.id_conta = e.fk_id_conta
        JOIN t_hn_usuario u ON c.id_conta = u.fk_id_conta
        WHERE e.ds_email = '{email}' AND c.ds_senha = '{senha}' '''
        
        inst_consulta.execute(consulta_login)
        lista = inst_consulta.fetchall()
        nome = lista[0][0]
        tp_conta = lista[0][1]
    except:
        print("\033[031m--> Login não encontrado. Dados podem estar incorretos.\033[m\n")
        nome = ''
        tp_conta = ''
    return nome, tp_conta
        
def select_dados(tabela) -> dict:
    lista_dados = []
    consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_hn_{tabela}'
    inst_consulta.execute(consulta_max_id)
    ultima_ocorrencia = inst_consulta.fetchone()[0]

    if tabela == 'conta':
        exibir_colunas = ['nome', 'senha']
        colunas_select = 'nm_completo, ds_senha'
    elif tabela == 'email':
        exibir_colunas = ['Email', 'Status']
        colunas_select = 'ds_email, st_email'
    elif tabela == 'usuario':
        exibir_colunas = ['tipo_conta']
        colunas_select = 'tp_conta'
    else:
        exibir_colunas = ['CPF', 'CRM', 'Profissao']
        colunas_select = 'nr_cpf, ds_crm, nm_profissao'

    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute(f'''SELECT {colunas_select} FROM t_hn_{tabela} 
                          WHERE id_{tabela} = {ultima_ocorrencia}
    ''')

    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista_dados.append(dt)

    # ordena a lista
    lista_dados = sorted(lista_dados)
    
    # Cria um dicionário vazio
    dados_dict = {}

    # Adiciona elementos ao dicionário usando um laço de repetição
    for i in range(len(exibir_colunas)):
        if i < len(data[0]):  # Certifica-se de que o índice não ultrapasse o comprimento da lista
            dados_dict[exibir_colunas[i]] = data[0][i]

    return dados_dict

def delete_bd(tp_conta: str, dado: str):
    try:
        if tp_conta == 'usuario':
            consulta_id_conta = f'''SELECT fk_id_conta FROM t_hn_email WHERE ds_email = '{dado}' '''

            inst_consulta.execute(consulta_id_conta)
            id_conta = inst_consulta.fetchone()[0]

            deletar_usuario = f'''DELETE FROM t_hn_usuario WHERE fk_id_conta = {id_conta}'''
            inst_exclusao.execute(deletar_usuario)
            conn.commit()
        else:
            consulta_id_conta = f'''SELECT fk_id_conta FROM t_hn_especialista WHERE nr.cpf = '{dado}' '''

            inst_consulta.execute(consulta_id_conta)
            id_conta = inst_consulta.fetchone()[0]

            deletar_especialista = f'''DELETE FROM t_hn_especialista WHERE fk_id_conta = {id_conta}'''
            inst_exclusao.execute(deletar_especialista)
            conn.commit()
        
        deletar_email = f'''DELETE FROM t_hn_email WHERE fk_id_conta = {id_conta}'''
        inst_exclusao.execute(deletar_email)
        conn.commit()

        deletar_conta = f'''DELETE FROM t_hn_conta WHERE id_conta = {id_conta}'''
        inst_exclusao.execute(deletar_conta)
        conn.commit()
    except:
        print("\033[031m--> ERRO: Conta não encontrada. Tente novamente.\033[m\n")
        return False
    else:
        return True

# Conectando com o banco de dados
try:
    # Conecta o servidor
    dsnStr = cx_Oracle.makedsn("oracle.fiap.com.br", "1521",
                               "ORCL")
    # Efetua a conexão com o Usuário
    conn = cx_Oracle.connect(user='RM98502', password="090405",
                             dsn=dsnStr)
    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    # Informa o erro
    print(f"\033[031mErro: {e}\033[m\n")
    # Flag para não executar a Aplicação
    conexao = False
else:
    print('Conexão funcionando.')