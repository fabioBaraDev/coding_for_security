from flask import Blueprint, request, jsonify
from app.services import matricula_service

matricula_bp = Blueprint("matriculas", __name__)


@matricula_bp.get("/")
def listar():
    matriculas = matricula_service.listar_matriculas()
    return jsonify(matriculas)


@matricula_bp.get("/<int:matricula_id>")
def buscar(matricula_id):
    try:
        matricula = matricula_service.buscar_matricula(matricula_id)
        return jsonify(matricula)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@matricula_bp.post("/")
def criar():
    try:
        matricula = matricula_service.criar_matricula(request.json)
        return jsonify(matricula), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@matricula_bp.put("/<int:matricula_id>")
def atualizar(matricula_id):
    try:
        matricula = matricula_service.atualizar_matricula(matricula_id, request.json)
        return jsonify(matricula)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@matricula_bp.delete("/<int:matricula_id>")
def deletar(matricula_id):
    matricula_service.deletar_matricula(matricula_id)
    return "", 204
