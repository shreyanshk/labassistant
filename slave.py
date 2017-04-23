import socket
import struct
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from common import Common
import os
from time import sleep

class Slave(Common):
	def run(self, mcastGroup = None):
		if mcastGroup == None:
			self.mcastGroup = ('224.3.29.71', 24979)
		self.mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.mcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		self.mcastSocket.bind(self.mcastGroup)
		mreq = struct.pack("4sl", socket.inet_aton(self.mcastGroup[0]), socket.INADDR_ANY) #idk
		self.mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
		try:
			masterSerializedPublicKey=self.param['masterSerializedPublicKey']
			self.listener()
		except KeyError:
			print('Looking for master server now.')
			heartbeat = False
			while(~heartbeat):
				rcvdata,masterAddress = self.mcastSocket.recvfrom(1024)
				rcvdict = pickle.loads(rcvdata)
				if (rcvdict['type'] == 'heartbeat'):
					permission = input("Do you want to connect to: "
						+ rcvdict['friendlyName']
						+ ' at IP '+ str(masterAddress)
						+ ' whose signature is \n\n'+rcvdict['serializedPublicKey'].decode()
						+ '\nReply with [y/n]: '
					)
					if (permission == 'y') or (permission == 'Y'):
						self.masterAuthenticate(rcvdict,masterAddress)
						self.listener()
					else:
						print('Incomplete configuration, please rerun the program.')
						exit()

	def masterAuthenticate(self,masterData,masterAddress):
		self.masterUcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = {
			'serializedPublicKey': self.param['serializedPublicKey'],
			'friendlyName': self.param['friendlyName'],
			'msg': 'ackSlave'
		}
		ackData = pickle.dumps(data)
		self.masterUcastSocket.sendto(ackData, masterAddress)
		#rcvdata,address = self.masterUcastSocket.recvfrom(1024) ##Recieve acknowledment from master
		'''if (address == masterAddress[0]):
			rcvdict = pickle.loads('data')
			masterPublicKey = serialization.load_pem_public_key(
				masterData['serializedPublicKey'],
				backend=default_backend()
			)'''
		self.param['masterSerializedPublicKey'] = masterData['serializedPublicKey']
		self.param['masterFriendlyName'] = masterData['friendlyName']
		self.saveParams()
		print(self.param)

	def listener(self):
		print("Listening for commands from " + self.param['masterFriendlyName'])
		masterSerializedPublicKey = self.param['masterSerializedPublicKey']
		masterPublicKey = serialization.load_pem_public_key(
				masterSerializedPublicKey,
				backend = default_backend()
			)
		while True:
			rcvdata,masterAddress = self.mcastSocket.recvfrom(1024)
			rcvdict = pickle.loads(rcvdata)
			if (rcvdict['type'] == 'cmd') and (self.verifyMsg(masterPublicKey, rcvdict)):
				cmds = pickle.loads(rcvdict['data'])
				function = self.dispatcher(cmds['cmd'])
				if (function == None):
					self.cmdNotFoundError(cmds['cmd'])
				else:
					function(cmds['args'])

	def cmdNotFoundError(self, string):
		data = {
			'serializedPublicKey': self.param['serializedPublicKey'],
			'friendlyName': self.param['friendlyName'],
			'msg': 'cmdNotFoundError'
		}

# function definitions starts here

	def displayString(self,string):
		print(string)

	def shutdown(self, force = False, timer = 0) :
		print("The system will shut down in " + str(timer) + " seconds." )
		sleep(timer)
		os.system("shutdown now -h")

	def reboot(self, force = False, timer = 0) :
		print("The system will reboot in " + str(timer) + " seconds." )
		sleep(timer)
		if (force):
			os.system("reboot --force")
		else:
			os.system("reboot")

# function definitions end here

	def dispatcher(self, string):
		cmds = {
			'displayString': self.displayString,
			'reboot': self.reboot
			'shutdown': self.shutdown
		}
		return cmds[string]
