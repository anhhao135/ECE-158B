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
    try:
        connectionSocket, clientAddress = serverSocket.accept()
        message, address = connectionSocket.recvfrom(1024)
        filename = message.decode().split()[1]
        f = open(filename[1:], 'rb')
        response = f.read()
        f.close()
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connectionSocket.send(response)
        connectionSocket.send("\r\n".encode())
        connectionSocket.close() 
    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close the client connection socket
        connectionSocket.close()
