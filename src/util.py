from socket import *

HOST = gethostname()
PORT = 50000
DATA_SIZE = 1024

class Util:
    QT_EMPLOYEES_BY_BLOCK = {'A': 5, 'B':3, 'C': 2, 'D': 1 }

    PATIENT_STATE = {1: 'Ligh', 2:'Moderate', 3: 'Serious', 4: 'Very Serious' }

    def get_patient_information(message):
        list = message.split()
        name = list[0]
        state = int(list[1])
        return name, state

class Client:    

    def close_connection(message):        
        return message == '0' or message == 0

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
            #Validando se mensagem contém duas informações
            list = message.split()
            if(len(list) != 2):
                return False            

            name = list[0]
            state = int(list[1])

            #Validando os tipos das duas informações
            if(type(name) != str or type(state) != int):
                return False             

            #Validando se a gravidade é válida
            if(state < 1 or state > 4):
                return False

            return True 
        except:
            return False

class Server:    

    def close_connection(message):
        return message == '0'

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