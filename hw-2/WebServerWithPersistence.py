#basic HTTP web server that can support non-persistent or persistent HTTP requests for task 2
from socket import *

IP = '192.168.1.178' #IP of server machine
PORT = 8000 #port of HTTP application

serverSocket = socket(AF_INET, SOCK_STREAM) #create TCP socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #this will allow the re-use of the port or else the server can not restart and use the same port again
serverSocket.bind((IP, PORT)) #bind the application to the port
serverSocket.listen(1) #listen for incoming connection requests
print("Server is now listening")

while True:

    try:
        connectionSocket, clientAddress = serverSocket.accept() #accept any incoming TCP connection requests from clients
        message = connectionSocket.recv(1024) #receive a message from the client; this is expected to be an HTTP request
        #debug print out the request
        print("---------------------------------------")
        print("Received messsage: " + message.decode())
        print("From: " + str(clientAddress))
        print("---------------------------------------")
        filename = message.decode().split()[1] #get the first field of the message which is the request file name and directory
        connectionType = message.decode().split()[4] #get the request persistence type
        f = open(filename[1:], 'rb') #open the file by path in the server local 
        if connectionType == 'close':
            print("Non-persistent connection")
            response = f.read() #read the file contents as bytes and save it in a response variable
            f.close() #close out file so other processes can access it
            connectionSocket.send("HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n".encode()) #send an OK 200 response as the header so the client's browser can signify a successful page load to the client
            #since it is non-persistent connection, acknowledge this with "Connection: close"
            #leave a blank line with two carriage returns and two new lines
            #below the blank line are the contents of the HTML page to be rendered on the client's browser
            connectionSocket.send(response) #send the response to the client
            connectionSocket.send("\r\n".encode()) #send a carriage return and new line to signify the end of the HTTP response
            connectionSocket.close() #close the TCP connection after an object as been sent
        else:
            print("Persistent connection")
            requestedObjectPaths = ["objects/cat0.png", "objects/cat1.jpg", "objects/cat2.jpg", "objects/cat3.jpg", "objects/cat4.jpg", "objects/cat5.jpg", "objects/cat6.jpg", "objects/cat7.jpg", "objects/cat8.jpg", "objects/cat9.jpg", "objects/text0.txt", "objects/text1.txt", "objects/text2.txt", "objects/text3.txt", "objects/text4.txt", "objects/text5.txt", "objects/text6.txt", "objects/text7.txt", "objects/text8.txt", "objects/text9.txt"]
            requestedObjectPaths.insert(0, str(filename[1:])) #along with the objects, the base HTML file should also be requested
            #hard code the object paths that would be associated with the base HTML file
            #in a more sophisticated server, it will automatically parse the HTML file to get this information
            for requestedObjectPath in requestedObjectPaths: #iterate through the object paths and append it to the response
                f = open(requestedObjectPath, 'rb')
                response = f.read()
                header = "HTTP/1.1 200 OK\r\nConnection: keep-alive\r\nContent-Length: " + str(len(response)) + "\r\n\r\n"
                connectionSocket.send(response) #send the response to the client
                connectionSocket.send("\r\n".encode()) #send a carriage return and new line to signify the end of the HTTP response
            connectionSocket.close() #close the TCP connection so other clients can request

    except IOError: #if opening the request file path results in the file not existing, catch this error and return a 404 HTTP response as well as a 404 not found HTML page
        # Send HTTP response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close the client connection socket
        connectionSocket.close() 
