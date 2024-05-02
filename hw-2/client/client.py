import sys
from socket import *
import time

serverHostIP = sys.argv[1]
serverHostPort = sys.argv[2]
requestedObject = sys.argv[3]
persistent = int(sys.argv[4]) #0 for non-persistent, 1 for persistent

requestedObjectPaths = ["objects/cat0.png", "objects/cat1.jpg", "objects/cat2.jpg", "objects/cat3.jpg", "objects/cat4.jpg", "objects/cat5.jpg", "objects/cat6.jpg", "objects/cat7.jpg", "objects/cat8.jpg", "objects/cat9.jpg", "objects/text0.txt", "objects/text1.txt", "objects/text2.txt", "objects/text3.txt", "objects/text4.txt", "objects/text5.txt", "objects/text6.txt", "objects/text7.txt", "objects/text8.txt", "objects/text9.txt"]

requestedObjectPaths.insert(0, str(requestedObject))

if persistent:
    startTime = time.time()
    clientSocket = socket(AF_INET, SOCK_STREAM) 
    message = "GET /" + str(requestedObject) + " HTTP/1.1\r\nConnection: keep-alive\r\nAccept: image/*,text/*\r\n\r\n"
    clientSocket.connect((str(serverHostIP), int(serverHostPort)))
    clientSocket.send(message.encode())
    message = clientSocket.recv(1024)
    totalBytesReceived = 0
    while len(message) > 0:
        #print("---------------------------------------")
        #print("Received messsage length: " + str(len(message)))
        #print("From: " + str(serverHostIP))
        #print("---------------------------------------")
        totalBytesReceived = totalBytesReceived + len(message)
        message = clientSocket.recv(1024)
    clientSocket.close()
    print("Bytes received: " + str(totalBytesReceived))
    endTime = time.time() #end RTT timer
    totalTime = endTime - startTime
    print("Persistent transaction took: " + str(totalTime))
else:
    startTime = time.time()
    for requestedObjectPath in requestedObjectPaths:
        print(requestedObjectPath)
        clientSocket = socket(AF_INET, SOCK_STREAM) 
        message = "GET /" + str(requestedObjectPath) + " HTTP/1.1\r\nConnection: close\r\n\r\n"
        clientSocket.connect((str(serverHostIP), int(serverHostPort)))
        clientSocket.send(message.encode())
        message = clientSocket.recv(1024)
        totalBytesReceived = 0
        while len(message) > 0:
            #print("---------------------------------------")
            #print("Received messsage length: " + str(len(message)))
            #print("From: " + str(serverHostIP))
            #print("---------------------------------------")
            totalBytesReceived = totalBytesReceived + len(message)
            message = clientSocket.recv(1024)
        clientSocket.close()
        print("Bytes received: " + str(totalBytesReceived))
    endTime = time.time() #end RTT timer
    totalTime = endTime - startTime
    print("Non-persistent transaction took: " + str(totalTime))



while False:

    clientSocket = socket(AF_INET, SOCK_STREAM) 
    message = "GET /" + str(requestedObject) + " HTTP/1.1\r\nConnection: close\r\nAccept: image/*,text/*\r\n\r\n"
    clientSocket.connect((str(serverHostIP), int(serverHostPort)))
    clientSocket.send(message.encode())

    while True:
        message = clientSocket.recv(1024)
        print("---------------------------------------")
        print("Received messsage: " + message.decode())
        print("From: " + str(serverHostIP))
        print("---------------------------------------")

    clientSocket.close()

    while False:
        message, address = clientSocket.recv(1024)
        pingEndTime = time.time() 
        #print out datagram info
        print("Received messsage: " + message.decode())
        print("From: " + str(address))
        print("Ping RTT: " + str(pingRTT))

