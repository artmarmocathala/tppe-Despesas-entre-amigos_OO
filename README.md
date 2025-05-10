# tppe-Despesas-entre-amigos_OO

## Documentação

## Dependências

Docker e docker compose

## Infra

Docker e docker compose para gerenciar os serviços

### Serviços
- Backend em python/flask na porta 5000
- banco postgres na porta 5432
    - usuário: tppe
    - senha: escondidinho
    - banco: db

### Como rodar

1. Clonar o repositório
2. Instalar as dependências
3. na raiz do projeto:
    ```bash
    docker-compose up --build
    ```
4. Acessar a api por http://localhost:5000 e banco em localhost:5432