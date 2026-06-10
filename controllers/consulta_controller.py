from database import engine
from sqlalchemy.orm import sessionmaker
from models.entities import Consulta
from datetime import datetime

Session = sessionmaker(bind=engine)

class ConsultaController:
    def __init__(self):
        self.session = Session()

    def agendar_consulta(self, data_str, hora_str, diagnostico, tratamento, id_animal, id_veterinario):
        try:
            data_valida = datetime.strptime(data_str, "%d/%m/%Y").date()
            hora_valida = datetime.strptime(hora_str, "%H:%M").time()
            
            nova_consulta = Consulta(
                data=data_valida,
                hora=hora_valida,
                diagnostico=diagnostico,
                tratamento=tratamento,
                id_animal=id_animal,            
                id_veterinario=id_veterinario    
            )
            
            self.session.add(nova_consulta)
            self.session.commit()
            return f"Sucesso: Consulta agendada para o dia {data_str} às {hora_str}!"
            
        except ValueError as ve:
            return f"Erro de Formato: {ve}. Use DD/MM/AAAA para data e HH:MM para hora."
        except Exception as e:
            self.session.rollback()
            return f"Erro no Banco de Dados: {e}"
        finally:
            self.session.close()