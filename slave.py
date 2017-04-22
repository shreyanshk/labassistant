import socket
import struct
from common import Common

class Slave(Common):
    def run(self, mcastGroup = None):
        if mcastGroup == None:
            mcastGroup = ('224.3.29.71', 24979)
        mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        mcastSocket.bind(mcastGroup)
        mreq = struct.pack("4sl", socket.inet_aton(mcastGroup[0]), socket.INADDR_ANY) #idk
        mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while (True):
            print(mcastSocket.recv(1024))
