# Check Point 02 — Coding for Security (2º Semestre)

## Conteúdo avaliado: Aulas 1 a 8

- **Aula 1:** SQL vs NoSQL, modelagem, ACID, Teorema CAP
- **Aula 2:** MongoDB com PyMongo — CRUD, filtros, índices, agregação
- **Aula 3:** MySQL — queries parametrizadas, transações, `commit`/`rollback`
- **Aula 4:** Machine Learning — classificação, anomalias, precisão/recall/F1
- **Aula 6:** APIs Web com Flask — rotas, métodos, validação, status codes
- **Aula 7:** Flask + bancos — serialização, paginação, filtros, erros de banco
- **Aula 8:** OWASP Top 10 (2025), SQL Injection, XSS, misconfiguration, headers, logging

**Cada exercício vale 1 ponto. Nota máxima: 10 (+ até 1,0 de bônus).**

> **Ambiente:** `pymongo`, `mysql-connector-python`, `scikit-learn`, `numpy`, `flask`, `requests`. Bancos via Docker (`mongo-lab` e `mysql-lab`, ver *Ambiente de Laboratório* na apostila). Credenciais em variável de ambiente — qualquer senha escrita no código custa 0,3 do total.

---

> **Exercício 1 — Assistente de decisão de armazenamento (Aulas 1 e 8):** Escreva `recomendar(perfil)` que recebe o perfil de um conjunto de dados e devolve uma recomendação fundamentada: qual banco usar, qual lado do CAP priorizar e qual risco OWASP a escolha errada cria. Nada de `if` solto no meio do código — a função precisa explicar a decisão.
>
> ```python
> # Entrada: dict com as chaves
> #   schema_fixo (bool), precisa_acid (bool), escala_horizontal (bool),
> #   tolera_atraso_de_consistencia (bool), dado_sensivel (bool)
> #
> # Saída: dict {"banco": "MySQL"|"MongoDB", "cap": "CP"|"AP",
> #              "justificativa": str, "risco_owasp": str}
>
> perfis = {
>   "credenciais_do_SOC":      {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
>   "telemetria_de_sensores":  {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":False},
>   "trilha_de_auditoria":     {"schema_fixo":False, "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":False, "dado_sensivel":True},
>   "carrinho_de_licencas":    {"schema_fixo":True,  "precisa_acid":True,  "escala_horizontal":False, "tolera_atraso_de_consistencia":False, "dado_sensivel":False},
>   "cache_de_sessoes":        {"schema_fixo":True,  "precisa_acid":False, "escala_horizontal":True,  "tolera_atraso_de_consistencia":True,  "dado_sensivel":True},
> }
>
> # Saída esperada (formato; as justificativas são suas):
> # credenciais_do_SOC     -> MySQL   | CP | "autenticar errado é pior que ficar fora do ar" | A07
> # telemetria_de_sensores -> MongoDB | AP | "perder 1s de log < parar de aceitar log"       | A09
> # trilha_de_auditoria    -> MongoDB | CP | "auditoria divergente não vale como prova"      | A08
> # ...
> ```
> A `justificativa` precisa nomear **qual erro seria inaceitável** naquele cenário. Repetir a sigla ("é CP porque é consistente") vale 0.

---

> **Exercício 2 — Migração relacional → documentos (Aulas 1, 2 e 3):** O cadastro está normalizado em MySQL (`ativos` 1—N `alertas`). Migre para o MongoDB no modelo de documentos, **aninhando** os dados do ativo dentro de cada alerta, e prove que nada se perdeu no caminho.
>
> ```python
> # MySQL (crie e popule):
> # ativos(id PK, nome, ip UNIQUE, criticidade ENUM('baixa','media','alta'))
> # alertas(id PK, ativo_id FK, tipo, severidade, criado_em)
>
> ativos  = [(1,"SRV-WEB01","192.168.1.10","alta"), (2,"PC-RH03","192.168.1.45","baixa")]
> alertas = [(1,1,"BRUTE_FORCE","critica"), (2,1,"PORT_SCAN","alta"), (3,2,"XSS","media")]
>
> # 1. Leia com um JOIN parametrizado.
> # 2. Monte documentos assim e insira com insert_many:
> # {"tipo":"BRUTE_FORCE","severidade":"critica",
> #  "ativo":{"nome":"SRV-WEB01","ip":"192.168.1.10","criticidade":"alta"}}
> # 3. Verifique a migração: conte no MySQL e no Mongo e compare.
>
> # Saída esperada:
> # MySQL: 3 alertas | MongoDB: 3 documentos -> MIGRAÇÃO ÍNTEGRA
> # Consulta sem JOIN: db.alertas.find({"ativo.criticidade":"alta"}) -> 2 documentos
> # Comentário (2 linhas): o que se ganha (leitura sem JOIN) e o que se perde
> #                        (duplicação: renomear o ativo exige update_many).
> ```

