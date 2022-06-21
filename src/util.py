from socket import *

HOST = gethostname()
PORT = 50000
DATA_SIZE = 1024

class Util:
    
    PATIENT_STATE_PT_BR = {1: 'Leve', 2:'Moderado', 3: 'Grave', 4: 'Gravissimo' }

    TREATMENT_TIME = {'Leve': 3, 'Moderado':6, 'Grave': 9, 'Gravissimo': 12 }

    def get_environment_informations(message):
        list = message.split()
        patient_arrival_interval = int(list[0])
        qt_doctors = int(list[1])
        qt_nurses = int(list[2])
        simulation_time = int(list[3])
        return patient_arrival_interval, qt_doctors, qt_nurses, simulation_time

class Client:        

    def create_client():
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((HOST, PORT))
        return client

    def send_message(client, message):
        client.send(message.encode())
    
    def get_message(client):
        return client.recv(DATA_SIZE).decode()

    def validate_message(message):
        try:
            #Validando se mensagem contém quatro informações
            list = message.split()
            if(len(list) != 4):
                return False            

            patient_arrival_interval = int(list[0])
            qt_doctors = int(list[1])
            qt_nurses = int(list[2])
            simulation_time = int(list[3])

            #Validando os tipos das quatro informações
            if(type(patient_arrival_interval) != int or type(qt_doctors) != int or type(qt_nurses) != int or type(simulation_time) != int):
                return False
            
            if(patient_arrival_interval < 1 or qt_doctors < 1 or qt_nurses < 1 or simulation_time < 1):
                return False

            return True 
        except:
            return False

class Server:        

    def create_server():
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        conn, ender = server.accept()
        return conn, ender

    def send_message(conn, message):
        conn.sendall(message.encode())

    def get_message(conn):
        return conn.recv(DATA_SIZE).decode()

class File:
    def print(text):
        print(text)
        with open("result.txt", 'a') as file:
            file.write(text)
            file.close()