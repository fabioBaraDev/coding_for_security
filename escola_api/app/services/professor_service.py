from app.repositories import professor_repository


def listar_professores():
    return professor_repository.listar()


def buscar_professor(professor_id):
    professor = professor_repository.buscar_por_id(professor_id)
    if not professor:
        raise ValueError("Professor nao encontrado")
    return professor


def criar_professor(dados):
    campos = ["nome", "email"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return professor_repository.criar(dados)


def atualizar_professor(professor_id, dados):
    professor_repository.buscar_por_id(professor_id)
    campos = ["nome", "email"]
    for campo in campos:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatorio: {campo}")
    return professor_repository.atualizar(professor_id, dados)


def deletar_professor(professor_id):
    professor_repository.deletar(professor_id)