---

> **Exercício 3 — Retenção e janela temporal (Aula 2):** Um SOC não guarda log para sempre nem olha o total — olha a **janela**. Crie a coleção `eventos` com um índice **TTL**, popule 200 eventos espalhados em 24 horas e produza, por agregação, a distribuição de falhas **por hora do dia**.
>
> ```python
> # Dicas:
> # TTL:      eventos.create_index("timestamp", expireAfterSeconds=604800)   # 7 dias
> # Hora:     {"$group": {"_id": {"$hour": "$timestamp"}, "total": {"$sum": 1}}}
> # Filtro de janela: {"timestamp": {"$gte": datetime.now() - timedelta(hours=6)}}
>
> # Saída esperada (exemplo — seus números variam com a geração):
> # === Falhas por hora (últimas 24h) ===
> # 02h | ████████████ 34
> # 03h | ██████████████████ 51   <- pico
> # 09h | ███ 8
> # Hora de pico: 03h (51 falhas)
> # Índice TTL ativo: eventos com mais de 7 dias serão removidos automaticamente.
> # Comentário (1 linha): por que o TTL é uma decisão de segurança, não só de disco.
> ```
> ⚠️ O MongoDB roda a limpeza do TTL a cada ~60s; não espere exclusão instantânea no teste.

---

> **Exercício 4 — Transação com trilha de auditoria (Aulas 2, 3 e 8/A09):** Escreva `alterar_nivel(admin_id, alvo_id, novo_nivel)` que só grava se **tudo** der certo, e que registre a tentativa na trilha de auditoria **mesmo quando falha** — porque ataque que não deixa rastro é ataque invisível (A09).
>
> ```python
> # Regras:
> # - A alteração acontece dentro de uma transação MySQL (commit/rollback).
> # - Só admin com nivel_acesso >= 5 pode alterar; senão, recusa.
> # - Ninguém pode se auto-promover (admin_id == alvo_id -> recusa).
> # - TODA tentativa (aceita ou recusada) vira um documento na coleção Mongo
> #   `auditoria`: {quem, alvo, nivel_anterior, nivel_novo, resultado, timestamp}
>
> usuarios = [(1,"ana","ana@x.com",5), (2,"bruno","bruno@x.com",2), (3,"caio","caio@x.com",1)]
>
> # Sequência de teste e saída esperada:
> # alterar_nivel(1, 2, 4)   -> OK. commit. Bruno: 2 -> 4
> # alterar_nivel(2, 3, 5)   -> RECUSADO (admin sem privilégio). rollback. Caio: 1
> # alterar_nivel(1, 1, 9)   -> RECUSADO (auto-promoção). rollback. Ana: 5
> # alterar_nivel(1, 99, 3)  -> RECUSADO (alvo inexistente). rollback.
> #
> # Trilha de auditoria ao final: 4 documentos (1 sucesso, 3 recusas)
> # db.auditoria.count_documents({"resultado":"RECUSADO"}) -> 3
> ```

---

