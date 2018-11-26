from slave import Slave
from master import Master
from sys import argv


if __name__ == '__main__':
    if argv[1] == 'slave':
        slave = Slave()
        slave.run()
    elif argv[1] == 'master':
        master = Master()
        master.run()
else:
    print("Please execute the program correctly.")  # put better explanation
