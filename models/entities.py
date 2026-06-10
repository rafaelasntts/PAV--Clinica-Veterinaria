from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Date, Time
from sqlalchemy.orm import relationship
from database import Base


class Cliente(Base):
    __tablename__ = "Cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    telefone = Column(String(14), nullable=False)
    endereco = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)

    animais = relationship("Animal", back_populates="cliente")


class Animal(Base):
    __tablename__ = "Animal"

    id_animal = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    especie = Column(String(20), nullable=False)
    raca = Column(String(30), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String(10), nullable=False)

    id_cliente = Column(Integer, ForeignKey("Cliente.id_cliente"))

    cliente = relationship("Cliente", back_populates="animais")
    consultas = relationship("Consulta", back_populates="animal")


class Veterinario(Base):
    __tablename__ = "Veterinario"

    id_veterinario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    crmv = Column(String(11), nullable=False)
    especialidade = Column(String(70), nullable=False)
    telefone = Column(String(15), nullable=False)

    consultas = relationship("Consulta", back_populates="veterinario")


class Consulta(Base):
    __tablename__ = "Consulta"

    id_consulta = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    diagnostico = Column(Text, nullable=False)
    tratamento = Column(Text, nullable=False)

    id_animal = Column(Integer, ForeignKey("Animal.id_animal"))
    id_veterinario = Column(Integer, ForeignKey("Veterinario.id_veterinario"))

    animal = relationship("Animal", back_populates="consultas")
    veterinario = relationship("Veterinario", back_populates="consultas")
    exames = relationship("Exame", back_populates="consulta")


class Exame(Base):
    __tablename__ = "Exame"

    id_exame = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)

    id_consulta = Column(Integer, ForeignKey("Consulta.id_consulta"))

    consulta = relationship("Consulta", back_populates="exames")
