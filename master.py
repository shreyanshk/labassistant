import socket
from common import Common
from time import sleep

class Master(Common):
    def run(self, mcastGroup = None):
        if mcastGroup == None:
            mcastGroup = ('224.3.29.71', 24979)
        mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        while (True):
            mcastSocket.sendto(b"this is a test", mcastGroup)
            sleep(1)
