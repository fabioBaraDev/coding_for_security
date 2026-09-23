from app.repositories.db import execute_query, execute_returning


def listar():
    return execute_query("SELECT * FROM professores ORDER BY id")


def buscar_por_id(professor_id):
    rows = execute_query("SELECT * FROM professores WHERE id = %s", (professor_id,))
    return rows[0] if rows else None


def criar(dados):
    return execute_returning(
        "INSERT INTO professores (nome, email, especialidade) VALUES (%s, %s, %s) RETURNING *",
        (dados["nome"], dados["email"], dados.get("especialidade")),
    )


def atualizar(professor_id, dados):
    return execute_returning(
        "UPDATE professores SET nome = %s, email = %s, especialidade = %s WHERE id = %s RETURNING *",
        (dados["nome"], dados["email"], dados.get("especialidade"), professor_id),
    )


def deletar(professor_id):
    execute_query("DELETE FROM professores WHERE id = %s", (professor_id,), fetch=False)