> **Exercício 5 — O `ORDER BY` que o `%s` não protege (Aulas 3, 6, 7 e 8/A05):** Crie `GET /api/eventos?ordenar_por=&ordem=&tamanho=` sobre o MySQL. Descubra na prática que **placeholder não parametriza nome de coluna** e defenda com *whitelist*.
>
> ```python
> # ❌ Tentativa ingênua (não compila como parâmetro — e concatenar abre injeção):
> # cur.execute(f"SELECT * FROM eventos ORDER BY {col} {ordem} LIMIT {tam}")
>
> # ✅ Defesa: mapa fechado de valores permitidos
> COLUNAS = {"data": "criado_em", "sev": "severidade", "ip": "ip_origem"}
> ORDEM   = {"asc": "ASC", "desc": "DESC"}
>
> # Testes obrigatórios (com o servidor no ar):
> # GET /api/eventos?ordenar_por=sev&ordem=desc&tamanho=5
> #   -> 200, 5 eventos ordenados por severidade
> # GET /api/eventos?ordenar_por=criado_em,(SELECT+1)&ordem=asc
> #   -> 400 {"erro":"campo de ordenação inválido"}   (NÃO 500, NÃO executa)
> # GET /api/eventos?tamanho=abc
> #   -> 400 {"erro":"tamanho deve ser inteiro"}
> # GET /api/eventos?tamanho=100000
> #   -> 200, mas no máximo 100 registros (teto do servidor)
>
> # Entregue também, em comentário de 3 linhas: por que `LIMIT %s` funciona
> # mas `ORDER BY %s` não, e o que isso diz sobre "identificador vs dado".
> ```

---

> **Exercício 6 — Controle de acesso quebrado (Aulas 3, 6 e 8/A01):** Uma API de incidentes em que cada analista só pode ver os **seus** incidentes, e apenas nível ≥ 5 pode apagar qualquer um. Autenticação por header `X-API-Key` validado no MySQL com query parametrizada.
>
> ```python
> # Tabelas: analistas(id, nome, api_key UNIQUE, nivel)
> #          incidentes(id, dono_id FK, titulo, severidade, status)
>
> analistas  = [(1,"ana","key-ana-001",5), (2,"bruno","key-bruno-002",2)]
> incidentes = [(1,1,"Brute force SSH","critica"), (2,2,"Phishing no RH","media")]
>
> # Matriz de testes — a saída esperada é o status code:
> # | Requisição                                   | Header            | Esperado |
> # | GET    /api/incidentes/1                     | key-ana-001       | 200      |
> # | GET    /api/incidentes/1                     | key-bruno-002     | 403      |  <- IDOR barrado
> # | GET    /api/incidentes/1                     | (sem header)      | 401      |
> # | GET    /api/incidentes/1                     | key-inexistente   | 401      |
> # | GET    /api/incidentes                       | key-bruno-002     | 200, só o incidente 2 |
> # | DELETE /api/incidentes/2                     | key-ana-001       | 200      |  <- nível 5
> # | DELETE /api/incidentes/1                     | key-bruno-002     | 403      |
> # | GET    /api/incidentes/999                   | key-ana-001       | 404      |
>
> # Atenção ao par 401 x 403: 401 = "não sei quem você é";
> #                           403 = "sei quem você é e você não pode".
> # O corpo do 403 NÃO pode revelar se o incidente existe ou não.
> ```

---

> **Exercício 7 — XSS onde ninguém procura: dentro do atributo (Aulas 6, 7 e 8/A05):** Monte `GET /dashboard` que renderiza uma tabela de incidentes vindos do MongoDB, incluindo o nome do ativo dentro de um atributo HTML (`<img src="/icone.png" alt="...">`). Prove que sua defesa segura **dois** payloads diferentes.
>
> ```python
> # Cadastre dois incidentes com estes títulos/ativos:
> p1 = "<script>alert('xss1')</script>"
> p2 = 'x" onerror="alert(\'xss2\')'      # escapa do atributo, sem usar <script>
>
> # Saída esperada na página:
> # - p1 aparece como TEXTO literal na célula da tabela
> # - p2 aparece como TEXTO literal dentro do alt, e a imagem NÃO dispara alert
> # - Nenhum alert() abre no navegador
>
> # Requisitos adicionais:
> # 1. Use template Jinja2 (escape por padrão) — e explique em 1 linha por que
> #    um |safe mal colocado reabriria o buraco.
> # 2. Header Content-Security-Policy: default-src 'self' em todas as respostas.
> # 3. Uma rota /dashboard-inseguro, claramente marcada, para comparação lado a lado.
> ```
> ⚠️ Exercício defensivo. Os payloads rodam apenas contra a sua própria aplicação local.

