# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import time

serverName = '192.168.1.178'
serverPort = 1919
clientSocket = socket(AF_INET, SOCK_DGRAM)


for i in range(10):
	time.sleep(0.1)
	message = 'test' + str(i)
	clientSocket.sendto(message.encode(), (serverName, serverPort))
	clientSocket.settimeout(1)

	try:

		message, address = clientSocket.recvfrom(1024)
		print("Received messsage: " + message.decode())
		print("From: " + str(address))


	except:
		print("timed out")



