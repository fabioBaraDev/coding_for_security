from app.repositories import nota_repository


def listar_notas():
    return nota_repository.listar()


def buscar_nota(nota_id):
    nota = nota_repository.buscar_por_id(nota_id)
    if not nota:
        raise ValueError("Nota nao encontrada")
    return nota


def criar_nota(dados):
    campos = ["matricula_id", "valor"]
    for campo in campos:
        if dados.get(campo) is None:
            raise ValueError(f"Campo obrigatorio: {campo}")
    valor = float(dados["valor"])
    if valor < 0 or valor > 10:
        raise ValueError("Nota deve ser entre 0 e 10")
    return nota_repository.criar(dados)


def atualizar_nota(nota_id, dados):
    nota_repository.buscar_por_id(nota_id)
    campos = ["matricula_id", "valor"]
    for campo in campos:
        if dados.get(campo) is None:
            raise ValueError(f"Campo obrigatorio: {campo}")
    valor = float(dados["valor"])
    if valor < 0 or valor > 10:
        raise ValueError("Nota deve ser entre 0 e 10")
    return nota_repository.atualizar(nota_id, dados)


def deletar_nota(nota_id):
    nota_repository.deletar(nota_id)
