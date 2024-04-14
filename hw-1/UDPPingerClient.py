from socket import *
import time

serverName = '192.168.1.178' #local linux machine running server code
serverPort = 1919 #known socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

numberOfPings = 10

for i in range(numberOfPings):
	message = 'ping' + str(i)
	clientSocket.settimeout(1)
	clientSocket.sendto(message.encode(), (serverName, serverPort))
	pingStartTime = time.time()

	try:
		message, address = clientSocket.recvfrom(1024)
		pingEndTime = time.time()
		pingRTT = pingEndTime - pingStartTime
		print("Received messsage: " + message.decode())
		print("From: " + str(address))
		print("Ping RTT: " + str(pingRTT))
	except:
		print("Ping timed out!")

	print("---------------------------------------")



