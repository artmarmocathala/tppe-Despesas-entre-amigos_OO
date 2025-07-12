from database import db 

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    grupo_id = db.Column(
        db.Integer, db.ForeignKey('grupos.id'), nullable=False
    )
    grupo = db.relationship('Grupo', back_populates='pessoas')
    despesas_pagas = db.relationship('Despesa', back_populates='pagador')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'grupo_id': self.grupo_id
        }