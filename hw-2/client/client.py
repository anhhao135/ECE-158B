import sys
from socket import *
import time

#this is the client code to test non-persistent and persistent HTTP requests

#command line arguments
serverHostIP = sys.argv[1]
serverHostPort = sys.argv[2]
requestedObject = sys.argv[3]
persistent = int(sys.argv[4]) #0 for non-persistent, 1 for persistent
printServerResponse = int(sys.argv[5]) #0 for do not print, 1 for print; printing response can slow down transaction so disable for benchmarking

requestedObjectPaths = ["objects/cat0.png", "objects/cat1.jpg", "objects/cat2.jpg", "objects/cat3.jpg", "objects/cat4.jpg", "objects/cat5.jpg", "objects/cat6.jpg", "objects/cat7.jpg", "objects/cat8.jpg", "objects/cat9.jpg", "objects/text0.txt", "objects/text1.txt", "objects/text2.txt", "objects/text3.txt", "objects/text4.txt", "objects/text5.txt", "objects/text6.txt", "objects/text7.txt", "objects/text8.txt", "objects/text9.txt"] #we are hardcoding the objects that will exists in the HTML file

requestedObjectPaths.insert(0, str(requestedObject)) #along with the objects, the base HTML file should also be requested

if persistent: #only one TCP connection to get all objects
    startTime = time.time() #start time to measure transaction length
    clientSocket = socket(AF_INET, SOCK_STREAM) 
    clientSocket.connect((str(serverHostIP), int(serverHostPort)))
    message = "GET /" + str(requestedObject) + " HTTP/1.1\r\nConnection: keep-alive\r\nAccept: image/*,text/*\r\n\r\n"
    #the HTTP request will be a GET request, but we request the connection to be persistent with "keep-alive", and also tell the server to send over any objects that are part of the HTML file so it can be rendered on the client side with the "Accept: " field; the server knows it can send over any image or text type object
    clientSocket.send(message.encode()) #send this GET request
    message = clientSocket.recv(1024) #wait for a response
    totalBytesReceived = 0 #keep count of the total amount of bytes received from the server, including the headers
    while len(message) > 0: #keep receiving as long as there are bytes coming in from server
        if printServerResponse:
            print("---------------------------------------")
            print("Received messsage: " + str(message))
            print("From: " + str(serverHostIP))
            print("---------------------------------------")
        totalBytesReceived = totalBytesReceived + len(message)
        message = clientSocket.recv(1024)
    clientSocket.close() #once there are no more received bytes, we close the persistent TCP connection
    #at this point, the client can fully render the base HTML webpage with the objects
    #this would be under the hood of a browser; obviously this code is not sophisticated enough to do that so we don't do anything with the received data
    endTime = time.time() #end persistent HTTP transaction timer
    totalTime = endTime - startTime #measure how long the transaction took
    print("Bytes received: " + str(totalBytesReceived)) #print how many bytes were sent from the server
    print("Persistent transaction took: " + str(totalTime)) #print out transaction time for comparison
else: #one TCP connection per object
    startTime = time.time()
    totalBytesReceived = 0
    for requestedObjectPath in requestedObjectPaths: #we iterate through the individual object paths to request, starting with the base HTML page
        print("Requesting object: " + str(requestedObjectPath)) #print out requested object
        clientSocket = socket(AF_INET, SOCK_STREAM) 
        message = "GET /" + str(requestedObjectPath) + " HTTP/1.1\r\nConnection: close\r\n\r\n"
        #create the GET request but since it is non-persistnet, it is very simple, only indicating the object path and non-persistent HTTP (close) - close the connection after
        clientSocket.connect((str(serverHostIP), int(serverHostPort))) #we open a new TCP connection per object
        clientSocket.send(message.encode())
        message = clientSocket.recv(1024)
        while len(message) > 0: #keep receiving bytes from server and track byte count
            if printServerResponse:
                print("---------------------------------------")
                print("Received messsage: " + str(message))
                print("From: " + str(serverHostIP))
                print("---------------------------------------")
            totalBytesReceived = totalBytesReceived + len(message)
            message = clientSocket.recv(1024)
        clientSocket.close()
        #at this point we have received one object from the server. move on to the next object and open a new conenction for that
    endTime = time.time()
    totalTime = endTime - startTime
    print("Bytes received: " + str(totalBytesReceived))
    print("Non-persistent transaction took: " + str(totalTime)) #print out transaction time for comparison
