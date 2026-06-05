# teste.py
from controllers.cliente_controller import ClienteController

controller = ClienteController()

print("--- TESTANDO CADASTRO DE CLIENTE ---")
# Tentando cadastrar um cliente com os dados certinhos
resultado = controller.cadastrar_cliente(
    nome="Eshley Silva",
    cpf="12345678901",  # exatamente 11 números
    telefone="21999999999",
    endereco="Rua da Faculdade, 123",
    email= "eshley@email.com"
)

print(resultado)