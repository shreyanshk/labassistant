import socket
import ssl
import subprocess
from common import *

try:
    privatekey = open("privatekey.pem", 'r').read()
    publickey = open("publickey.pem", 'r').read()
    print(privatekey)
    print(publickey
except FileNotFoundError:
    generateKey()
