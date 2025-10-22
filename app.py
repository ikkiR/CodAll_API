from flask import Flask
from extensoes import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    # Configuração do banco (MariaDB no XAMPP)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/codeall'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'a1047962b5dc7ae24409567ce9949c6f62ed60da70d8d010d0b488f2b717960b'

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importa e registra as rotas (depois você cria o arquivo routes)
    from rotas import regitrar_rotas
    regitrar_rotas(app)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)