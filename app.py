from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import datetime



app = Flask(__name__)

#CONFIGURAÇÃO DO BANCO (MariaDB no XAMPP)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/codeall'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'a1047962b5dc7ae24409567ce9949c6f62ed60da70d8d010d0b488f2b717960b'       
                                                                 #essa é uma chave secreta que voçê mesmo pode criar. mas tambem
                                                                #pode pedir ao python digitando no terminal de python puro =
                                                                # import secrets print(secrets.token_hex(32)) 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #aqui ligamos as bibliotecas a este app 
jwt = JWTManager(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(100), nullable=False)
    cep = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer(), nullable=False)
    complemento = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)



    def to_dict(self):
        return{"id": self.id, "nome":self.nome,"email":self.email, "senha":self.senha}


@app.route('/usuarios', methods=['GET'])
# @jwt_required() #decorator que obriga o usuário ter um token valido para acessar essa rota
def listar_usuarios():
    # usuario_id = get_jwt_identity()
    usuarios = Usuarios.query.all() #faz o python listar todos os registros da tabela usuário que retorna uma lista de objetos python

    return jsonify([u.to_dict() for u in usuarios]) # list comprehension de para cada "u" em usuarios, aplico a função to_dict() para rotornar os dados em formato de dicionário python

    #o jsonify só pega isso e transforma em jason para poder ser lidos por rotas HTTP


@app.route('/usuarios', methods=['POST'])
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


@app.route('/login', methods=['POST'])
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



@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado!"}), 404


    dados = request.get_json()
    usuario.nome = dados.get('nome', usuario.nome)
    usuario.curso = dados.get('curso', usuario.curso)
    usuario.idade = dados.get('idade', usuario.idade)
    db.session.commit()
    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 201


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
   usuario = Usuarios.query.get(id)
   if not usuario:
       return jsonify({"erro": "Usuário não encontrado"}), 404
   
   db.session.delete(usuario)
   db.session.commit()
   return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 201



if __name__ == '__main__':
    with app.app_context(): #quando rodar o app, Caso o banco não exista essa linha criará  um contexto de aplicação para o banco saber onde criar 
        db.create_all()  #Cria o banco
    app.run(host='0.0.0.0', port=5000, debug=True)