from socket import *
from util import Client

client = Client.create_client()

while True:       

    #Enviando mensagem para o servidor
    patient_arrival_interval = input("Digite o intervalo de chegada dos pacientes: ")
    qt_doctors = input("Digite a quantidade de médicos: ")
    qt_nurses = input("Digite a quantidade de enfermeiros: ")
    simulation_time = input("Digite o tempo de simulação: ")

    message = '%s %s %s %s' % (patient_arrival_interval, qt_doctors, qt_nurses, simulation_time)       

    #Validando se mensagem é válida
    if(not Client.validate_message(message)):
        print("Entrada inválida \n")
        continue

    #Enviando mensagem
    Client.send_message(client, message)

    #Recebendo resposta do servidor
    response = Client.get_message(client)
    print(response + '\n')    
