from socket import *

HOST = gethostname()
PORT = 50000

class Client:    

    def close_connection(message):        
        return message == '0' or message == 0

    def create_client():
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((HOST, PORT))
        return client

class Server:    

    def close_connection(data):
        return data.decode() == '0'

    def create_server():
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        conn, ender = server.accept()
        return conn, ender


    def send_message(conn, message):
        conn.sendall(message.encode())