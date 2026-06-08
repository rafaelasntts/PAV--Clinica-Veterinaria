class Pessoa:
    def __init__(self, nome, telefone):
        self._nome = nome          
        self._telefone = telefone  

    @property
    def nome(self):
        return self._nome

    @property
    def telefone(self):
        return self._telefone

    def obter_documento_identificador(self):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")


class ClienteBusiness(Pessoa):
    def __init__(self, nome, cpf, telefone, endereco, email):
        super().__init__(nome, telefone)
        
        if len(cpf) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos.")
            
        self.__cpf = cpf
        self.endereco = endereco
        self.email = email

    @property
    def cpf(self):
        return self.__cpf

    def obter_documento_identificador(self):
        return f"CPF: {self.__cpf}"


class VeterinarioBusiness(Pessoa):
    def __init__(self, nome, crmv, especialidade, telefone):
        super().__init__(nome, telefone)
        self.__crmv = crmv 
        self.especialidade = especialidade

    @property
    def crmv(self):
        return self.__crmv

    def obter_documento_identificador(self):
        return f"CRMV: {self.__crmv}"