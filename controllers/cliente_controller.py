
from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Cliente 
from models.business import ClienteBusiness 


Session = sessionmaker(bind=engine)

class ClienteController:
    def __init__(self):
        self.session = Session()

    def cadastrar_cliente(self, nome, cpf, telefone, endereco, email):
        try:
            
            cliente_valido = ClienteBusiness(nome, cpf, telefone, endereco, email)
            
            
            novo_cliente = Cliente(
                nome=cliente_valido.nome,
                cpf=cliente_valido.cpf,
                telefone=cliente_valido.telefone,
                endereco=cliente_valido.endereco,
                email=cliente_valido.email
            )
            
            
            self.session.add(novo_cliente)
            self.session.commit()
            return f"Sucesso: Cliente {cliente_valido.nome} cadastrado perfeitamente!"
            
        except ValueError as ve:
           
            return f"Erro de Validação: {ve}"
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()