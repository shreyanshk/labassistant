import os
import socket
import struct
import sys
import ssl

def generatekey(param):
    exist = os.path.isfile("/usr/bin/openssl")
    if (exist):
        cmd = [
            'openssl',
            'ecparam',
            '-name',
            param,
            '-genkey',
            '-noout',
            '-out',
            'privatekey.pem'
        ]
        error = run(cmd).returncode
        if (error != 0):
            return error
        cmd = [
            'openssl',
            'ec',
            '-in',
            'privatekey.pem',
            '-pubout',
            '-out',
            'publickey.pem'
        ]
        error = run(cmd).returncode
        if (error != 0):
            return error
        return exist
    else:
        return exist

def verifyKeys():
    try:
        privatekey = open("privatekey.pem", 'r').read()
        publickey = open("publickey.pem", 'r').read()
        verifyerror = False
        verify = privatekey.split("\n")
        if ((verify[0] != "-----BEGIN EC PRIVATE KEY-----") or (verify[4] != "-----END EC PRIVATE KEY-----")):
            verifyerror = True
            print("error in privatekey")
        verify = publickey.split("\n")
        if ((verify[0] != "-----BEGIN PUBLIC KEY-----") or (verify[3] != "-----END PUBLIC KEY-----")):
            verifyerror = True
            print("error in publickey")

    except FileNotFoundError:
        verifyerror = True
        print("File not found")
    return verifyerror

def createSocket(address,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverif = (address, port)
    sock.bind(serverif)
    return sock

def Send(message,address,sock):
    try:
        print(sys.stderr, 'sending "%s"' % message)
        sent = sock.sendto(message.encode(), address)
    except:
        print("Error in sending  Data")
