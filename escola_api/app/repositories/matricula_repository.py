from app.repositories.db import execute_query, execute_returning


def listar():
    return execute_query(
        """SELECT m.*, a.nome AS aluno_nome, c.nome AS curso_nome
           FROM matriculas m
           JOIN alunos a ON a.id = m.aluno_id
           JOIN cursos c ON c.id = m.curso_id
           ORDER BY m.id"""
    )


def buscar_por_id(matricula_id):
    rows = execute_query(
        """SELECT m.*, a.nome AS aluno_nome, c.nome AS curso_nome
           FROM matriculas m
           JOIN alunos a ON a.id = m.aluno_id
           JOIN cursos c ON c.id = m.curso_id
           WHERE m.id = %s""",
        (matricula_id,),
    )
    return rows[0] if rows else None


def criar(dados):
    return execute_returning(
        "INSERT INTO matriculas (aluno_id, curso_id, data_matricula, status) VALUES (%s, %s, COALESCE(%s, CURRENT_DATE), %s) RETURNING *",
        (dados["aluno_id"], dados["curso_id"], dados.get("data_matricula"), dados.get("status", "ativa")),
    )


def atualizar(matricula_id, dados):
    return execute_returning(
        "UPDATE matriculas SET aluno_id = %s, curso_id = %s, status = %s WHERE id = %s RETURNING *",
        (dados["aluno_id"], dados["curso_id"], dados.get("status", "ativa"), matricula_id),
    )


def deletar(matricula_id):
    execute_query("DELETE FROM matriculas WHERE id = %s", (matricula_id,), fetch=False)
