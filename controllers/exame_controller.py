from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Exame

Session = sessionmaker(bind=engine)

class ExameController:
    def __init__(self):
        self.session = Session()

    def cadastrar_exame(self, nome, descricao, valor, id_consulta):
        try:
            novo_exame = Exame(
                nome=nome,
                descricao=descricao,
                valor=valor,              
                id_consulta=id_consulta   
            )
            
            self.session.add(novo_exame)
            self.session.commit()
            return f"Sucesso: Exame '{nome}' registrado e vinculado à consulta com sucesso!"
            
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()