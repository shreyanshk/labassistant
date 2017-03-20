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
