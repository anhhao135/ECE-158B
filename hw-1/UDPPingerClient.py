from socket import *
import time

serverName = '192.168.1.178' #local linux machine running server code
serverPort = 1919 #known socket
clientSocket = socket(AF_INET, SOCK_DGRAM) #create socket with automatic number allocated
clientSocket.settimeout(1) #set receive timeout to 1 second
numberOfPings = 10 #number of pings to try

for i in range(numberOfPings): #do pings that send out a message each time and waits for a reply from the server
	message = 'ping' + str(i) #construct unique ping message
	clientSocket.sendto(message.encode(), (serverName, serverPort)) #send message to server IP and port
	pingStartTime = time.time() #start RTT timer

	try: #if message is received from server
		message, address = clientSocket.recvfrom(1024) #store the received message and address
		pingEndTime = time.time() #end RTT timer
		pingRTT = pingEndTime - pingStartTime #calculate RTT
		#print out datagram info
		print("Received messsage: " + message.decode())
		print("From: " + str(address))
		print("Ping RTT: " + str(pingRTT))
	except: #if recvform() function times out
		print("Ping timed out!")

	#move on to next ping
	print("---------------------------------------")



