from extensoes import db




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