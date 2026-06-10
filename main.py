# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import engine, SessionLocal
from models.entities import Base, Cliente, Animal, Veterinario, Consulta, Exame
from controllers.cliente_controller import ClienteController
from controllers.veterinario_controller import VeterinarioController
from controllers.animal_controller import AnimalController
from controllers.consulta_controller import ConsultaController
from controllers.exame_controller import ExameController
from datetime import datetime


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clínica Veterinária API Completa", version="1.0")


cliente_ctrl = ClienteController()
vet_ctrl = VeterinarioController()
animal_ctrl = AnimalController()
consulta_ctrl = ConsultaController()
exame_ctrl = ExameController()



class ClienteSchema(BaseModel):
    nome: str; cpf: str; telefone: str; endereco: str; email: str

class VeterinarioSchema(BaseModel):
    nome: str; crmv: str; especialidade: str; telefone: str

class AnimalSchema(BaseModel):
    nome: str; especie: str; raca: str; idade: int; sexo: str; id_cliente: int

class ConsultaSchema(BaseModel):
    data_str: str; hora_str: str; diagnostico: str; tratamento: str; id_animal: int; id_veterinario: int

class ExameSchema(BaseModel):
    nome: str; descricao: str; valor: float; id_consulta: int


@app.post("/clientes", tags=["Clientes"])
def cadastrar_cliente(dados: ClienteSchema):
    res = cliente_ctrl.cadastrar_cliente(dados.nome, dados.cpf, dados.telefone, dados.endereco, dados.email)
    if "Erro" in res: raise HTTPException(status_code=400, detail=res)
    return {"mensagem": res}

@app.get("/clientes", tags=["Clientes"])
def listar_clientes():
    session = SessionLocal()
    try:
        clientes = session.query(Cliente).all()
        return [{"id_cliente": c.id_cliente, "nome": c.nome, "cpf": c.cpf, "telefone": c.telefone, "email": c.email} for c in clientes]
    finally: session.close()

@app.put("/clientes/{id_cliente}", tags=["Clientes"])
def editar_cliente(id_cliente: int, dados: ClienteSchema):
    session = SessionLocal()
    try:
        c = session.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if not c: raise HTTPException(status_code=404, detail="Cliente não encontrado")
        c.nome=dados.nome; c.cpf=dados.cpf; c.telefone=dados.telefone; c.endereco=dados.endereco; c.email=dados.email
        session.commit()
        return {"mensagem": "Cliente atualizado com sucesso"}
    except Exception as e: session.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally: session.close()

@app.delete("/clientes/{id_cliente}", tags=["Clientes"])
def excluir_cliente(id_cliente: int):
    session = SessionLocal()
    try:
        c = session.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if not c: raise HTTPException(status_code=404, detail="Cliente não encontrado")
        session.delete(c); session.commit()
        return {"mensagem": "Cliente deletado com sucesso"}
    except Exception: raise HTTPException(status_code=400, detail="Erro ao deletar. Verifique se o cliente possui animais vinculados.")
    finally: session.close()



@app.post("/veterinarios", tags=["Veterinários"])
def cadastrar_veterinario(dados: VeterinarioSchema):
    res = vet_ctrl.cadastrar_veterinario(dados.nome, dados.crmv, dados.especialidade, dados.telefone)
    if "Erro" in res: raise HTTPException(status_code=400, detail=res)
    return {"mensagem": res}

@app.get("/veterinarios", tags=["Veterinários"])
def listar_veterinarios():
    session = SessionLocal()
    try:
        vets = session.query(Veterinario).all()
        return [{"id_veterinario": v.id_veterinario, "nome": v.nome, "crmv": v.crmv, "especialidade": v.especialidade} for v in vets]
    finally: session.close()

@app.put("/veterinarios/{id_veterinario}", tags=["Veterinários"])
def editar_veterinario(id_veterinario: int, dados: VeterinarioSchema):
    session = SessionLocal()
    try:
        v = session.query(Veterinario).filter(Veterinario.id_veterinario == id_veterinario).first()
        if not v: raise HTTPException(status_code=404, detail="Veterinário não encontrado")
        v.nome=dados.nome; v.crmv=dados.crmv; v.especialidade=dados.especialidade; v.telefone=dados.telefone
        session.commit()
        return {"mensagem": "Veterinário atualizado com sucesso"}
    except Exception as e: session.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally: session.close()

@app.delete("/veterinarios/{id_veterinario}", tags=["Veterinários"])
def excluir_veterinario(id_veterinario: int):
    session = SessionLocal()
    try:
        v = session.query(Veterinario).filter(Veterinario.id_veterinario == id_veterinario).first()
        if not v: raise HTTPException(status_code=404, detail="Veterinário não encontrado")
        session.delete(v); session.commit()
        return {"mensagem": "Veterinário deletado com sucesso"}
    except Exception: raise HTTPException(status_code=400, detail="Erro ao deletar. Verifique se o veterinário possui consultas vinculadas.")
    finally: session.close()



@app.post("/animais", tags=["Animais"])
def cadastrar_animal(dados: AnimalSchema):
    res = animal_ctrl.cadastrar_animal(dados.nome, dados.especie, dados.raca, dados.idade, dados.sexo, dados.id_cliente)
    if "Erro" in res: raise HTTPException(status_code=400, detail=res)
    return {"mensagem": res}

