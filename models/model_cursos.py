from extensoes import db



class Cursos(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Interger, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    dificuldade = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    logo_url = db.column(db.String(100), nullable= False)

    
    

#Função para retornar os dados do curso

def to_dict(self):
    return{"id": self.id, "titulo": self.titulo, "dificuldade": self.dificuldade, "descricao": self.descricao, "logo_url": self.logo_url }




