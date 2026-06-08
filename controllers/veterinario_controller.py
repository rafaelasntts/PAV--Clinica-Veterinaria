
from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Veterinario  # Tabela do banco
from models.business import VeterinarioBusiness  # Regras OO (como CRF/CRMV)

Session = sessionmaker(bind=engine)

class VeterinarioController:
    def __init__(self):
        self.session = Session()

    def cadastrar_veterinario(self, nome, crmv, especialidade, telefone):
        try:
            # 1. Instancia a regra de negócio (aplica validações se houver)
            vet_valido = VeterinarioBusiness(nome, crmv, especialidade, telefone)
            
            # 2. Transfere para a entidade que o SQLAlchemy joga no banco
            novo_vet = Veterinario(
                nome=vet_valido.nome,
                crmv=vet_valido.crmv,
                especialidade=vet_valido.especialidade,
                telefone=vet_valido.telefone
            )
            
            # 3. Salva no MySQL do XAMPP
            self.session.add(novo_vet)
            self.session.commit()
            return f"Sucesso: Veterinário(a) Dr(a). {vet_valido.nome} cadastrado com sucesso!"
            
        except ValueError as ve:
            return f"Erro de Validação: {ve}"
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()