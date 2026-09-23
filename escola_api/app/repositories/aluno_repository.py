from app.repositories.db import execute_query, execute_returning


def listar():
    return execute_query("SELECT * FROM alunos ORDER BY id")


def buscar_por_id(aluno_id):
    rows = execute_query("SELECT * FROM alunos WHERE id = %s", (aluno_id,))
    return rows[0] if rows else None


def criar(dados):
    return execute_returning(
        "INSERT INTO alunos (nome, email, data_nascimento, cpf) VALUES (%s, %s, %s, %s) RETURNING *",
        (dados["nome"], dados["email"], dados.get("data_nascimento"), dados["cpf"]),
    )


def atualizar(aluno_id, dados):
    return execute_returning(
        "UPDATE alunos SET nome = %s, email = %s, data_nascimento = %s, cpf = %s WHERE id = %s RETURNING *",
        (dados["nome"], dados["email"], dados.get("data_nascimento"), dados["cpf"], aluno_id),
    )


def deletar(aluno_id):
    execute_query("DELETE FROM alunos WHERE id = %s", (aluno_id,), fetch=False)
