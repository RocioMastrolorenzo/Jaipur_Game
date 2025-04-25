import socket

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

welcome = client.recv(4096).decode()
print(welcome)

d = client.recv(4096).decode()
print(d)