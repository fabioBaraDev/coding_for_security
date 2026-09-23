# Exercicio Pratico - Docker: Criando sua propria imagem

## Contexto

Voce recebeu um projeto de uma API Flask que gerencia um sistema escolar (alunos, professores, cursos, matriculas e notas). A aplicacao esta funcional e utiliza um banco de dados PostgreSQL.

Seu desafio e **dockerizar** este projeto, criando sua propria imagem Docker e orquestrando os servicos com Docker Compose.

---

## O que voce recebeu

```
escola_api/
├── pyproject.toml              # Dependencias do projeto (Poetry)
├── poetry.lock                 # Lock das dependencias
├── sql/
│   ├── 01_schema.sql           # Script de criacao das tabelas
│   └── 02_seed.sql             # Script com dados iniciais
└── app/
    ├── __init__.py              # Inicializacao do Flask
    ├── config.py                # Configuracao de conexao com o banco
    ├── controllers/             # Camada de rotas (endpoints HTTP)
    ├── services/                # Camada de regras de negocio
    └── repositories/            # Camada de acesso ao banco de dados
```

### Informacoes importantes antes de comecar

Leia estes arquivos para entender como a aplicacao se conecta ao banco:

**app/config.py** - A aplicacao le as configuracoes do banco a partir de **variaveis de ambiente**:

| Variavel     | Valor esperado  |
|--------------|-----------------|
| `DB_HOST`    | host do banco   |
| `DB_PORT`    | `5432`          |
| `DB_NAME`    | `escola`        |
| `DB_USER`    | `escola_user`   |
| `DB_PASSWORD`| `escola_pass`   |

**Comando para rodar o Flask:**

```bash
python -m flask --app app run --host 0.0.0.0 --port 5000
```

**Dependencias sao gerenciadas com Poetry.** Para instalar:

```bash
pip install poetry
poetry install
```

---

## Etapa 1 - Criando o Dockerfile (construindo sua imagem)

### Objetivo

Criar um arquivo `Dockerfile` na raiz do projeto que construa uma imagem Docker da API.

### Requisitos

O seu Dockerfile deve:

1. Usar a imagem base `python:3.11-slim`
2. Definir o diretorio de trabalho como `/app`
3. Instalar o Poetry
4. Copiar os arquivos de dependencia (`pyproject.toml` e `poetry.lock`) e instala-las
5. Copiar o restante do codigo da aplicacao
6. Expor a porta `5000`
7. Definir o comando de inicializacao do Flask

### Estrutura sugerida

```dockerfile
# 1. Imagem base
FROM ___________

# 2. Diretorio de trabalho
WORKDIR ___________

# 3. Instalar o Poetry e configurar para NAO criar virtualenv
RUN ___________

# 4. Copiar arquivos de dependencia e instalar
COPY ___________ ./
RUN ___________

# 5. Copiar o codigo da aplicacao
COPY ___________

# 6. Expor a porta
EXPOSE ___________

# 7. Comando de inicializacao
CMD ___________
```

### Validacao

Apos criar o Dockerfile, execute:

```bash
docker build -t escola-api .
docker run -p 5000:5000 escola-api
```

**Resultado esperado:** A imagem sera construida com sucesso e o container vai iniciar, mas a API vai dar **erro de conexao com o banco de dados**. Isso e esperado! Voce ainda nao tem um banco rodando. Siga para a Etapa 2.

### Dicas

- Pesquise o que cada instrucao faz: `FROM`, `WORKDIR`, `RUN`, `COPY`, `EXPOSE`, `CMD`
- O Poetry cria virtualenvs por padrao. Dentro de um container isso e desnecessario. Pesquise como desabilitar isso no Poetry
- O `CMD` recebe o comando como uma lista de strings: `["arg1", "arg2", "arg3"]`

---

## Etapa 2 - Criando o Docker Compose (orquestrando os servicos)

### Objetivo

Criar um arquivo `docker-compose.yml` na raiz do projeto que suba **dois servicos**: o banco de dados PostgreSQL e a API Flask.

### Requisitos

O seu `docker-compose.yml` deve definir:

#### Servico `db` (banco de dados)

