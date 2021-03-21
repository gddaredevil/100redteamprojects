import socket
import threading
import sys
import logging
import time
from signal import signal

logging.basicConfig(format="    %(asctime)s : %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

def getIP():
    try:
        return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except:
        return(socket.gethostbyname(socket.gethostname()))
def send(s):
    while(True):
        msg=input()
        s.send(msg.encode())

def recv(s):
    while(True):
        msg = s.recv(1024)
        if not msg:
            break
        print(msg.decode())

def signal_handler(sign_recv, frame):
    print("Level 2")

def listen(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip=getIP()
    s.bind((ip, int(port)))
    s.listen(5)
    stat, conn = s.accept()
    print('{} established a connection through port {}'.format(conn[0],conn[1]))
    sen = threading.Thread(target=send, args=(stat,), daemon=False)
    rec = threading.Thread(target=recv, args=(stat,), daemon=False)
#    sen.daemon=True#    rec.daemon=True
    sen.start()
    rec.start()

def connect(ip, port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    print("Connection Successful")
    sen = threading.Thread(target=send, args=(s,), daemon=False)
    rec = threading.Thread(target=recv, args=(s,), daemon=False)

    sen.start()
    rec.start()

def portScan(ip, port):
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
    print("[^_^] Scan completed in {:.2f} seconds".format(end_time-start_time))
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
            print('')
            sys.exit(1)


