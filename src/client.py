import socket

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(str.encode('Bom dia Bóson'))
data = s.recv(1024)

print('Mensagem enviada do client: ', data.decode())
