from app.repositories import aluno_repository


def listar_alunos():
    return aluno_repository.listar()


def buscar_aluno(aluno_id):
    aluno = aluno_repository.buscar_por_id(aluno_id)
    if not aluno:
        raise ValueError("Aluno nao encontrado")
    return aluno


def criar_aluno(dados):
    campos = ["nome", "email", "cpf"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return aluno_repository.criar(dados)


def atualizar_aluno(aluno_id, dados):
    aluno_repository.buscar_por_id(aluno_id)
    campos = ["nome", "email", "cpf"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return aluno_repository.atualizar(aluno_id, dados)


def deletar_aluno(aluno_id):
    aluno_repository.deletar(aluno_id)
