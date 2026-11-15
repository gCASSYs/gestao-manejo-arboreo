# Gestão de Manejo Arbóreo

MVP acadêmico para organizar e acompanhar solicitações fictícias de manejo arbóreo. O projeto foi concebido no curso de Análise e Desenvolvimento de Sistemas e não representa um sistema oficial da Prefeitura de São Paulo ou da Subprefeitura de Santo Amaro.

## Objetivo

Centralizar o cadastro e o acompanhamento de solicitações, oferecendo uma interface simples, responsiva e acessível para demonstrar o fluxo administrativo proposto.

## Tecnologias

- Python 3.12+
- Flask
- SQLite
- Bootstrap 5

## Estrutura

```text
gestao-manejo-arboreo/
├── app/
│   ├── static/css/
│   ├── templates/
│   ├── __init__.py
│   ├── db.py
│   └── routes.py
├── instance/          # banco local (não versionado)
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

## Execução local

1. Crie e ative um ambiente virtual.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e defina uma chave local.
4. Execute `flask --app run.py run --debug`.
5. Acesse `http://127.0.0.1:5000`.

O banco SQLite é criado automaticamente em `instance/manejo.db`. Os registros exibidos são exclusivamente fictícios.

## Segurança e privacidade

- Não use dados pessoais, institucionais ou credenciais reais.
- O arquivo `.env` e o banco local não são versionados.
- A chave presente em `.env.example` é apenas um marcador e deve ser substituída localmente.

## Escopo acadêmico

Esta versão inicial demonstra organização do projeto, painel, formulário e listagem. Autenticação, autorização, auditoria, testes de segurança e implantação produtiva permanecem fora do escopo deste protótipo inicial.

## Licença

Distribuído sob a licença MIT. Consulte `LICENSE`.
