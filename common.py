from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import os
import pickle

class Common:
	def __init__(self):
		try:
			self.loadParam()
		except FileNotFoundError:
			self.param = {}
			self.privateKey = ec.generate_private_key(
				ec.SECP256K1(),
				default_backend()
			)
			self.param['friendlyName'] = input("Enter your friendly name: ")
			self.saveParams()

	def saveParams(self):
		serializedPrivateKey = self.privateKey.private_bytes(
			encoding = serialization.Encoding.PEM,
			format = serialization.PrivateFormat.PKCS8,
			encryption_algorithm = serialization.NoEncryption()
		)
		data  = (self.param, serializedPrivateKey)
		with open('param.pickle', 'wb') as f:
			pickle.dump(data, f)

	def signMessage(self, data):
		signature = self.privateKey.sign(data,ec.ECDSA(hashes.SHA512())) #check if it's secure
		return signature

	def loadParam(self):
		with open('param.pickle', 'rb') as f:
			data = pickle.load(f)
			self.param = data[0]
			self.privateKey = serialization.load_pem_private_key(
				data[1],
				password = None,
				backend = default_backend()
			)

if __name__ == '__main__':
	c = Common()
