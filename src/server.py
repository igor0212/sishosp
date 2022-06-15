from util import Server
from allocate import Allocate

print('Aguardando conexão')
conn, ender = Server.create_server()

while True:
    
    #Recebendo mensagem do cliente
    message = Server.get_message(conn)
    if not message or Server.close_connection(message):
        error = 'Encerrando conexão'
        print(error)
        Server.send_message(conn, error)
        conn.close()
        break

    #Enviando informações para alocar paciente
    response = Allocate.allocate(message)    

    #Enviando retorno para o cliente
    Server.send_message(conn, response)
    
