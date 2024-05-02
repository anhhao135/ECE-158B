import sys
from socket import *
import time

serverHostIP = sys.argv[1]
serverHostPort = sys.argv[2]
requestedObject = sys.argv[3]


clientSocket = socket(AF_INET, SOCK_STREAM) 
message = "GET /" + str(requestedObject) + " HTTP/1.1\r\nConnection: close\r\nAccept: image/*,text/*\r\n\r\n"
clientSocket.connect((str(serverHostIP), int(serverHostPort)))
clientSocket.send(message.encode())
clientSocket.close()

while False:
    message, address = clientSocket.recv(1024)
    pingEndTime = time.time() 
    #print out datagram info
    print("Received messsage: " + message.decode())
    print("From: " + str(address))
    print("Ping RTT: " + str(pingRTT))