---

> **Exercício 8 — Modelo de ML servido por API, com métricas auditáveis (Aulas 2, 4, 6 e 7):** Treine um classificador de risco e exponha-o. O ponto do exercício é que **entrada de modelo também é entrada de usuário**: precisa ser validada.
>
> ```python
> # Features: [falhas_login, portas_distintas, bytes_saida, hora_do_dia]
> # Rotas:
> #   POST /api/triagem          -> {"risco":"alto"|"baixo", "confianca":0.xx}
> #   GET  /api/modelo/metricas  -> precisão, recall, F1 e matriz de confusão do conjunto de teste
> #
> # Toda previsão é gravada no MongoDB (coleção `previsoes`) com entrada,
> # saída, confiança e timestamp — para auditar o modelo depois (A09/A08).
>
> # Sequência de teste e saída esperada:
> # POST {"features":[12,7,90000,3]}      -> 200 {"risco":"alto","confianca":0.9x}
> # POST {"features":[0,1,1200,14]}       -> 200 {"risco":"baixo","confianca":0.9x}
> # POST {"features":[12,7,90000]}        -> 400 {"erro":"esperadas 4 features, recebidas 3"}
> # POST {"features":["12","sete",0,3]}   -> 400 {"erro":"features devem ser numéricas"}
> # POST {} (sem corpo)                   -> 400
> # GET  /api/modelo/metricas             -> 200 {"precisao":0.xx,"recall":0.xx,
> #                                               "f1":0.xx,"matriz":[[..],[..]]}
> # db.previsoes.count_documents({})      -> 2 (só as previsões válidas foram gravadas)
>
> # Na resposta do GET, inclua o campo "aviso" com uma frase sua explicando
> # por que a acurácia foi omitida de propósito desta API.
> ```

---

> **Exercício 9 — Rate limiting guiado por anomalia (Aulas 2, 4, 6 e 8/A09):** A própria API vira fonte de dados: registre cada requisição no MongoDB, extraia por agregação o comportamento de cada IP e use `IsolationForest` para decidir quem é bloqueado com **429**.
>
> ```python
> # 1. @app.before_request grava {ip, rota, metodo, timestamp} na coleção `acessos`.
> # 2. @app.after_request completa o registro com o status code devolvido.
> # 3. Agregação por IP -> features [req_por_minuto, taxa_4xx, rotas_distintas]
> # 4. IsolationForest(contamination=0.2, random_state=42) marca os anômalos.
> # 5. IP anômalo recebe 429 nas próximas requisições, com header Retry-After: 60.
>
> # Roteiro de teste (script com requests):
> # - IP "normal": 5 requisições válidas espaçadas         -> todas 200
> # - IP "hostil": 60 requisições em 10s, 40 delas para rotas inexistentes
> #
> # Saída esperada:
> # === Análise de acessos ===
> # 192.168.1.10   [ 0.5 req/min | 4xx 0.00 | 2 rotas]  -> normal
> # 185.220.101.1  [ 360 req/min | 4xx 0.67 | 9 rotas]  -> ANOMALIA -> bloqueado
> # Próxima requisição de 185.220.101.1 -> 429 {"erro":"muitas requisições"}
> #                                        Retry-After: 60
> #
> # Comentário (2 linhas): qual é o risco de bloquear por anomalia em vez de
> # por regra fixa? (dica: falso positivo aqui derruba usuário legítimo).
> ```

---

