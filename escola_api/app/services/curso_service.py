from app.repositories import curso_repository


def listar_cursos():
    return curso_repository.listar()


def buscar_curso(curso_id):
    curso = curso_repository.buscar_por_id(curso_id)
    if not curso:
        raise ValueError("Curso nao encontrado")
    return curso


def criar_curso(dados):
    campos = ["nome", "carga_horaria"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return curso_repository.criar(dados)


def atualizar_curso(curso_id, dados):
    curso_repository.buscar_por_id(curso_id)
    campos = ["nome", "carga_horaria"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return curso_repository.atualizar(curso_id, dados)


def deletar_curso(curso_id):
    curso_repository.deletar(curso_id)
