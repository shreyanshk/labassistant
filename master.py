import socket
from common import *
from time import sleep

def run(mcastGroup = None, key = None):
    if key == None:
        try:
            privateKey = loadPrivateKey('privatekey.pem')
        except FileNotFoundError:
            generatekey('SECP256K1')
    if mcastGroup == None:
        mcastGroup = ('224.3.29.71', 24979)
    mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    while (True):
        mcastSocket.sendto(b"this is a test", mcastGroup)
        sleep(1)
