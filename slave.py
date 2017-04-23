##Worked on windows so dont know if the code works.
import socket
import struct
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from common import Common
import os
from time import sleep
class Slave(Common):
    '''def shutdown(force,timer):
		print("The system will shut down in" + timer + "seconds" )	
		sleep(timer)
		os.system("shutdown now -h")'''
    def run(self, mcastGroup = None):
        if mcastGroup == None:
            mcastGroup = ('224.3.29.71', 24979)
        self.masterInfo = {}
        mcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        mcastSocket.bind(mcastGroup)
        mreq = struct.pack("4sl", socket.inet_aton(mcastGroup[0]), socket.INADDR_ANY) #idk
        mcastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while (True):
            rcvdata,masterAddress = mcastSocket.recvfrom(1024)
            rcvdict = pickle.loads(rcvdata)
            data = pickle.loads(rcvdict['data'])
            self.masterInfo = data
            try:
                data['MasterPublicKey']
            except NameError:
                masterPublicKey =  serialization.load_pem_public_key(
                    data['serializedPublicKey'],
                    backend=default_backend()
                )
                signature = rcvdict['signature']
                if(verifyMsg(masterPublicKey,signature,data)):
                    permision = input("Do you want to connect to: "+masterAddress+" "+data['friendlyName'])
                    if(permission == "y"):
                        data = {
                                'serializedPublicKey': self.param['serializedPublicKey'],
                                'friendlyName': self.param['friendlyName']##include signature here
                        }
                        self.masterConnect(data,masterAddress)
                    else:
                        break; ##Will keep the socket open to connect to diffeerent server
                else:
                    pass

    def masterConnect(self,data,masterAddress):
        ucastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ackData = pickle.dumps(data) 
            ucastSocket.sendto(data,(masterAddress[0],masterAddress[1]))
            rcvdata,address = mcastSocket.recvfrom(1024)##Recieve acknowledment from master
            if(address == masrerAddress[0]):##Check address of master is same
                rcvdict = pickle.loads('data')
                masterPublicKey =  serialization.load_pem_public_key(
                    MasterInfo['serializedPublicKey'],
                    backend=default_backend()
                )
                signature = rcvdict['signature']
                if(verifyMsg(masterPublicKey,signature,ackData)):                    
                        with open('masterParam.pickle', 'wb') as f:
                            pickle.dump(self.masterInfo, f)
        except:
            pass
