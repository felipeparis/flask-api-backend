# Documentação da API BACK-END para Cadastro de Clientes

Esta API é um serviço de back-end para cadastro de clientes. Ele fornece endpoints para criar, buscar, atualizar e listar clientes em um banco de dados PostgreSQL. Além disso, a API integra-se à API pública da Receita Federal do Brasil para obter informações adicionais sobre os clientes com base no CNPJ fornecido.

## Banco de Dados
Foi usado o ElephantSQL para armazenar os dados, usando uma variavel de ambiente com o link do banco.
Para essa API Simples foi usado apenas uma tabela que cumpre seu objetivo, caso queira tornar a aplicação escalavel, é interessante usar outras tabelas relacionadas.

## Requisitos

- Python 3.x
- Flask
- Psycopg2
- Requests
- PostgreSQL
- Variáveis de ambiente configuradas (DATABASE_URL)

## Endpoints

### 1. Cadastrar Cliente

- **URL:** `/api/clientes`
- **Método HTTP:** POST
- **Descrição:** Cria um novo cliente com base nos dados fornecidos, integrando-se à API da Receita Federal do Brasil para obter informações adicionais.
- **Corpo da Requisição (JSON):**
    - `cnpj` (string): CNPJ do cliente.
    - `num_funcionarios` (integer): Número de funcionários (opcional).
    - `faturamento_anual` (numeric): Faturamento anual (opcional).
    - `vendedor_responsavel` (string): Nome do vendedor responsável (opcional).
- **Resposta de Sucesso (HTTP 201):**
    - `message`: Mensagem de sucesso.
    - `dados`: Dados do cliente cadastrado.

### 2. Listar Clientes

- **URL:** `/api/vendedor`
- **Método HTTP:** GET
- **Descrição:** Lista todos os clientes ou os clientes de um vendedor específico.
- **Parâmetros da Requisição (query string):**
    - `vendedor_responsavel` (string, opcional): Nome do vendedor responsável.
- **Resposta de Sucesso (HTTP 200):**
    - Array de objetos JSON, onde cada objeto representa um cliente.

### 3. Buscar Cliente por ID

- **URL:** `/api/buscarcliente/<id>`
- **Método HTTP:** GET
- **Descrição:** Busca um cliente pelo ID fornecido.
- **Parâmetros da Requisição:**
    - `id` (integer): ID do cliente.
- **Resposta de Sucesso (HTTP 200):**
    - Objeto JSON representando os dados do cliente encontrado.

### 4. Atualizar Cliente

- **URL:** `/api/alterarcliente/<id>`
- **Método HTTP:** POST
- **Descrição:** Atualiza as informações de um cliente existente com base no ID fornecido.
- **Parâmetros da Requisição (JSON):**
    - `num_funcionarios` (integer): Novo número de funcionários.
    - `faturamento_anual` (numeric): Novo faturamento anual.
    - `vendedor_responsavel` (string): Novo vendedor responsável.
- **Resposta de Sucesso (HTTP 200):**
    - `message`: Mensagem de sucesso.

## Considerações Finais

Esta API foi desenvolvida para um processo seletivo em 2 dias, há muito a melhorar para se tornar uma aplicação escalável, porém cumpre seu objetivo de Cadastrar clientes e ter acesso a eles.
