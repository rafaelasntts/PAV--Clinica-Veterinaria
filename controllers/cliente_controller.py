
from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Cliente  # Tabela do banco
from models.business import ClienteBusiness  # Regras OO com validação

# Criamos a sessão para conversar com o MySQL
Session = sessionmaker(bind=engine)

class ClienteController:
    def __init__(self):
        self.session = Session()

    def cadastrar_cliente(self, nome, cpf, telefone, endereco, email):
        try:
            # 1. Instancia a classe de Regra de Negócio (Gera erro se o CPF não tiver 11 dígitos)
            cliente_valido = ClienteBusiness(nome, cpf, telefone, endereco, email)
            
            # 2. Se a validação passou, transferimos os dados para a Entidade do Banco
            novo_cliente = Cliente(
                nome=cliente_valido.nome,
                cpf=cliente_valido.cpf,
                telefone=cliente_valido.telefone,
                endereco=cliente_valido.endereco,
                email=cliente_valido.email
            )
            
            # 3. Salva de verdade no banco de dados do XAMPP
            self.session.add(novo_cliente)
            self.session.commit()
            return f"Sucesso: Cliente {cliente_valido.nome} cadastrado perfeitamente!"
            
        except ValueError as ve:
            # Captura o erro de validação do CPF
            return f"Erro de Validação: {ve}"
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()