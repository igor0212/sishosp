from socket import *
from util import Client

client = Client.create_client()
message = ''

while True:       

    #Enviando mensagem para o servidor
    message = input("Digite: ")
    client.send(message.encode())

    #Recebendo resposta do servidor
    data = client.recv(1024)
    print(data.decode())

    #Encerrando conexão
    if(Client.close_connection(message)):
        break
