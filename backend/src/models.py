from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    max_pessoas = db.Column(db.Integer)
    pessoas = db.relationship('Pessoa', back_populates='grupo')
    despesas = db.relationship('Despesa', back_populates='grupo')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'max_pessoas': self.max_pessoas,
            'qtd_pessoas': len(self.pessoas),
            'qtd_despesas': len(self.despesas)
        }


class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    grupo = db.relationship('Grupo', back_populates='pessoas')
    despesas_pagas = db.relationship('Despesa', back_populates='pagador')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'grupo_id': self.grupo_id
        }


class Despesa(db.Model):
    __tablename__ = 'despesas'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(50))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    pagador_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    
    grupo = db.relationship('Grupo', back_populates='despesas')
    pagador = db.relationship('Pessoa', back_populates='despesas_pagas')

    __mapper_args__ = {
        'polymorphic_identity': 'despesa',
        'polymorphic_on': tipo
    }


class Compra(Despesa):
    __tablename__ = 'compras'

    id = db.Column(db.Integer, db.ForeignKey('despesas.id'), primary_key=True)
    nome_mercado = db.Column(db.String(100))
    itens = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity': 'compra',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'data': self.data.isoformat(),
            'tipo': 'compra',
            'grupo_id': self.grupo_id,
            'pagador_id': self.pagador_id,
            'nome_mercado': self.nome_mercado,
            'itens': self.itens
        }


class Imovel(Despesa):
    __tablename__ = 'imoveis'

    id = db.Column(db.Integer, db.ForeignKey('despesas.id'), primary_key=True)
    endereco = db.Column(db.String(200))

    __mapper_args__ = {
        'polymorphic_identity': 'imovel',
    }

    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'data': self.data.isoformat(),
            'tipo': 'imovel',
            'grupo_id': self.grupo_id,
            'pagador_id': self.pagador_id,
            'endereco': self.endereco
        }
