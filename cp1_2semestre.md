# Check Point 01 — Coding for Security (2º Semestre)

## Conteúdo avaliado: Aulas 1 a 4
- **Aula 1:** Bancos de dados SQL vs NoSQL, CRUD, Teorema CAP
- **Aula 2:** MongoDB com PyMongo (CRUD, filtros, agregação, índices)
- **Aula 3:** MySQL com mysql-connector-python (queries parametrizadas, transações, SQL Injection)
- **Aula 4:** Machine Learning com scikit-learn (classificação, anomalias, métricas)

**Cada exercício vale 1 ponto. Nota máxima: 10.**

**Recorte:** este CP cobre o bloco de **persistência de dados + primeiro contato com ML**. É a base sobre a qual todo o resto do semestre se apoia.

> **Ambiente:** MongoDB e MySQL via Docker (ver *Ambiente de Laboratório* na apostila). Pacotes: `pymongo`, `mysql-connector-python`, `scikit-learn`, `numpy`.

---

> **Exercício 1 — Modelagem e CRUD SQL:** Crie a tabela `ativos` no MySQL e escreva os comandos para inserir, listar filtrando por tipo, atualizar o status e remover. Use `ENUM` para o campo `criticidade` e `UNIQUE` no IP.
>
> ```python
> # Schema esperado:
> # ativos(id PK AUTO_INCREMENT, nome, ip UNIQUE, tipo, criticidade ENUM('baixa','media','alta'), status)
>
> # Dados iniciais:
> ativos = [
>     ("SRV-WEB01", "192.168.1.10", "servidor", "alta",  "ativo"),
>     ("PC-RH03",   "192.168.1.45", "estacao",  "baixa", "ativo"),
>     ("SW-CORE01", "192.168.1.1",  "switch",   "media", "inativo"),
> ]
>
> # Saída esperada:
> # Listar tipo='servidor' -> SRV-WEB01 | 192.168.1.10 | alta | ativo
> # Após UPDATE status de SW-CORE01 para 'ativo' -> "1 registro atualizado"
> # Inserir IP duplicado (192.168.1.10) -> erro de UNIQUE tratado
> ```

---

> **Exercício 2 — CRUD com PyMongo:** Conecte ao MongoDB e implemente as quatro operações sobre uma coleção `vulnerabilidades`. Insira, busque por severidade, atualize `corrigida` para `True` e delete por `cve_id`.
>
> ```python
> vulns = [
>     {"cve_id": "CVE-2024-001", "tipo": "SQL Injection", "severidade": "Alta",  "corrigida": False},
>     {"cve_id": "CVE-2024-002", "tipo": "XSS",           "severidade": "Media", "corrigida": True},
>     {"cve_id": "CVE-2024-003", "tipo": "Path Traversal","severidade": "Critica","corrigida": False},
> ]
>
> # Saída esperada:
> # Buscar severidade='Alta'      -> CVE-2024-001: SQL Injection
> # update corrigida=True em 001  -> "1 documento modificado"
> # count corrigida=False         -> 1 (só a CVE-2024-003 restou aberta)
> ```

---

> **Exercício 3 — Agregação: Top IPs:** Insira uma lista de eventos no MongoDB e use um **aggregation pipeline** para retornar os 3 IPs com mais eventos do tipo `FAIL`, ordenados de forma decrescente.
>
> ```python
> eventos = [
>     {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
>     {"tipo": "OK",   "ip": "192.168.1.10"},  {"tipo": "FAIL", "ip": "91.240.118.172"},
>     {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
>     {"tipo": "FAIL", "ip": "45.33.32.156"},  {"tipo": "FAIL", "ip": "185.220.101.1"},
> ]
>
> # Dica: pipeline = [{"$match":{"tipo":"FAIL"}}, {"$group":{"_id":"$ip","total":{"$sum":1}}},
> #                   {"$sort":{"total":-1}}, {"$limit":3}]
>
> # Saída esperada:
> # 185.220.101.1 -> 4
> # 91.240.118.172 -> 2
> # 45.33.32.156  -> 1
> ```

---

> **Exercício 4 — Query parametrizada (defesa contra SQL Injection):** Escreva duas funções de busca por nome de usuário: uma **insegura** (concatenando) e uma **segura** (parametrizada). Demonstre com a entrada `' OR '1'='1` que a insegura vaza todos os registros e a segura não retorna nada.
>
> ```python
> usuarios = [("admin","admin@x.com"), ("ana","ana@x.com"), ("bruno","bruno@x.com")]
> entrada = "' OR '1'='1"
>
> # Saída esperada:
> # [INSEGURO] entrada=' OR '1'='1  -> 3 usuários (VAZAMENTO)
> # [SEGURO]   entrada=' OR '1'='1  -> 0 usuários (defesa OK)
> ```
> ⚠️ Exercício defensivo — rode apenas no banco local de laboratório.

---

> **Exercício 5 — Transação com rollback:** Simule uma transferência entre duas "contas" no MySQL (debita de uma, credita em outra). Se a segunda operação falhar (ex: conta inexistente), faça `rollback` e prove que o saldo da primeira conta não mudou.
>
> ```python
> # Tabela: contas(id, titular, saldo)
> contas = [(1, "Alice", 1000), (2, "Bob", 500)]
>
> # Cenário de teste:
> # Transferir 200 de Alice para Bob      -> commit, saldos: Alice=800, Bob=700
> # Transferir 100 de Alice para conta 99 -> rollback, saldos INALTERADOS: Alice=800
>
> # Saída esperada:
> # Transferência 1 OK. Alice=800, Bob=700
> # Transferência 2 FALHOU (conta destino inexistente). Rollback. Alice=800
> ```

