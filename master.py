import socket
from common import Common
from time import sleep
import pickle
import threading

class Master(Common):
	def displayString(self, string):
		cmd = {
			'cmd': 'displayString',
			'args': (string)
		}
		data = self.signedCmd(cmd)
		self.mcastSocket.sendto(data, self.mcastGroup)

	def reboot(self, force = False, timer = 0) :
		cmd: {
			'cmd': 'reboot',
			'args': (force, timer)
		}
		data = self.signedCmd(cmd)
		self.mcastSocket.sendto(data, self.mcastGroup)

	def shutdown(self, timer = 0, force = False):
		cmd = {
		'cmd': 'shutdown',
		'args': (timer, force)
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
		while True:
			self.reboot()
			sleep(1)

	def heartbeat(self, timer = 5):
		data = {
			'type': 'heartbeat',
			'serializedPublicKey': self.param['serializedPublicKey'],
			'friendlyName': self.param['friendlyName']
		}
		data = pickle.dumps(data)
		while (True):
			self.mcastSocket.sendto(data, self.mcastGroup)
			sleep(timer)
