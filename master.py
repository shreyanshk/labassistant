import socket
import ssl
from common import *

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
        print("Generating new key pair")
        generatekey("secp256k1")
    else:
        pass
except FileNotFoundError:
    generatekey("secp256k1")
