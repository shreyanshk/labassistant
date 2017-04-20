from subprocess import run
import os

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

def signMessage(key, data):
    signature = key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verifyKeys():
    try:
        privatekey = open("privatekey.pem", 'r').read()
        publickey = open("publickey.pem", 'r').read()
        verifyerror = False
        verify = privatekey.split("\n")
        if ((verify[0] != "-----BEGIN EC PRIVATE KEY-----") or (verify[4] != "-----END EC PRIVATE KEY-----")):
            verifyerror = True
        verify = publickey.split("\n")
        if ((verify[0] != "-----BEGIN PUBLIC KEY-----") or (verify[3] != "-----END PUBLIC KEY-----")):
            verifyerror = True
        if (verifyerror):
            print("Generating new key pair")
            generatekey("secp256k1")
        else:
            pass
    except FileNotFoundError:
        generatekey("secp256k1")

def loadPrivateKey(filename):
    pass
