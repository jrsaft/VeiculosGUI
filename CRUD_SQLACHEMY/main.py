from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.models import Usuario

# Base para nossos modelos
Base = declarative_base()

# Conectar ao banco
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

def criar_usuario(nome: str, idade: int) -> Usuario:
    # Criar novo usuário
    novo_usuario = Usuario(nome="João Silva", idade=25)
    # Adicionar à sessão
    session.add(novo_usuario)
    # Salvar no banco
    session.commit()
    return novo_usuario

if __name__ == 'main':
    print("Meu primeiro banco de dados!")

    novo_usuario = criar_usuario(nome="Tiago", idade=18)
    print(novo_usuario)

def buscar_todos_usuarios() -> list[usuario]:
    try:
        usuarios = session.query(usuario).all()
    except Exception as e:
        print(e)
        usuarios = []
    return usuarios

def buscar_usuarios_por_nome() -> list[usuario]:
    try:
        usuarios = session.query(usuario).filter_by(nome=nome).all()
    except Exception as e: #o "e" é para definir qual foi o erro e mostrar ele no print.
        print(e)
        usuarios = []
    return usuarios
