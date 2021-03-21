import sys
import socket
import threading
import argparse
import pycat_util
from signal import signal

#Global Variables
Listen = False
Connect= False
PortScan=False

def usage():
    print("Usage:")
    print("Connect to somewhere: \t python3 pycat.py [-options] hostname")
    print("Listen for connections: \t python3 pycat.py -l -p port [-options]..")
    print("-p \t port \t : Specify port for establishing a connection")
    print("-l \t listen \t: Listen for incoming connections")
    print("-v \t Verbose \t : Display verbose output")
    print("-z \t Zero mode \t : Used for scanning ports")
    sys.exit(1)

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', dest='listen', help="Listen for incoming connections",action='store_true')
    parser.add_argument('-p', '--port',help="specify port to listen on")
    parser.add_argument("host_address", nargs="*")
    parser.add_argument('-v', help="Verbose Output", action="store_true")
    parser.add_argument('-z', help="Zero I/O mode - Used for Scanning", action="store_true")
    args= vars(parser.parse_args())
    return(args)

def isIP(addr):
    try:
        seg = addr.split('.')
        if(len(seg)!=4):
            return False
        for i in seg:
            if(int(i)<0 or int(i)>255):
                return False
        return True
    except:
        return False

def main():

    global Listen   
    global Connect

    opts = argparser()
    if(len(sys.argv)<2):
        usage()

    #Listen
    Listen = True if opts['listen']==True else False
    if(Listen):
        if(opts['port'] == None):
            usage()
        else:
            pycat_util.listen(opts['port'])

    #Connect
    Connect = True if opts['listen']==False and opts['z']==False and opts['host_address']!=[] else False
#    print(opts['host_address'], len(opts['host_address']))
    if(Connect):
        ip = opts['host_address'][0]
        port = int(opts['port'])
        if(isIP(ip)):
            pycat_util.connect(ip,port)
        else:
            print("Invalid IP address")

    #Port Scanning
    PortScan = True if opts['z']==True else False
    if(PortScan):
        port=opts['port']
        ip = opts['host_address'][0] if isIP(opts['host_address'][0]) else None
        if(ip):
            pycat_util.portScan(ip,port)
        else:
            print("Invalid IP")

if __name__=='__main__':
    main()
