import sys
import socket
import threading
import argparse
import pycat_util
import os
from signal import signal

#Global Variables
Listen = False
Connect= False
PortScan=False
Execute=False

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
    parser.add_argument('-e','--execute',help="Launches a specified script/program after connection")
    parser.add_argument('-q', help="Specify number of seconds to keep the connection open")
    parser.add_argument('-p', '--port',help="specify port to listen on")
    parser.add_argument("host_address", nargs="*")
    parser.add_argument('-v', help="Verbose Output", action="store_true")
    parser.add_argument('-z', help="Zero I/O mode - Used for Scanning", action="store_true")
    args= vars(parser.parse_args())
#    print(args)
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
    Execute= True if opts['execute']!=None else False
    fpath=None
    qsec=None
    if(Listen):
        if(opts['port'] == None):
            usage()
        if(not Execute):
            fpath=None
        else:
            fpath=opts['execute']
        if(opts['q']):
            qsec=int(opts['q'])
        else:
            qsec=None
        pycat_util.listen(opts['port'],fpath, qsec)

    #Connect
    Connect = True if opts['listen']==False and opts['execute']==None and opts['z']==False and opts['host_address']!=[] else False
#    print(opts['host_address'], len(opts['host_address']))
#    print(Connect)
    if(Connect):
        if(not sys.stdin.isatty()):
            inp_file=sys.stdin.read()
        else:
            inp_file=None
        ip = opts['host_address'][0]
        ip=socket.gethostbyname(ip)
        port = int(opts['port']) if opts['port']!=None else 80
        if(isIP(ip)):
            pycat_util.connect(ip,inp_file,port)
        else:
            print("Invalid IP address")

    #Port Scanning
    PortScan = True if opts['z']==True else False
    if(PortScan):
        port=opts['port']
        ip=socket.gethostbyname(opts['host_address'][0])
#        ip = opts['host_address'][0] if isIP(opts['host_address'][0]) else None
        if(ip):
            pycat_util.portScan(ip,port)
        else:
            print("Invalid IP")

#    Execute=True if opts['execute']!=None else False
#    if(Execute):
#        os.popen(opts['execute'])

if __name__=='__main__':
    main()
