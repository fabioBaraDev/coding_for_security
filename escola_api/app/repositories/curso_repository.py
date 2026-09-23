from app.repositories.db import execute_query, execute_returning


def listar():
    return execute_query(
        """SELECT c.*, p.nome AS professor_nome
           FROM cursos c
           LEFT JOIN professores p ON p.id = c.professor_id
           ORDER BY c.id"""
    )


def buscar_por_id(curso_id):
    rows = execute_query(
        """SELECT c.*, p.nome AS professor_nome
           FROM cursos c
           LEFT JOIN professores p ON p.id = c.professor_id
           WHERE c.id = %s""",
        (curso_id,),
    )
    return rows[0] if rows else None


def criar(dados):
    return execute_returning(
        "INSERT INTO cursos (nome, descricao, carga_horaria, professor_id) VALUES (%s, %s, %s, %s) RETURNING *",
        (dados["nome"], dados.get("descricao"), dados["carga_horaria"], dados.get("professor_id")),
    )


def atualizar(curso_id, dados):
    return execute_returning(
        "UPDATE cursos SET nome = %s, descricao = %s, carga_horaria = %s, professor_id = %s WHERE id = %s RETURNING *",
        (dados["nome"], dados.get("descricao"), dados["carga_horaria"], dados.get("professor_id"), curso_id),
    )


def deletar(curso_id):
    execute_query("DELETE FROM cursos WHERE id = %s", (curso_id,), fetch=False)
