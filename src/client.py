from socket import *
from util import Client

client = Client.create_client()

while True:       

    #Enviando mensagem para o servidor
    message = input("Digite o nome do paciente e a sua gravidade (1 - LEVE, 2 - MODERADO, 3 - GRAVE OU 4 - GRAVÍSSIMO): ")

    #Validando se mensagem é válida
    if(not Client.validate_message(message)):
        print("Entrada inválida \n")
        continue

    #Enviando mensagem
    Client.send_message(client, message)

    #Recebendo resposta do servidor
    response = Client.get_message(client)
    print(response + '\n')

    #Encerrando conexão
    if(Client.close_connection(message)):
        break
