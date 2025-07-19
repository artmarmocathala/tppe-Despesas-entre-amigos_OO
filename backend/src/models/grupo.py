from database import db
from sqlalchemy.ext.hybrid import hybrid_property

class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    max_pessoas = db.Column(db.Integer)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey('usuarios.id'), nullable=True
    )
    usuario = db.relationship('Usuario', back_populates='grupos')
    pessoas = db.relationship('Pessoa', back_populates='grupo')
    despesas = db.relationship('Despesa', back_populates='grupo')
    
    @hybrid_property
    def total_despesas(self):
        return sum(d.valor for d in self.despesas)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'max_pessoas': self.max_pessoas,
            'usuario_id': self.usuario_id,
            'qtd_pessoas': len(self.pessoas),
            'qtd_despesas': len(self.despesas),
            'total_despesas': self.total_despesas
        }

    def dividir_despesas(self):
        total_despesas = self.total_despesas
        qtd_pessoas = len(self.pessoas)
        if qtd_pessoas == 0:
            return {
                'error': 'Nenhuma pessoa no grupo para dividir as despesas'
            }
        valor_por_pessoa = total_despesas / qtd_pessoas
        return {
            'total_despesas': total_despesas,
            'valor_por_pessoa': valor_por_pessoa,
            'qtd_pessoas': qtd_pessoas
        }