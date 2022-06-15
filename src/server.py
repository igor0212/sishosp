from util import Server
from allocate import Allocate

print('Aguardando conexão')
conn, ender = Server.create_server()

while True:
    #Recebendo dados do cliente
    data = conn.recv(1024)
    if not data or Server.close_connection(data):
        msg = 'Encerrando conexão'
        print(msg)
        Server.send_message(conn, msg)
        conn.close()
        break

    #Enviando informações para alocar paciente
    response = Allocate.allocate(data.decode())    

    #Enviando retorno para o cliente
    Server.send_message(conn, response)
    
