from app.repositories.db import execute_query, execute_returning


def listar():
    return execute_query(
        """SELECT n.*, a.nome AS aluno_nome, c.nome AS curso_nome
           FROM notas n
           JOIN matriculas m ON m.id = n.matricula_id
           JOIN alunos a ON a.id = m.aluno_id
           JOIN cursos c ON c.id = m.curso_id
           ORDER BY n.id"""
    )


def buscar_por_id(nota_id):
    rows = execute_query(
        """SELECT n.*, a.nome AS aluno_nome, c.nome AS curso_nome
           FROM notas n
           JOIN matriculas m ON m.id = n.matricula_id
           JOIN alunos a ON a.id = m.aluno_id
           JOIN cursos c ON c.id = m.curso_id
           WHERE n.id = %s""",
        (nota_id,),
    )
    return rows[0] if rows else None


def criar(dados):
    return execute_returning(
        "INSERT INTO notas (matricula_id, valor, descricao, data_avaliacao) VALUES (%s, %s, %s, COALESCE(%s, CURRENT_DATE)) RETURNING *",
        (dados["matricula_id"], dados["valor"], dados.get("descricao"), dados.get("data_avaliacao")),
    )


def atualizar(nota_id, dados):
    return execute_returning(
        "UPDATE notas SET matricula_id = %s, valor = %s, descricao = %s, data_avaliacao = %s WHERE id = %s RETURNING *",
        (dados["matricula_id"], dados["valor"], dados.get("descricao"), dados.get("data_avaliacao"), nota_id),
    )


def deletar(nota_id):
    execute_query("DELETE FROM notas WHERE id = %s", (nota_id,), fetch=False)
