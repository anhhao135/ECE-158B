#ECE158B, HW2. Skeleton Python Code for the Web Server.
#import socket module
from socket import *
import signal
import sys
import time
import threading

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    serverSocket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = threading.Event()
forever.wait()

IP = '192.168.1.178'
PORT = 8000

serverSocket = socket(AF_INET, SOCK_STREAM) #TCP
serverSocket.bind((IP, PORT))
serverSocket.listen(1)
print("Server is now listening")

while True:

    clientConnection, clientAddress = serverSocket.accept()
    print("here")
    message, address = clientConnection.recvfrom(1024)
    # Print out datagram info
    print("Received messsage: " + message.decode())
    print("From: " + str(address))
    print("---------------------------------------")
    response = 'HTTP/1.0 200 OK\n\nHello World'
    clientConnection.sendall(response.encode())
    clientConnection.close()