> **Exercício 10 (Desafio) — Antes e depois: prove o ataque, aplique a defesa, prove a defesa (Aulas 1 a 8):** Você recebe a API vulnerável abaixo. Entregue **três arquivos**: `exploit.py` (demonstra cada falha contra a sua própria cópia local), `app_seguro.py` (a versão corrigida) e `auditoria.md` (uma linha por falha: código OWASP 2025, impacto e correção). O mesmo `exploit.py`, rodado contra `app_seguro.py`, deve falhar em **todos** os ataques.
>
> ```python
> # ===== app_vulneravel.py — laboratório apenas =====
> from flask import Flask, request, jsonify
> import mysql.connector
>
> app = Flask(__name__)
> SENHA_MESTRA = "Cyber@2024"
>
> def db():
>     return mysql.connector.connect(host="localhost", user="root",
>                                    password="senha", database="seguranca")
>
> @app.route("/api/usuarios/buscar")
> def buscar():
>     nome = request.args.get("nome", "")
>     cur = db().cursor(dictionary=True)
>     cur.execute(f"SELECT * FROM usuarios WHERE nome LIKE '%{nome}%'")
>     return jsonify(cur.fetchall())
>
> @app.route("/perfil")
> def perfil():
>     return f"<h1>Bem-vindo, {request.args.get('u','')}</h1>"
>
> @app.route("/api/usuarios/<int:uid>", methods=["DELETE"])
> def remover(uid):
>     con = db(); cur = con.cursor()
>     cur.execute("DELETE FROM usuarios WHERE id = %s", (uid,))
>     con.commit()
>     return jsonify({"removido": uid})
>
> @app.route("/api/relatorio")
> def relatorio():
>     cur = db().cursor()
>     cur.execute("SELECT * FROM tabela_inexistente")
>     return jsonify(cur.fetchall())
>
> if __name__ == "__main__":
>     app.run(debug=True, host="0.0.0.0")
> ```
>
> ```python
> # Encontre no mínimo 8 falhas. DUAS delas são AUSÊNCIAS: não estão escritas
> # em lugar nenhum do arquivo, e é exatamente por isso que são falhas.
>
> # Saída esperada do exploit.py ANTES da correção:
> # [1] Injeção em /api/usuarios/buscar?nome=' OR '1'='1  -> 3 usuários (VAZAMENTO)
> # [2] XSS em /perfil?u=<script>alert(1)</script>        -> payload volta cru
> # [3] DELETE /api/usuarios/2 sem credencial             -> 200 (usuário apagado!)
> # [4] GET /api/relatorio                                -> 500 com traceback e nome da tabela
> # [5] Resposta de /api/usuarios/buscar                  -> traz coluna senha
> # [6] Headers de segurança                              -> ausentes
> # ... 6 ataques bem-sucedidos.
>
> # Saída esperada do MESMO exploit.py DEPOIS (contra app_seguro.py):
> # [1] -> 0 usuários (parametrizado)            DEFENDIDO
> # [2] -> payload escapado, texto literal       DEFENDIDO
> # [3] -> 401 sem credencial / 403 sem nível    DEFENDIDO
> # [4] -> 500 {"erro":"erro interno"} sem detalhe  DEFENDIDO
> # [5] -> resposta sem a coluna senha           DEFENDIDO
> # [6] -> 3 headers presentes                   DEFENDIDO
> # === 0 de 6 ataques bem-sucedidos ===
> ```
> ⚠️ Rode o exploit **exclusivamente** contra a sua cópia local. Apontar esse script para qualquer sistema de terceiros é crime (Lei 12.737/2012).

---

### Critérios de correção

| Faixa | Descrição |
|-------|-----------|
| 1,0 por exercício | Funciona, a saída bate com a esperada **e** a parte de segurança está correta |
| 0,7 | Funciona, mas a defesa de segurança do enunciado está incompleta |
| 0,5 | Funcionalidade principal ok, com falhas menores (status code errado, validação ausente) |
| 0,0 | Não implementado ou não funcional |

**Boas práticas valorizadas:** agregação feita no banco e não em laço Python; status codes semânticos (201/400/401/403/404/409/429); `random_state` fixo para reprodutibilidade; mensagens de erro que não diferenciam "não existe" de "não pode"; e logging de requisições — o A09 é a falha que impede você de descobrir todas as outras.