| Item | Valor |
|------|-------|
| Imagem | `postgres:16-alpine` |
| Variaveis de ambiente | `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (usar os valores da tabela da secao anterior) |
| Porta | `5432:5432` |
| Volume (dados) | Mapear um volume nomeado para `/var/lib/postgresql/data` |
| Volume (scripts SQL) | Mapear a pasta `./sql` para `/docker-entrypoint-initdb.d` |
| Healthcheck | Usar `pg_isready` para verificar se o banco esta pronto |

#### Servico `app` (API Flask)

| Item | Valor |
|------|-------|
| Build | Usar o Dockerfile que voce criou na Etapa 1 |
| Porta | Mapear para a porta `5000` do container |
| Variaveis de ambiente | `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` |
| Dependencia | A API so deve iniciar **apos o banco estar saudavel** |

### Estrutura sugerida

```yaml
services:
  db:
    image: ___________
    environment:
      ___________: ___________
      ___________: ___________
      ___________: ___________
    ports:
      - "___________:___________"
    volumes:
      - ___________:/docker-entrypoint-initdb.d
      - ___________:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "___________"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: ___________
    ports:
      - "___________:___________"
    environment:
      DB_HOST: ___________
      DB_PORT: ___________
      DB_NAME: ___________
      DB_USER: ___________
      DB_PASSWORD: ___________
    depends_on:
      db:
        condition: ___________

volumes:
  ___________:
```

### Validacao

Execute:

```bash
docker compose up --build
```

**Resultado esperado:** O PostgreSQL sobe, executa os scripts SQL, e quando estiver saudavel a API inicia. Teste acessando:

```bash
curl http://localhost:5000/alunos
```

Voce deve receber um JSON com a lista de alunos cadastrados no seed.

### Dicas

- O nome do servico no Docker Compose funciona como hostname na rede interna. Se o servico do banco se chama `db`, entao `DB_HOST` deve ser `db`
- A pasta `/docker-entrypoint-initdb.d` do PostgreSQL executa automaticamente arquivos `.sql` em ordem alfabetica na primeira inicializacao
- Pesquise a diferenca entre `depends_on` simples e `depends_on` com `condition: service_healthy`
- Se a porta 5000 estiver em uso no seu Mac, mapeie para outra porta (ex: `5050:5000`)

---

## Etapa 3 - Perguntas de reflexao

Responda as perguntas abaixo em um arquivo `RESPOSTAS.md` na raiz do projeto.

### Pergunta 1 - Persistencia de dados
Se voce executar `docker compose down` e depois `docker compose up` novamente, os dados do banco sao perdidos? E se usar `docker compose down -v`? Explique a diferenca e o papel dos **volumes** nesse contexto.

### Pergunta 2 - Rede interna do Docker
Por que a API usa `DB_HOST=db` e nao `DB_HOST=localhost`? O que aconteceria se voce trocasse para `localhost`?

### Pergunta 3 - Healthcheck
Qual problema o `healthcheck` com `condition: service_healthy` resolve que o `depends_on` simples nao resolve? Descreva um cenario real onde isso faria diferenca.

### Pergunta 4 - Ordem do COPY no Dockerfile
No Dockerfile, por que copiamos primeiro o `pyproject.toml` e instalamos as dependencias, e so depois copiamos o restante do codigo? O que aconteceria se fizessemos um unico `COPY . .` antes do `RUN poetry install`?

### Pergunta 5 - Boas praticas
Pesquise e explique:
- Qual a diferenca entre `COPY` e `ADD` no Dockerfile?
- Por que usamos `python:3.11-slim` e nao `python:3.11`?
- Para que serve o arquivo `.dockerignore`?

---

## Criterios de avaliacao

| Criterio | Peso |
|----------|------|
| Dockerfile funcional (imagem builda sem erros) | 25% |
| Docker Compose funcional (API e banco sobem corretamente) | 35% |
| Scripts SQL executados automaticamente na inicializacao | 15% |
| Respostas das perguntas de reflexao | 25% |

---

## Entrega

Entregar um repositorio contendo:

```
escola_api/
├── Dockerfile                  # Criado por voce
├── docker-compose.yml          # Criado por voce
├── .dockerignore               # (bonus) Criado por voce
├── RESPOSTAS.md                # Respostas da Etapa 3
├── pyproject.toml
├── poetry.lock
├── sql/
│   ├── 01_schema.sql
│   └── 02_seed.sql
└── app/
    └── (codigo da aplicacao)
```

### Comando para validacao final

O professor vai executar apenas:

```bash
docker compose up --build
```

E testar os endpoints. A aplicacao deve subir sem nenhuma intervencao manual.

---

## Material de apoio

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose reference](https://docs.docker.com/reference/compose-file/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)

Boa sorte!
