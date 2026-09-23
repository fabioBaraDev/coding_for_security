from flask import Blueprint, request, jsonify
from app.services import professor_service

professor_bp = Blueprint("professores", __name__)


@professor_bp.get("/")
def listar():
    professores = professor_service.listar_professores()
    return jsonify(professores)


@professor_bp.get("/<int:professor_id>")
def buscar(professor_id):
    try:
        professor = professor_service.buscar_professor(professor_id)
        return jsonify(professor)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@professor_bp.post("/")
def criar():
    try:
        professor = professor_service.criar_professor(request.json)
        return jsonify(professor), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@professor_bp.put("/<int:professor_id>")
def atualizar(professor_id):
    try:
        professor = professor_service.atualizar_professor(professor_id, request.json)
        return jsonify(professor)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@professor_bp.delete("/<int:professor_id>")
def deletar(professor_id):
    professor_service.deletar_professor(professor_id)
    return "", 204
