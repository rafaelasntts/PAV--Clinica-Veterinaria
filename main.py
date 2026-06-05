from database import engine 
from models.entities import Base 


Base.metadata.create_all(bind=engine) 

print("Modelos carregados com sucesso!")