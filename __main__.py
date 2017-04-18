import slave
import master
from sys import argv


if  __name__ == '__main__':
    if argv[1] == 'slave':
        slave.run()
    elif argv[1] == 'master':
        master.run()
else:
    print("Please execute the program correctly.") #put better explanation
