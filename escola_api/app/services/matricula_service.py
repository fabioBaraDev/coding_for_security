from app.repositories import matricula_repository


def listar_matriculas():
    return matricula_repository.listar()


def buscar_matricula(matricula_id):
    matricula = matricula_repository.buscar_por_id(matricula_id)
    if not matricula:
        raise ValueError("Matricula nao encontrada")
    return matricula


def criar_matricula(dados):
    campos = ["aluno_id", "curso_id"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return matricula_repository.criar(dados)


def atualizar_matricula(matricula_id, dados):
    matricula_repository.buscar_por_id(matricula_id)
    campos = ["aluno_id", "curso_id"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return matricula_repository.atualizar(matricula_id, dados)


def deletar_matricula(matricula_id):
    matricula_repository.deletar(matricula_id)
