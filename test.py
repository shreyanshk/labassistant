import socket
import ssl
from common import *
import struct
import sys
import pickle

param = {}
multicast_group = '224.3.29.71'

def sendPublicKey(publickey):
	server_address = ('', 24979)
	# Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# Bind to the server address
	sock.bind(server_address)
	# Tell the operating system to add the socket to the multicast group
	# on all interfaces.
	group = socket.inet_aton(multicast_group)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	# Receive/respond loop
	msg = {}
	msg["akg"] = "Connection is acknowledged"
	msg["publickey"] = publickey
	while True:
		print("waiting for connection")
		data, address = sock.recvfrom(1024)
		print(data)
		if (data.decode() == "connect"):
			sock.sendto(publickey.encode(), address)
			data, address = sock.recvfrom(1024)
			MasterPublicKey = data.decode()
			print(MasterPublicKey)
try:
	with open('param.pickle', 'rb') as f:
		param = pickle.load(f)
except:
	param['friendlyName'] = input("Enter the friendly name")
	with open('param.pickle', 'wb') as f:
		pickle.dump(param, f)
try:
	privatekey = open("privatekey.pem", 'r').read()
	publickey = open("publickey.pem", 'r').read()
	verifyerror = False
	verify = privatekey.split("\n")
	if ((verify[0] != "-----BEGIN EC PRIVATE KEY-----") or (verify[4] != "-----END EC PRIVATE KEY-----")):
		verifyerror = True
	verify = publickey.split("\n")
	if ((verify[0] != "-----BEGIN PUBLIC KEY-----") or (verify[3] != "-----END PUBLIC KEY-----")):
		verifyerror = True
	if (verifyerror):
		print(verify)
		print("Generating new key pair")
		generateKey()
	else:
		sendKeyPair(publickey)
except FileNotFoundError:
    generateKey()
