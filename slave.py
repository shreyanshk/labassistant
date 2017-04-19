import socket
import ssl
from common import *
import struct
import sys
import pickle
import json
from slaveUtil import *
param = {}
multicast_group = '224.3.29.71'
server_address = ('', 24979)

def run():
    param = ReadPickle()
    if(verifyKeys()==True):
        generatekey("secp256k1")
        run()
    publickey = open("publickey.pem", 'r').read()
    msg = {}
    msg["akg"] = "Connection is acknowledged"
    msg["publickey"] = publickey
    msg["friendlyName"] = param["friendlyName"]
    connMsg = json.dumps(msg)
    sock = createSocket('', 24979)
    SlaveSocketConfig(sock,multicast_group)
    while True:
        data,address = SlaveReceive(sock,"Waiting for connection")
        if(data.decode() == "connect"):
            Send(connMsg,address,sock)
            data,address = SlaveReceive(sock,"Waiting for Master Public Key")
            param["Master Public Key"] = data
            param["Master address"] = address
            WritePickle(param)
