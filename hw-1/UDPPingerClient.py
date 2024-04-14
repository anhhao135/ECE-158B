# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *

serverName = '192.168.1.178'
serverPort = 1919
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = 'test123'
clientSocket.sendto(message.encode(), (serverName, serverPort))


