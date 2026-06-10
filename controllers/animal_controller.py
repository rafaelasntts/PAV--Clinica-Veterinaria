from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Animal  

Session = sessionmaker(bind=engine)

class AnimalController:
    def __init__(self):
        self.session = Session()

    def cadastrar_animal(self, nome, especie, raca, idade, sexo, id_cliente):
        try:
            novo_animal = Animal(
                nome=nome,
                especie=especie,
                raca=raca,
                idade=idade,
                sexo=sexo,
                id_cliente=id_cliente
            )
            
            self.session.add(novo_animal)
            self.session.commit()
            return f"Sucesso: O pet {nome} foi cadastrado e vinculado ao dono com sucesso!"
            
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()