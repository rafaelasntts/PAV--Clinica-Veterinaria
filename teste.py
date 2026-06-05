from database import engine

try:
    conn = engine.connect()
    print("Conectado com sucesso!")
    conn.close()
except Exception as e:
    print("Erro:")
    print(e)