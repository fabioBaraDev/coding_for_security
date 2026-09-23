from flask import Blueprint, request, jsonify
from app.services import curso_service

curso_bp = Blueprint("cursos", __name__)


@curso_bp.get("/")
def listar():
    cursos = curso_service.listar_cursos()
    return jsonify(cursos)


@curso_bp.get("/<int:curso_id>")
def buscar(curso_id):
    try:
        curso = curso_service.buscar_curso(curso_id)
        return jsonify(curso)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@curso_bp.post("/")
def criar():
    try:
        curso = curso_service.criar_curso(request.json)
        return jsonify(curso), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@curso_bp.put("/<int:curso_id>")
def atualizar(curso_id):
    try:
        curso = curso_service.atualizar_curso(curso_id, request.json)
        return jsonify(curso)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@curso_bp.delete("/<int:curso_id>")
def deletar(curso_id):
    curso_service.deletar_curso(curso_id)
    return "", 204
