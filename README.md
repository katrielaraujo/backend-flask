# API de Vendas

Esta é uma API de Vendas desenvolvida usando Flask, Flask-SQLAlchemy e JWT para autenticação. A API permite o registro e autenticação de usuários, operações CRUD em vendas e a geração de PDFs com informações de vendas em intervalos de datas.

## Pré-requisitos

- Python 3.10 ou superior
- Pipenv ou venv para gerenciamento de ambientes virtuais

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/katrielaraujo/backend-flask.git
    cd backend-flask
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

 Crie um arquivo `instance/config.py` e configure as variáveis conforme necessário: 
     
    ```python
    import os

    class Config:
        SECRET_KEY = 'admin123'
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'vendas.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = 'super-secret'

    class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ```

## Execução

1. Inicialize o repositório de migrações:
    ```bash
    flask db init
    ```
2. Crie a primeira migração:
    ```bash
    flask db migrate -m "Initial migration"
    ```
3. Aplique a migração ao banco de dados:
    ```bash
    flask db upgrade
    ```

1. Inicie a aplicação:
    ```bash
    flask run
    ```

    A aplicação estará disponível em `http://127.0.0.1:5000`.

## Testes

1. Para executar os testes automatizados, utilize o pytest:
    ```bash
    pytest
    ```

## Documentação das Funcionalidades

### Autenticação de Usuários
- **POST /register**: Registro de novos usuários.
    - Campos: `email`, `senha`
- **POST /login**: Autenticação de usuários existentes.
    - Campos: `email`, `senha`

### CRUD de Vendas
- **GET /sales**: Consultar todas as vendas.
- **POST /sales**: Adicionar uma nova venda.
    - Campos: `nome_cliente`, `produto`, `valor`, `data_venda`
- **PUT /sales/:id**: Editar uma venda existente.
    - Campos: `nome_cliente`, `produto`, `valor`, `data_venda`
- **DELETE /sales/:id**: Excluir uma venda existente.

### Geração de PDF
- **GET /sales/pdf?start_date=DD-MM-YYYY&end_date=DD-MM-YYYY**: Gerar um PDF contendo todas as vendas entre `start_date` e `end_date`.

## Escolhas Tecnológicas e Arquitetônicas

- **Flask-SQLAlchemy**: Integração com o SQLAlchemy para mapeamento objeto-relacional.
- **Flask-JWT-Extended**: Biblioteca para autenticação JWT, garantindo segurança nas operações.
- **pytest**: Framework de testes utilizado para garantir a qualidade do código.

A arquitetura do projeto está organizada de forma a separar as preocupações, facilitando a manutenção e a escalabilidade:
- **app/**: Contém a lógica da aplicação (modelos, rotas, utilitários).
- **instance/**: Contém as configurações específicas da instância.
- **tests/**: Contém os testes automatizados.
- **venv/**: Ambiente virtual.

## Segurança

- **Autenticação JWT**: Implementada para proteger as rotas e garantir que apenas usuários autenticados possam acessar as funcionalidades críticas.
- **Hashing de Senhas**: Senhas são armazenadas de forma segura usando hashing com Bcrypt.

## Contato

Para mais informações, entre em contato pelo e-mail: [katrielaraujo@gmail.com](mailto:katrielaraujo@gmail.com)
