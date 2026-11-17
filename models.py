from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Familia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responsavel = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    atendimentos = db.relationship("Atendimento", backref="familia", lazy=True,
                                   order_by="Atendimento.data.desc()")


class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    familia_id = db.Column(db.Integer, db.ForeignKey("familia.id"), nullable=False)