@app.get("/animais", tags=["Animais"])
def listar_animais():
    session = SessionLocal()
    try:
        animais = session.query(Animal).all()
        return [{"id_animal": a.id_animal, "nome": a.nome, "especie": a.especie, "raca": a.raca, "idade": a.idade, "sexo": a.sexo, "id_cliente": a.id_cliente} for a in animais]
    finally: session.close()

@app.put("/animais/{id_animal}", tags=["Animais"])
def editar_animal(id_animal: int, dados: AnimalSchema):
    session = SessionLocal()
    try:
        a = session.query(Animal).filter(Animal.id_animal == id_animal).first()
        if not a: raise HTTPException(status_code=404, detail="Animal não encontrado")
        a.nome=dados.nome; a.especie=dados.especie; a.raca=dados.raca; a.idade=dados.idade; a.sexo=dados.sexo; a.id_cliente=dados.id_cliente
        session.commit()
        return {"mensagem": "Animal atualizado com sucesso"}
    except Exception as e: session.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally: session.close()

@app.delete("/animais/{id_animal}", tags=["Animais"])
def excluir_animal(id_animal: int):
    session = SessionLocal()
    try:
        a = session.query(Animal).filter(Animal.id_animal == id_animal).first()
        if not a: raise HTTPException(status_code=404, detail="Animal não encontrado")
        session.delete(a); session.commit()
        return {"mensagem": "Animal deletado com sucesso"}
    except Exception: raise HTTPException(status_code=400, detail="Erro ao deletar. Verifique se o animal possui consultas vinculadas.")
    finally: session.close()



@app.post("/consultas", tags=["Consultas"])
def agendar_consulta(dados: ConsultaSchema):
    res = consulta_ctrl.agendar_consulta(dados.data_str, dados.hora_str, dados.diagnostico, dados.tratamento, dados.id_animal, dados.id_veterinario)
    if "Erro" in res: raise HTTPException(status_code=400, detail=res)
    return {"mensagem": res}

@app.get("/consultas", tags=["Consultas"])
def listar_consultas():
    session = SessionLocal()
    try:
        consultas = session.query(Consulta).all()
        return [{"id_consulta": c.id_consulta, "data": str(c.data), "hora": str(c.hora), "diagnostico": c.diagnostico, "tratamento": c.tratamento, "id_animal": c.id_animal, "id_veterinario": c.id_veterinario} for c in consultas]
    finally: session.close()

@app.put("/consultas/{id_consulta}", tags=["Consultas"])
def editar_consulta(id_consulta: int, dados: ConsultaSchema):
    session = SessionLocal()
    try:
        c = session.query(Consulta).filter(Consulta.id_consulta == id_consulta).first()
        if not c: raise HTTPException(status_code=404, detail="Consulta não encontrada")
        c.data = datetime.strptime(dados.data_str, "%d/%m/%Y").date()
        c.hora = datetime.strptime(dados.hora_str, "%H:%M").time()
        c.diagnostico = dados.diagnostico; c.tratamento = dados.tratamento; c.id_animal = dados.id_animal; c.id_veterinario = dados.id_veterinario
        session.commit()
        return {"mensagem": "Consulta atualizada com sucesso"}
    except Exception as e: session.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally: session.close()

@app.delete("/consultas/{id_consulta}", tags=["Consultas"])
def excluir_consulta(id_consulta: int):
    session = SessionLocal()
    try:
        c = session.query(Consulta).filter(Consulta.id_consulta == id_consulta).first()
        if not c: raise HTTPException(status_code=404, detail="Consulta não encontrada")
        session.delete(c); session.commit()
        return {"mensagem": "Consulta deletada com sucesso"}
    except Exception: raise HTTPException(status_code=400, detail="Erro ao deletar. Verifique se a consulta possui exames vinculados.")
    finally: session.close()



@app.post("/exames", tags=["Exames"])
def cadastrar_exame(dados: ExameSchema):
    res = excuse = exame_ctrl.cadastrar_exame(dados.nome, dados.descricao, dados.valor, dados.id_consulta)
    if "Erro" in res: raise HTTPException(status_code=400, detail=res)
    return {"mensagem": res}

@app.get("/exames", tags=["Exames"])
def listar_exames():
    session = SessionLocal()
    try:
        exames = session.query(Exame).all()
        return [{"id_exame": e.id_exame, "nome": e.nome, "descricao": e.descricao, "valor": float(e.valor), "id_consulta": e.id_consulta} for e in exames]
    finally: session.close()

@app.put("/exames/{id_exame}", tags=["Exames"])
def editar_exame(id_exame: int, dados: ExameSchema):
    session = SessionLocal()
    try:
        e = session.query(Exame).filter(Exame.id_exame == id_exame).first()
        if not e: raise HTTPException(status_code=404, detail="Exame não encontrado")
        e.nome=dados.nome; e.descricao=dados.descricao; e.valor=dados.valor; e.id_consulta=dados.id_consulta
        session.commit()
        return {"mensagem": "Exame atualizado com sucesso"}
    except Exception as e: session.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally: session.close()

@app.delete("/exames/{id_exame}", tags=["Exames"])
def excluir_exame(id_exame: int):
    session = SessionLocal()
    try:
        e = session.query(Exame).filter(Exame.id_exame == id_exame).first()
        if not e: raise HTTPException(status_code=404, detail="Exame não encontrado")
        session.delete(e); session.commit()
        return {"mensagem": "Exame deletado com sucesso"}
    except Exception as error: session.rollback(); raise HTTPException(status_code=400, detail=str(error))
    finally: session.close()