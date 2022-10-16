import socket
import sys

def createRxSocket(ip, port):
	rxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	rxAddr = (ip, port)
	rxSocket.bind(rxAddr)
	return rxSocket

def createTxSocket():
	txSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return txSocket

def send(data, socket,ip, port):
	payload = str(data)
	socket.sendto(payload.encode('utf-8'), (ip, port))

