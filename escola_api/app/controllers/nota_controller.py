from flask import Blueprint, request, jsonify
from app.services import nota_service

nota_bp = Blueprint("notas", __name__)


@nota_bp.get("/")
def listar():
    notas = nota_service.listar_notas()
    return jsonify(notas)


@nota_bp.get("/<int:nota_id>")
def buscar(nota_id):
    try:
        nota = nota_service.buscar_nota(nota_id)
        return jsonify(nota)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@nota_bp.post("/")
def criar():
    try:
        nota = nota_service.criar_nota(request.json)
        return jsonify(nota), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@nota_bp.put("/<int:nota_id>")
def atualizar(nota_id):
    try:
        nota = nota_service.atualizar_nota(nota_id, request.json)
        return jsonify(nota)
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@nota_bp.delete("/<int:nota_id>")
def deletar(nota_id):
    nota_service.deletar_nota(nota_id)
    return "", 204
