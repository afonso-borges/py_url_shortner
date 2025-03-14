# URL Shortener API

Uma API simples para encurtar URLs e rastrear estatísticas de acesso.

## Funcionalidades

- Encurtamento de URLs
- Códigos personalizados
- Expiração de URLs
- Rastreamento de acessos
- Estatísticas de uso
- Autenticação via API Key

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para interação com banco de dados
- [Pydantic](https://docs.pydantic.dev/) - Validação de dados

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/afonso-borges/py_url_shortner.git
cd py_url_shortner
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente criando um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

## Executando a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em http://localhost:8000 e a documentação em http://localhost:8000/docs.

## Endpoints

### Encurtar URL

```http
POST /api/shorten
X-API-Key: your_secret_api_key

{
  "original_url": "https://example.com/very-long-url",
  "expires_in_days": 30,
  "custom_code": "exemplo"  // opcional
}
```

### Obter estatísticas

```http
GET /api/stats/{short_code}
X-API-Key: your_secret_api_key
```

### Listar URLs

```http
GET /api/list?skip=0&limit=100
X-API-Key: your_secret_api_key
```

### Redirecionar para URL original

```http
GET /{short_code}
```

## Testes

Execute os testes com:

```bash
pytest
```

## Estrutura do Projeto

```
py_url_shortner/
├── app/
│   ├── api/
│   │   ├── dependencies.py  # Dependências da API (autenticação)
│   │   └── routes.py        # Rotas da API
│   ├── models/
│   │   ├── database.py      # Configuração do banco de dados
│   │   └── url.py           # Modelo de URL
│   ├── services/
│   │   └── url_service.py   # Lógica de negócio
│   ├── utils/
│   │   └── config.py        # Configurações da aplicação
│   ├── main.py              # Ponto de entrada da aplicação
│   └── schemas.py           # Esquemas Pydantic
├── tests/
│   ├── conftest.py          # Configurações para testes
│   └── test_url_service.py  # Testes do serviço de URL
├── .env                     # Variáveis de ambiente (não versionado)
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação
```
