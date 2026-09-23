from flask import Blueprint, request, jsonify
from app.services import aluno_service

aluno_bp = Blueprint("alunos", __name__)


@aluno_bp.get("/")
def listar():
    alunos = aluno_service.listar_alunos()
    return jsonify(alunos)


@aluno_bp.get("/<int:aluno_id>")
def buscar(aluno_id):
    try:
        aluno = aluno_service.buscar_aluno(aluno_id)
        return jsonify(aluno)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@aluno_bp.post("/")
def criar():
    try:
        aluno = aluno_service.criar_aluno(request.json)
        return jsonify(aluno), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@aluno_bp.put("/<int:aluno_id>")
def atualizar(aluno_id):
    try:
        aluno = aluno_service.atualizar_aluno(aluno_id, request.json)
        return jsonify(aluno)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@aluno_bp.delete("/<int:aluno_id>")
def deletar(aluno_id):
    aluno_service.deletar_aluno(aluno_id)
    return "", 204
