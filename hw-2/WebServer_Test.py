#ECE158B, HW2. Skeleton Python Code for the Web Server.
#import socket module
from socket import *

IP = '192.168.1.178'
PORT = 8000

serverSocket = socket(AF_INET, SOCK_STREAM) #TCP
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((IP, PORT))
serverSocket.listen(1)
print("Server is now listening")

while True:

    connectionSocket, clientAddress = serverSocket.accept()
    message, address = connectionSocket.recvfrom(1024)
    filename = message.split()[1]
    f = open(filename[1:])
    connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    for i in range(0, len(f)):
            # encode the string using the provided encoding. This function returns the bytes object. If we don’t provide encoding, “utf-8” encoding is used as default.
            connectionSocket.send(f[i].encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.close() 
