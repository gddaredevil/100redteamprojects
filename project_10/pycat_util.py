import socket
import subprocess
import os
import threading
import sys
import logging
import time
import signal

global Verbose


logging.basicConfig(format="    %(asctime)s : %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
global INT_STAT
INT_STAT="RUN"
def getIP():
    try:
        return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except:
        return(socket.gethostbyname(socket.gethostname()))
def send(s):
    global INT_STAT
    while(True):
        try:
            if(INT_STAT=="STOP"):
                break
            else:
                msg=input()
                s.send(msg.encode())
        except:
            sys.exit(1)
            INT_STAT="STOP"
def recv(s):
    global INT_STAT
    while(True):
        try:
            if(INT_STAT =="STOP"):
                break
            else:
                msg=s.recv(1024)
            if(msg == b''):
                raise RuntimeError("SOCKET Connection Broken...")
                sys.exit(1)
            print(msg.decode())
        except:
            sys.exit(1)
            INT_STAT="STOP"

def spawn(s):
#    print("Spawning a shell")
    while(True):
        s.send("<BASh:#>".encode())
        msg=s.recv(1024)
        if(not msg):
            break
        try:
            output=subprocess.check_output(msg, stderr=subprocess.STDOUT, shell=True)
        except:
            output="Failed to execute command...\n".encode()
#        output=subprocess.run(msg, stderr=subprocess.STDOUT, shell=True, capture_output=False)
#        print(output)
        s.send(output)
def Interrupt(signum, frame):
    global INT_STAT
    INT_STAT="STOP"
def listen(port,fpath, qsec, Verbose):
    if(qsec!=None):
        signal.signal(signal.SIGALRM, Interrupt)
        signal.alarm(qsec)
        if(Verbose):
            print("Connection is established for {} seconds".format(qsec))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip=getIP()
    s.bind((ip, int(port)))
    if(Verbose):
        print("Listening at {}:{}".format(ip, port))
    s.listen(5)
    stat, conn = s.accept()
    if(fpath==None):
        if(Verbose):
            print("\U0001F609",end=" ")
            print('{} established a connection through port {}'.format(conn[0],conn[1]))
        sen = threading.Thread(target=send, args=(stat,), daemon=False)
        rec = threading.Thread(target=recv, args=(stat,), daemon=False)
    #    sen.daemon=True#    rec.daemon=True
        sen.start()
        rec.start()
#        sen.join()
#        rec.join()
    else:
        print("Spawning a Shell...")
        rec=threading.Thread(target=spawn, args=(stat,),daemon=False)
        rec.start()

def connect(ip, inp_file, port, Verbose):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    if(Verbose):
        print("Connection Successful through port {}".format(port))
#    if(s.recv(1024)):
#        print(s.recv(1024).decode())
    if(inp_file==None):
        sen = threading.Thread(target=send, args=(s,), daemon=False)
        rec = threading.Thread(target=recv, args=(s,), daemon=False)
#        print("Sending and Receiving Threads ready")
        sen.start()
        rec.start()
    else:
        s.send(inp_file.encode())
#        s.close()
#        with open(inp_file,"w") as file:
#            data=file.readline()
#            while(data):
#                data=file.readline()
#                print(data)
#                s.send(data)
#            file.close()
#    print("COnnection ended...")

def portScan(ip, port, Verbose):
    global active_ports
    active_ports={}
    start_time = time.time()
    socket.setdefaulttimeout(1)
    counter=0
    inc=50
    threads=[]
    flag="CREATE"
    port_ini=0
    port_fin=1024
    if(port.isdigit() == False):
        try:
            arr = port.split('-')
            if(len(arr)!=2 or arr[0].isdigit()==False or arr[1].isdigit()==False):
                print("Invalid port")
                sys.exit(1)
            else:
                port_ini=int(arr[0])
                port_fin=int(arr[1])+1
        except:
            print("Invalid input for Port")
    else:
        port_ini = int(port)
        port_fin = int(port)+1
    if(Verbose):
        print("Connection established with {}".format(socket.gethostbyname(ip)))
        print("Scanning ports {}-{}\n".format(port_ini, port_fin-1))
    while(port_ini < port_fin):
        if(flag=="CREATE"):
            counter+=1
            pini = port_ini
            if(port_ini+inc < port_fin):
                pfin = pini+inc
                port_ini = pfin
            else:
                pfin = port_ini+(port_fin-port_ini)
                port_ini= pfin
            t= threading.Thread(target=scan, args=(ip, pini, pfin,))
            threads.append(t)
            t.start()
            if(counter>=128):
                flag="DESTROY"
        elif(flag=="DESTROY"):
            for index,thread in enumerate(threads):
                thread.join()
                counter-=1
                if(counter<=0):
                    flag="CREATE"
                    threads=[]
    for index, thread in enumerate(threads):
        thread.join()
    end_time=time.time()
    active_indices=sorted(active_ports)
    for i in active_indices:
        sen=str(i)+"/"+str(active_ports[i])
        senx = sen.ljust(30)
        print(senx,"Open")
    if(Verbose):
        print("\n[^_^] Scan completed in {:.2f} seconds".format(end_time-start_time))
def scan(ip,pini,pfin):
    for i in range(pini, pfin):
        ip = socket.gethostbyname(ip)
        try:
#            print("Connecting to Port {}".format(i))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res=s.connect_ex((ip,i))
            if(res==0):
#                print("[*] Port {}/{} \t open".format(i,socket.getservbyport(i)))
                active_ports[i]=socket.getservbyport(i)
            s.close()
        except KeyboardInterrupt:
            print("Keyboard Interrupt Detected. Exiting...")
            sys.exit(1)
        except socket.gaierror:
            print("Hostname couldn't be resolved. Exiting...")
            sys.exit(1)
        except socket.error:
#            print("Server not responding. Exiting...")
            sys.exit(1)