---

> **Exercício 6 — Índice e desempenho:** Crie uma coleção com 1000 eventos gerados em laço, crie um índice no campo `ip` e demonstre uma consulta por IP. Explique em 2 linhas (comentário no código) por que o índice importa quando a coleção cresce.
>
> ```python
> # Dica: gere eventos com um for e insert_many; use create_index("ip").
> # Consulte um IP específico e conte quantos eventos retornaram.
>
> # Saída esperada (exemplo):
> # 1000 eventos inseridos.
> # Índice criado em 'ip'.
> # Eventos do IP 185.220.101.1: 250
> # Comentário: sem índice a busca seria O(n) (varre tudo); com índice ~O(log n).
> ```

---

> **Exercício 7 — Classificador de tráfego:** Treine um `RandomForestClassifier` para distinguir tráfego normal de malicioso. Divida treino/teste (`test_size=0.3, random_state=42`), reporte a acurácia e classifique um caso novo.
>
> ```python
> import numpy as np
> # Features: [bytes, porta, duracao]
> X = np.array([
>     [500,80,0.1],[1200,80,0.5],[64,22,0.02],[64000,4444,10.0],[45000,8080,15.0],
>     [60000,31337,20.0],[800,443,0.3],[300,53,0.05],[55000,9999,18.0],[200,25,0.2],
> ])
> y = np.array([0,0,0,1,1,1,0,0,1,0])
> caso_novo = [[58000, 4444, 16.0]]
>
> # Saída esperada:
> # Acurácia no teste: (imprime o valor, ex. 1.00)
> # Caso novo [58000,4444,16.0] -> Malicioso (1)
> ```

---

> **Exercício 8 — Detecção de anomalias:** Use `IsolationForest` para sinalizar comportamentos anômalos em métricas de acesso. Liste quais amostras foram marcadas como anomalia.
>
> ```python
> import numpy as np
> # [requisicoes_min, conexoes_simultaneas]
> trafego = np.array([
>     [100,5],[120,6],[110,5],[105,4],[50000,500],[109,5],[111,6],[45000,450],
> ])
> # Dica: IsolationForest(contamination=0.25, random_state=42); -1 = anomalia
>
> # Saída esperada:
> # Amostra 4: [50000, 500] -> ANOMALIA
> # Amostra 7: [45000, 450] -> ANOMALIA
> # Demais -> Normal
> ```

---

> **Exercício 9 — Métricas honestas:** Dado um conjunto de teste desbalanceado, calcule acurácia, precisão, recall e F1, e a matriz de confusão. Explique (comentário) por que a acurácia sozinha é enganosa aqui.
>
> ```python
> from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
> y_true = [0,0,0,0,0,0,0,0,1,1]   # 8 normais, 2 ataques
> y_pred = [0,0,0,0,0,0,0,0,0,1]   # perdeu 1 ataque
>
> # Saída esperada:
> # Matriz: [[8,0],[1,1]]
> # Acurácia: 0.90 | Precisão: 1.00 | Recall: 0.50 | F1: 0.67
> # Comentário: acurácia 0.90 mascara que METADE dos ataques passou (recall 0.50).
> ```

---

> **Exercício 10 (Desafio) — Mini-pipeline SIEM: log → MongoDB → ML:** Integre tudo. (1) Leia o `auth.log` (formato da GS do 1º semestre) e normalize cada linha em um documento. (2) Insira todos no MongoDB. (3) Para cada IP, calcule via agregação a contagem de FAILs. (4) Monte um dataset simples `[qtd_fails]` e rotule IP como suspeito (1) se ≥ 5 falhas, senão 0. (5) Treine um classificador e preveja o rótulo de um IP novo com 8 falhas.
>
> ```python
> # auth.log (23 linhas, formato: TIMESTAMP TIPO usuario=NOME ip=IP)
> # 2025-02-20 08:15:01 FAIL usuario=admin ip=185.220.101.1
> # ... (use o arquivo da GS)
>
> # Contagem esperada (agregação):
> # 185.220.101.1 -> 10 FAILs (suspeito=1)
> # 91.240.118.172 -> 5 FAILs (suspeito=1)
> # 45.33.32.156  -> 3 FAILs (suspeito=0)
>
> # Saída esperada:
> # Eventos inseridos no MongoDB: 23
> # Dataset de treino: [[10],[5],[3], ...] rótulos [1,1,0, ...]
> # Previsão para IP com 8 falhas -> Suspeito (1)
> ```

---

### Critérios de correção (sugestão)

| Faixa | Descrição |
|-------|-----------|
| 1,0 por exercício | Requisitos atendidos, saída bate com a esperada |
| 0,5 por exercício | Funcionalidade principal ok, com falhas menores |
| 0,0 | Não implementado ou não funcional |

**Boas práticas valorizadas:** queries parametrizadas (Ex. 4), tratamento de erros de conexão, `random_state` fixo para reprodutibilidade, e uso correto de agregação em vez de laços manuais.
