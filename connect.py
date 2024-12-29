import mysql.connector, time

def connect():
    return mysql.connector.connect(
        host='',
        user='',
        password='',
        database='',
        port=''
    )

def reconectar(conexao, cursor):
    # Verifica se a conexão ainda está ativa
    if conexao is None or not conexao.is_connected():
        while True:
            try:
                print("Reconectando ao banco...")
                conexao = connect()
                cursor = conexao.cursor()
                break
            except:
                print("Erro de banco, espere alguns segundos para normalizar")
                time.sleep(10)
    return conexao, cursor