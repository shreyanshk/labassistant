import socket
import ssl
from common import *
from masterUtil import *
import sqlite3
import struct
import sys

multicast_group = ('224.3.29.71', 24979)


def run():
    createDB()
    message="connect"
    if(verifyKeys()==True):
        generatekey("secp256k1")
        run()
    publickey = open("publickey.pem", 'r').read()
    sock = createSocket("169.254.188.114",0)
    MasterSocketConfig(sock)
    Send(message,multicast_group,sock)
    MasterReceive(sock)
    Send(publickey,multicast_group,sock)
    print(sys.stderr, 'closing socket')
    sock.close()
