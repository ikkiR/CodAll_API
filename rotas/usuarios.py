
from flask import Blueprint, jsonify, request
from extensoes import db, bcrypt, jwt
from models .model_usuarios import Usuarios
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime


usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/', methods=['GET'])
# @jwt_required() #decorator que obriga o usuário ter um token valido para acessar essa rota
def listar_usuarios():
    # usuario_id = get_jwt_identity()
    usuarios = Usuarios.query.all() #faz o python listar todos os registros da tabela usuário que retorna uma lista de objetos python

    return jsonify([u.to_dict() for u in usuarios]) # list comprehension de para cada "u" em usuarios, aplico a função to_dict() para rotornar os dados em formato de dicionário python

    #o jsonify só pega isso e transforma em jason para poder ser lidos por rotas HTTP


@usuarios_bp.route('/', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json() #pegar o json da requisição
    email = dados.get('email')
    senha = dados.get('senha')
    nome=dados.get('nome')
    telefone = dados.get('telefone')
    cpf = dados.get('cpf')
    cep = dados.get('cep')
    endereco = dados.get('endereco')
    numero = dados.get('numero')
    complemento = dados.get('complemento')
    bairro = dados.get('bairro')
    cidade = dados.get('cidade')

    if Usuarios.query.filter_by(email=email).first(): #faz uma consulta para ver se existe um email no banco igual ao email 
        return jsonify({"erro": "email já cadastrado!"}), 400 #enviado, caso exista ele retorna o primeiro que encontrar
    
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8') #gera um hash para a senha enviada
    novo_usuario = Usuarios(nome=nome, email=email, telefone=telefone, cpf=cpf, cep=cep, endereco=endereco, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, senha=senha_hash) #os dados que serão enviados
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'Mensagem': 'Usuário Criado com sucesso!' }), 201


@usuarios_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email') #definindo oque será recebido pelo json
    senha = dados.get('senha')


    usuario = Usuarios.query.filter_by(email=email).first()
    if usuario and bcrypt.check_password_hash(usuario.senha, senha): #compara a senha enviada com a senha criptografada do banco
        token = create_access_token(identity=usuario.id, expires_delta=datetime.timedelta(hours=1))
        nome = usuario.nome
        id = usuario.id
        email = usuario.email
        #    gera um token de acesso/identifica o usuario dentro do token/define quanto tempo o token vai ser valido
        return jsonify({"token": token, "nome":nome, "id":id,"email":email})
    return jsonify({"erro": "Email ou senhas incorretos!"}), 401



# @app.route('/usuarios/<int:id>', methods=['PUT'])
# def atualizar_usuario(id):
#     usuario = Usuarios.query.get(id)
#     if not usuario:
#         return jsonify({"erro": "Usuário não encontrado!"}), 404


#     dados = request.get_json()
#     usuario.nome = dados.get('nome', usuario.nome)
#     usuario.curso = dados.get('curso', usuario.curso)
#     usuario.idade = dados.get('idade', usuario.idade)
#     db.session.commit()
#     return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 201


# @app.route('/usuarios/<int:id>', methods=['DELETE'])
# def deletar_usuario(id):
#    usuario = Usuarios.query.get(id)
#    if not usuario:
#        return jsonify({"erro": "Usuário não encontrado"}), 404
   
#    db.session.delete(usuario)
#    db.session.commit()
#    return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 201



# if __name__ == '__main__':
#     with app.app_context(): #quando rodar o app, Caso o banco não exista essa linha criará  um contexto de aplicação para o banco saber onde criar 
#         db.create_all()  #Cria o banco
#     app.run(host='0.0.0.0', port=5000, debug=True)