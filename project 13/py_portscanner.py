import sys
import socket
import logging
import time
import threading
import concurrent.futures
from scapy.all import *
from struct import *

class port_scanner:
    def __init__(self, ip):
        self.ip = ip
        socket.setdefaulttimeout(1)
    def scan(self,ports):
        Hostname=socket.gethostbyname(self.ip)
        
        ports = ports.split('-')
        initial_port = int(ports[0])
        final_port = int(ports[1])+1
        
        try:
            for port in range(initial_port, final_port):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                res = s.connect_ex((self.ip,port))
                if(res == 0):
                    socket.getservbyport(port)
                    active_ports.append(port)
                s.close()
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Quitting..")
            sys.exit(1)
        except socket.gaierror:
            print("Hostname couldn't be resolved. Quitting..")
            sys.exit(1)
        except socket.error:
            print("Server not responding")
            sys.exit(1)
        
if __name__=='__main__':
#    sys.stderr=open(os.devnull, "w")
#    sys.stdout=open(os.devnull,"w")
    if(len(sys.argv)<2):
        print("Invalid arguments")
        print("Usage : python3 day12_port_scanner.py <ip_address>")
        print("Options:")
        print(" -p  :   specify ports eg. 1-10, 40-100")
        print("")
        sys.exit(1)
    args=list(sys.argv)

    #logging Config
    logging.basicConfig(format="   %(asctime)s : %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    ip = args[-1]
#    sys.stderr=open(os.devnull, "w")
#    sys.stdout=open(os.devnull,"w")
    if('-o' in args):
#        print(ip)
        icmp = IP(dst=ip)/ICMP()
        resp = bytes(sr1(icmp, timeout=10, verbose=0))
        ip_header = resp[0:20]
        iph = unpack("!BBHHHBBH4s4s",ip_header)
        ttl = iph[5]
#        print("TTL : {}".format(ttl))
#    sys.stderr=open(os.devnull, "w")
#    sys.stdout=open(os.devnull,"w")

    if('-p' in args):
        ind=args.index('-p')
        if(args[ind+1]!=args[-1]):
            ports=args[ind+1]
        else:
            print("Enter a valid port range")
            sys.exit(1)
    else:
        ports="0-65535"

    ps = port_scanner(ip)
    Hostname=socket.gethostbyname(ip)
    print('-'*65)
    logging.info("Establishing a connection with {}".format(Hostname))
    print('-'*65)
    
    start_time=time.time()
    threads=[]
    port_ini=int(ports.split('-')[0])
    port_final=int(ports.split('-')[1])
    inc=30
    counter=0
    active_ports=[]
    while(port_ini<port_final):
#        logging.info("Thread {}: Starting".format(index))
#        print(port_ini)
        flag='create'
        counter+=1
        if(counter<200 and flag=='create'):
            if(port_ini+inc < port_final):
                arg = str(port_ini)+'-'+str(port_ini+inc)
            else:
                arg = str(port_ini)+'-'+str(port_final)
            x=threading.Thread(target=ps.scan, args=(arg,))
            threads.append(x)
            port_ini=port_ini+inc
            x.start()
        else:
            flag='destroy'
        if(flag=='destroy'):
            for index,thread in enumerate(threads):
#        logging.info("Thread {}: Ending".format(index))
                thread.join()
                counter-=1
    for index, thread in enumerate(threads):
        thread.join()
    active_ports=sorted(active_ports)
#    print(active_ports)
    print(" PORT \t\t STATUS\tSERVICE ")
    for i in active_ports:
        print("{}/tcp  \t Open \t {}".format(i,socket.getservbyport(i)))

    end_time=time.time()
    print("\nTTL : {}".format(ttl))
    if(ttl < 65):
        print("Target Machine is running on Linux Distribution")
    elif(ttl >= 65 and ttl < 129):
        print("Target Machine is running on Windows Bases Distribution")
    else:
        print("Target Machine is running on Cisco")
    print("\nScan completed in {:.2f} seconds".format(end_time-start_time))
