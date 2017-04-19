import pickle
import socket
import struct
def ReadPickle():
        param = {}
        try:
                with open('param.pickle', 'rb') as f:
                        param = pickle.load(f)
        except:
                param['friendlyName'] = input("Enter the friendly name")
                WritePickle(param)
        return param

def WritePickle(obj):
    with open('param.pickle', 'wb') as f:
        pickle.dump(obj, f)

def SlaveSocketConfig(sock,multicast_group):
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def SlaveReceive(sock,displayMsg):
        print(displayMsg)
        data, address = sock.recvfrom(1024)
        print(data)
        return data, address
