import socket
import subprocess
import os
import threading
import sys
import logging
import time
import signal
import random
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


global block_size

logging.basicConfig(format="    %(asctime)s : %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
global INT_STAT
INT_STAT="RUN"
def getIP():
    try:
        return([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    except:
        return(socket.gethostbyname(socket.gethostname()))

def diffieHellman(s):
    low_lim=1
    up_lim =999999
    P=random.randint(low_lim, up_lim)
    G=random.randint(low_lim, up_lim)
    int_var = random.randint(low_lim, 200)
    var = (G**int_var)%P
    s.send((str(var)+":"+str(P)+":"+str(G)).encode())
    recvar = (s.recv(1024)).decode()
    key = (int(recvar)**int_var)%P
    return(key)

def Diffiehellman(s):
    int_var = random.randint(1, 200)
    rec_var = s.recv(2048).decode()
    rec_var = rec_var.split(':')
    P=int(rec_var[1])
    G=int(rec_var[2])
    recKey=int(rec_var[0])
    var = (G**int_var)%P
    s.send(str(var).encode())
    key=(int(recKey)**int_var)%P
    return(key)


def AESCipher(key):
    global block_size
    block_size = AES.block_size
    keyHash = hashlib.sha256(str(key).encode()).digest()
    return(keyHash)
def padding(stat,text):
    global block_size
    if(stat=="pad"):
        bytes_to_pad= block_size - len(text) % block_size
        ascii_string = chr(bytes_to_pad)
        pad_str = str(ascii_string)*bytes_to_pad
        final_str = text+pad_str
        return(final_str)
    elif(stat=="unpad"):
        text=text.decode()
        pad_char = text[-1]
        for i in range(1,len(text)):
            if(text[i]==pad_char):
                ind = i
                break
        return(text[:ind])
def crypt(stat, text, key):
    global block_size
    if(stat=="enc"):
        padtxt = padding("pad",text)
        iv = Random.new().read(block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        enc_text = cipher.encrypt(padtxt.encode())
        return(b64encode(iv+enc_text).decode("utf-8"))
    elif(stat=="dec"):
        enc_text = b64decode(text)
        iv = enc_text[:block_size]
        cipher=AES.new(key, AES.MODE_CBC, iv)
        padtxt = cipher.decrypt(enc_text[block_size:])
        return(padding("unpad", padtxt))


def send(s,key):
    key = AESCipher(key)
    global INT_STAT
    while(True):
        try:
            if(INT_STAT=="STOP"):
                break
            else:
                msg=input()
                msg = crypt("enc",msg, key)
                s.send(msg.encode())
        except:
            sys.exit(1)
            INT_STAT="STOP"
def recv(s,key):
    key = AESCipher(key)
    global INT_STAT
    while(True):
        try:
            if(INT_STAT =="STOP"):
                break
            else:
                msg=s.recv(1024)
                msg = msg.decode()
                msg = crypt("dec",msg,key)
            if(msg == b''):
                raise RuntimeError("SOCKET Connection Broken...")
                sys.exit(1)
            print(msg)
        except:
            sys.exit(1)
            INT_STAT="STOP"

def spawn(s):
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
    key = diffieHellman(stat)
    if(fpath==None):
        if(Verbose):
            print("\U0001F609",end=" ")
            print('{} established a connection through port {}'.format(conn[0],conn[1]))
        sen = threading.Thread(target=send, args=(stat,key,), daemon=False)
        rec = threading.Thread(target=recv, args=(stat,key,), daemon=False)
    #    sen.daemon=True
    #    rec.daemon=True
        sen.start()
        rec.start()
    else:
        print("Spawning a Shell...")
        rec=threading.Thread(target=spawn, args=(stat,),daemon=False)
        rec.start()

def connect(ip, inp_file, port, Verbose):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,port))
    if(Verbose):
        print("Connection Successful through port {}".format(port))
    key=Diffiehellman(s)
    if(inp_file==None):
        sen = threading.Thread(target=send, args=(s,key,), daemon=False)
        rec = threading.Thread(target=recv, args=(s,key,), daemon=False)
        sen.start()
        rec.start()
    else:
        s.send(inp_file.encode())

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
