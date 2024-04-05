# API BACK-END PARA CADASTRO DE CLIENTES, DOCUMENTAÇÃO EM README

import os
import re
import psycopg2
import requests

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)
url = os.getenv('DATABASE_URL')

# Conexão com o banco
connection = psycopg2.connect(url)

# Constantes SQL para uso no banco de dados.
CREATE_TABLE_CLIENTE = (
    """ CREATE TABLE IF NOT EXISTS cliente ( 
        id SERIAL PRIMARY KEY,  
        cnpj VARCHAR(18) NOT NULL UNIQUE, 
        situacao VARCHAR(20), 
        tipo VARCHAR(20), 
        razao_social VARCHAR(100), 
        nome_fantasia VARCHAR(200), 
        estado VARCHAR(100), 
        municipio VARCHAR(100), 
        endereco VARCHAR(200), 
        natureza_juridica VARCHAR(200), 
        porte VARCHAR(50), 
        atividade_principal VARCHAR(100), 
        telefone VARCHAR(200), 
        num_funcionarios INTEGER, 
        faturamento_anual NUMERIC, 
        vendedor_responsavel VARCHAR(300) ); """
)

INSERT_CLIENTE = (
    """ INSERT INTO cliente (cnpj, situacao, tipo,  nome_fantasia, estado, municipio, endereco,
        natureza_juridica, porte, atividade_principal, telefone, num_funcionarios, faturamento_anual, vendedor_responsavel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    )

SELECT_ALL = "SELECT * FROM cliente"
SELECT_CLIENTE_VENDEDOR = "SELECT * FROM cliente WHERE vendedor_responsavel = %s"
SELECT_CLIENTE_ONE = "SELECT * FROM cliente WHERE id = %s"
UPDATE_CLIENTE_ONE = "UPDATE cliente SET num_funcionarios = %s, faturamento_anual = %s, vendedor_responsavel = %s WHERE id = %s"
SELECT_COLUMNS = "SELECT column_name FROM information_schema.columns WHERE table_name = %s"


# função para buscar os informações da empresa de acordo com o CNPJ. apenas numeros
def get_rf_data(cnpj):
    cnpj = re.sub(r"[^\w\d]", "", cnpj) #função regex para retirar a mascara do CNPJ.
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    data = response.json()
    return data
    
# transforma array em json de acordo com as colunas do banco
def transforma_json(valor):    
    chave = get_colunas('cliente')
    
    if len(chave) != len(valor):
        raise ValueError("Os arrays de chave e valor devem ter o mesmo tamanho.")

    result = {}
    
    for i in range(len(chave)):
        result[chave[i]]=valor[i]
        
    return result

# devolve as colunas de uma tabela em forma de array
def get_colunas(nome_tabela):
    cursor = connection.cursor()
    cursor.execute(SELECT_COLUMNS,(nome_tabela,))
    
    colunas = cursor.fetchall()
    
    result = [coluna[0] for coluna in colunas]
    
    return result

# Inserir clientes na base
@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    cnpj = data['cnpj']

    rf_data = get_rf_data(cnpj) # dados da receita federal

    #dados editaveis no front
    rf_data['num_funcionarios'] = data.get('num_funcionarios') 
    rf_data['faturamento_anual'] = data.get('faturamento_anual')
    rf_data['vendedor_responsavel'] = data.get('vendedor_responsavel')    


    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_CLIENTE) # cria tabela caso ela nao existe
            cursor.execute(INSERT_CLIENTE, (
                rf_data['cnpj'], 
                rf_data['situacao'], 
                rf_data['tipo'], 
                rf_data['fantasia'],
                rf_data['uf'], 
                rf_data['municipio'], 
                rf_data['logradouro'], 
                rf_data['natureza_juridica'],
                rf_data['porte'], 
                rf_data['atividade_principal'][0]['text'], # campo json type na API.
                rf_data['telefone'], 
                rf_data['num_funcionarios'],
                rf_data['faturamento_anual'], 
                rf_data['vendedor_responsavel']
            ))

        connection.commit()

    return jsonify({'message': 'Cliente cadastrado com sucesso', 'dados': rf_data}), 201

@app.route('/api/vendedor', methods=['GET'])
def get_cliente():
    data = request.get_json()
    vendedor_responsavel = data.get('vendedor_responsavel')
    
    cursor = connection.cursor()
    if vendedor_responsavel:
        cursor.execute(SELECT_CLIENTE_VENDEDOR, (vendedor_responsavel,))
    else:
        cursor.execute(SELECT_ALL)
    
    response = cursor.fetchall()
    
    if response == []:
        return jsonify({'message':'Vendedor não cadastrado'}) 

    result = [transforma_json(registro) for registro in response]
    
    return jsonify(result), 200
# verificar pq não esta voltando um JSON.

# Metodo get para  buscar um cliente pelo ID
@app.route('/api/buscarcliente/<int:id>', methods=['GET'])
def get_cliente_one(id):
    id_cliente = int(id)
    
    cursor = connection.cursor()
    
    cursor.execute(SELECT_CLIENTE_ONE,(id_cliente,))
    response = cursor.fetchone()
    response = transforma_json(response)
    
    return jsonify(response)

# Alterar informações do cliente
@app.route('/api/alterarcliente/<int:id>', methods=['POST'])
def update_cliente_one(id):
    id_cliente = int(id)
    data = request.get_json()
    num_funcionarios = data['num_funcionarios']
    faturamento_anual = data['faturamento_anual']
    vendedor_responsavel = data['vendedor_responsavel']
            
    cursor = connection.cursor()
    
    cursor.execute(UPDATE_CLIENTE_ONE, (num_funcionarios, faturamento_anual, vendedor_responsavel, id_cliente))
    connection.commit()
    
    return jsonify({"message":"Cliente atualizado com sucesso!"})