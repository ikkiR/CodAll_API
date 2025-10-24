
from flask import Blueprint, jsonify, request
from extensoes import db, bcrypt, jwt
from models .model_usuarios import Usuarios, Alunos, Supervisor
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime


usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/<int:id>', methods=['GET'])
@jwt_required() #decorator que obriga o usuário ter um token valido para acessar essa rota
def listar_usuario(id):
    usuario_id = get_jwt_identity()
    usuario = Usuarios.query.get(id) #retorna o objeto usuario. um objeto NÃO É ITERAVEL

    return jsonify(usuario.to_dict()), 200 # PARA RETORNAR OS DADOS, TRANSFORMAMOS O OBJETO SQL EM UM DICIONÁRIO QUE É ITERAVEL


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
    tipo_usuario = dados.get ('tipo_usuario')

    if Usuarios.query.filter_by(nome=nome).first():
        return jsonify({"erro": "Nome de usuário já existe!"}), 400

    if Usuarios.query.filter_by(email=email).first(): #faz uma consulta para ver se existe um email no banco igual ao email 
        return jsonify({"erro": "email já cadastrado!"}), 400 #enviado, caso exista ele retorna o primeiro que encontrar
    
    senha_hash = bcrypt.generate_password_hash(senha).decode('utf-8') #gera um hash para a senha enviada
    novo_usuario = Usuarios(nome=nome, email=email, telefone=telefone, cpf=cpf, cep=cep, endereco=endereco, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, senha=senha_hash, tipo_usuario=tipo_usuario) #os dados que serão enviados
    db.session.add(novo_usuario)
    db.session.commit()
    
    # utilizando comparação para criar tabelas de acessos diferentes para usuarios diferentes
    if tipo_usuario == 'aluno':
        novo_aluno = Alunos(usuario_id = novo_usuario.id)
        db.session.add(novo_aluno)
    
    if tipo_usuario == 'supervisor':
        matricula = dados.get('matricula')
        novo_supervisor = Supervisor(usuario_id = novo_usuario.id, matricula = matricula)
    
        db.session.add(novo_supervisor)

    db.session.commit()


    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 202


@usuarios_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    login = dados.get('login') #definindo oque será recebido pelo json
    senha = dados.get('senha')

    if not login or not senha:
        return jsonify({'message': 'O campo login e senha são obrigatórios!'})

    # condição para usuário poder usar email e senha no login
    if '@' in login:
        usuario = Usuarios.query.filter_by(email=login).first()
    else:
        usuario = Usuarios.query.filter_by(nome=login).first()

    if usuario and bcrypt.check_password_hash(usuario.senha, senha): #compara a senha enviada com a senha criptografada do banco
        token = create_access_token(identity={
            "id": usuario.id,
            "nome": usuario.nome,
            "tipo_usuario": usuario.tipo_usuario
        },expires_delta=datetime.timedelta(hours=1)) #aqui criamos um token - um token armazena os dados do usuário de forma codificada. podemos escolher quais informações do usuario o token guarda.
        #    gera um token de acesso/identifica o usuario dentro do token/define quanto tempo o token vai ser valido
        return jsonify({"token": token,})
    return jsonify({"erro": "Email ou senhas incorretos!"}), 401


@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    usuario_id = get_jwt_identity() #pega os dados do usuário direto do token
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado!"}), 404


    dados = request.get_json()
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.email = dados.get('email', usuario.email)
    usuario.telefone = dados.get('telefone', usuario.telefone)
    usuario.cep = dados.get('cep', usuario.cep)
    usuario.endereco = dados.get('endereco', usuario.endereco)
    usuario.numero = dados.get('numero', usuario.numero)
    usuario.complemento = dados.get('complemento', usuario.complemento)
    usuario.bairro = dados.get('bairro', usuario.bairro)
    usuario.cidade = dados.get('cidade', usuario.cidade)
    

    senha_atual = dados.get("senha_atual")
    nova_senha = dados.get("nova_senha")


    if nova_senha and not senha_atual:   #verifica se a nova senha foi enviada mas a senha atual nao
        return jsonify({'message': 'você precisa digitar a senha antiga antes de altera-la'}),400


    if senha_atual and nova_senha:
        if usuario and bcrypt.check_password_hash(usuario.senha, senha_atual): # os parâmetros do check_password_hash(senha_banco, senha_digitada)
            usuario.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
        else:
             return jsonify({'message': 'A senha esta incorreta'})

    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 201


@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    usuario_id = get_jwt_identity()
    usuario= Usuarios.query.get(id)

    dados = request.get_json()
    senha = dados.get('senha')


    supervisor = Supervisor.query.filter_by(usuario_id = usuario.id).first() #ligando a variavel a tabela supervisor e especificando a chave estrangeira

    aluno = Alunos.query.filter_by(usuario_id = usuario.id).first()


    #agora podemos excluir os filhos da tabela usuário
    if supervisor:
        db.session.delete(supervisor)
    
    if aluno:
        db.session.delete(aluno)
    

    if usuario and bcrypt.check_password_hash(usuario.senha, senha):
        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 201
    
    else:
        return jsonify({"mensagem": "senha incorreta"}), 400



