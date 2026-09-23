from flask import Flask
from app.controllers.aluno_controller import aluno_bp
from app.controllers.professor_controller import professor_bp
from app.controllers.curso_controller import curso_bp
from app.controllers.matricula_controller import matricula_bp
from app.controllers.nota_controller import nota_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(aluno_bp, url_prefix="/alunos")
    app.register_blueprint(professor_bp, url_prefix="/professores")
    app.register_blueprint(curso_bp, url_prefix="/cursos")
    app.register_blueprint(matricula_bp, url_prefix="/matriculas")
    app.register_blueprint(nota_bp, url_prefix="/notas")

    @app.get("/")
    def health():
        return {"status": "ok", "app": "escola-api"}

    return app


app = create_app()
