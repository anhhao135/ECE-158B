#ECE158B, HW2. Skeleton Python Code for the Web Server.
#import socket module
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM) #TCP
serverSocket.bind(('', 1919))
serverSocket.listen(1)
print("Server is now listening")

while True:
    clientConnection, clientAddress = serverSocket.accept()
    message, address = clientConnection.recvfrom(1024)
    # Print out datagram info
    print("Received messsage: " + message.decode())
    print("From: " + str(address))
    print("---------------------------------------")
    clientConnection.close()

serverSocket.close()