from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import os

class Common:
    def __init__(self):
        self.privateKey = None
        self.loadParam()
    def generatekey(param):
        self.privateKey = ec.generate_private_key(
            ec.SECP256K1(), default_backend()
        )
    def saveParams():
        pass
    def signMessage(self, data):
        signature = self.privateKey.sign(
            data,
            ec.ECDSA(hashes.SHA512()) #check if it's secure
        )
        return signature
    def loadParam(self, filename = None):
        pass
