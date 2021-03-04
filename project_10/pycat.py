import socket
import sys
import os
from pycat_chat import tcp_connect
import signal

class Netcat:
    def __init__(self, argv):
        self.noAg = len(argv)
        self.args = list(argv)
    def chat(self,ip,port,status):
        print("Chat Initiated")
        ins = tcp_connect(str(ip),str(port))
        if(status=='serv'):
            ins.serv()
        elif(status=='cli'):
            ins.cli()
        
def areFlags(arg):
    flagList=[]
    for i in arg[1:-2]:
        if(isFlag(i)):
            flagList.append(i)
    return(flagList)
def isFlag(arg):
    if(len(arg)==2):
        if(arg[0]=='-' and arg[1].isalpha()==True):
            return True
    return False
def getIP():
    try:
        return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except:
        return('127.0.0.1')
def isAddress(arg):
    numflag=0
    if(arg.count('.')==3):
        iplist=arg.split('.')
        if(len(iplist)==4):
            for i in iplist:
                if(i.isdigit() and int(i)>=0 and int(i)<256):
                    pass
                else:
                    return False
        else:
            return False
    else:
        return False
    return True
def isPort( arg):
    if(arg.isdigit()):
        if(int(arg)>1024 and int(arg)<65536):
            return(True)
    return(False)



if __name__=='__main__':
    instance = Netcat(sys.argv)
    args = list(sys.argv)

    if(len(args) < 2):
        print("Usage:")
        print("python3 pycat.py <options> host_address port")
        print(" -l -p <port>\t : listen on a particular port")
        print("")
        sys.exit(1)

    if('-l' not in args):
        if(isAddress(args[-2])):
            if(isPort(args[-1])):
                instance.chat(str(args[-2]),str(args[-1]),'cli')
            else:
                print("Port error")
                sys.exit(1)
        else:
            print("Network Unreachable. Invalid Ip address")
            sys.exit(1)
    else:
        if(isFlag(args[-2]) and args[-2]=='-p'):
            if(isPort(args[-1])):
                ip_ad=getIP()
                instance.chat(str(ip_ad),str(args[-1]),'serv')
