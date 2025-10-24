from extensoes import db
from sqlalchemy import CheckConstraint




class Usuarios(db.Model):

    __tablename__= 'usuarios'
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
    tipo_usuario = db.Column(db.String(20), nullable=False)

    aluno = db.relationship('Alunos', backref='usuario', uselist=False)
    professor = db.relationship('Supervisor', backref='usuario', uselist=False)

   # isto serve para definir os valores que pode ser aceitos no campo tipo_usuario
    __table_args__ = (  
         CheckConstraint("tipo_usuario IN ('aluno', 'supervisor')", name='check_tipo_usuario'),
    )
    
 
    # função que retorna os dados
    def to_dict(self):
        return{"id": self.id, "nome":self.nome, "email":self.email, "telefone":self.telefone, "cpf": self.cpf, "cep": self.cep, "endereco": self.endereco, "numero": self.endereco, "complemento": self.complemento, "bairro": self.bairro , "cidade": self.cidade, "tipo_usuario": self.tipo_usuario}
    

class Alunos (db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer,primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) #Foreignkey que liga a tabela alunos a usuários




class Supervisor (db.Model):
    __tablename__= 'supervisor'
    id = db.Column(db.Integer,primary_key = True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    matricula = db.Column(db.String(10), nullable= False)

    