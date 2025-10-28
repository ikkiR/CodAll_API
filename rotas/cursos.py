
from flask import Blueprint, jsonify, request
from extensoes import db, bcrypt, jwt
from models .model_usuarios import Usuarios, Alunos, Supervisor
from models .model_cursos import Cursos
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime


cursos_bp = Blueprint('cursos', __name__, url_prefix='/cursos')

@cursos_bp.route('/', methods=['GET'])
def registrar_curso():
    tipo_usuario = Usuarios.request.get_json().get('Tipo_usuario')
    dados = Cursos.request.get_json()
    titulo = dados.get('titulo')
    dificuldade =  dados.get('dificuldade')
    descricao = dados.get('descricao')
    logo_url = dados.get('logo_url')


    if tipo_usuario == 'supervisor':
        novo_curso = Cursos(titulo = titulo, dificuldade=dificuldade, descricao=descricao, logo_url=logo_url)
        db.session.add(novo_curso)
        db.session.commit()

        return({'mensagem': "Curso cadastrado com sucesso"})
    else:
        return({'mensagem': 'Usuário sem permissão!'})
    



