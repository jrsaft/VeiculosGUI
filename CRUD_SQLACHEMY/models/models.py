"""
Arquivo que contém as classes que representam os modelos do banco de dados.

Classes:
 - Usuario: Classe que representa a tabela 'usuarios' no banco de dados.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base para nossos modelos
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    idade = Column(Integer)

def __repr__(self):
    return f"<Usuario(nome='{self.nome}', idade={self.idade})>"