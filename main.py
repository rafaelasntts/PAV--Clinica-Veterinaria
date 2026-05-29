from database import engine 
from entities import * 

Base.metadata.create_all(bind=engine) 

print("Modelos carregados com sucesso!")