import socket
from common import Common
from time import sleep
import pickle
import threading

class Master(Common):
	def shutdown(self, timer = 0, force = False):
		cmd = {
		'shutdown': (timer, force)
		}
		data = self.signedCmd(cmd)
		self.mcastSocket.sendto(data, self.mcastGroup)

	def displayString(self, string):
		cmd = {
			'echo': (string)
		}
		data = self.signedCmd(cmd)
		self.mcastSocket.sendto(data, self.mcastGroup)

	def run(self, mcastGroup = None):
		if mcastGroup == None:
			self.mcastGroup = ('224.3.29.71', 24979)
		self.mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		heartbeatThread = threading.Thread(target = self.heartbeat)
		heartbeatThread.daemon = False
		heartbeatThread.start()

	def heartbeat(self, timer = 5):
		data = {
			'serializedPublicKey': self.param['serializedPublicKey'],
			'friendlyName': self.param['friendlyName']
		}
		data = pickle.dumps(data)
		while (True):
			self.mcastSocket.sendto(data, self.mcastGroup)
			sleep(timer)
