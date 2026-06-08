from controllers.animal_controller import AnimalController
from controllers.consulta_controller import ConsultaController
from controllers.exame_controller import ExameController

animal_ctrl = AnimalController()
consulta_ctrl = ConsultaController()
exame_ctrl = ExameController()

print("--- 1. CADASTRANDO ANIMAL ---")
res_animal = animal_ctrl.cadastrar_animal(
    nome="Lutor", especie="Cachorro", raca="viralata", idade=3, sexo="Macho", id_cliente=1
)
print(res_animal)

print("\n--- 2. AGENDANDO CONSULTA ---")
res_consulta = consulta_ctrl.agendar_consulta(
    data_str="15/06/2026",
    hora_str="14:30",
    diagnostico="Suspeita de virose",
    tratamento="Pedir exames de sangue",
    id_animal=1,
    id_veterinario=1
)
print(res_consulta)

print("\n--- 3. REGISTRANDO EXAME PARA A CONSULTA ---")
# Vinculamos o exame ao id_consulta=1 que foi gerado no passo anterior
res_exame = exame_ctrl.cadastrar_exame(
    nome="Hemograma Completo",
    descricao="Contagem de plaquetas e hemácias para verificar infecção",
    valor=85.50,
    id_consulta=1
)
print(res_exame)