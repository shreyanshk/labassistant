import sqlite3
from common import *
import struct
import sys
import ssl
import json

def createDB():
    conn = sqlite3.connect('test.db')
    print ("Opened database successfully");
    conn.execute('''CREATE TABLE if not exists ipList (FriendlyName TEXT PRIMARY KEY NOT NULL, IPAdress TEXT NOT NULL, PublicKey TEXT NOT NULL);''');

def MasterReceive(sock):
    try:
        data, server = sock.recvfrom(1024)
    except socket.timeout:
        print ('timed out, no more responses')
        exit()
    else:
        print('received "%s" from %s' % (data, server))
        print(server[0])
        SlaveMsg = json.loads(data.decode())
        conn = sqlite3.connect('test.db')
        sql = ''' INSERT INTO ipList(FriendlyName,IPAdress,PublicKey) VALUES(?,?,?) '''
        values = (SlaveMsg["friendlyName"],server[0],SlaveMsg["publickey"])
        cur = conn.cursor()
        cur.execute(sql, values)


def MasterSocketConfig(sock):
        sock.settimeout(0.5)
        ttl = struct.pack('b', 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
