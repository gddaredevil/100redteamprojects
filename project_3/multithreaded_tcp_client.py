import socket
import logging
import time
import threading
import concurrent.futures
from signal import signal, SIGINT
from sys import exit

global prog_status

def handler(signal_recv, frame):
	global prog_status
	print('SIGINT or Ctrl-C detected. Exiting gracefully...')
	s.send(str.encode(exit_str))
	prog_status="stop"
	exit(0)

def send_msg(s):
	while(True):
		if(prog_status=="run"):
#			print('send :',end=' ')
			msg=input()
			s.send(msg.encode())
		else:
			break
			exit(0)

def recv_msg(s):
	global prog_status
	prog_status="run"
	while(True):
#		if(prog_status =="run"):
		if(1==1):
			msg=s.recv(1024)
			if(msg):
				msg=msg.decode()
				if(exit_str in msg):
					prog_status="stop"
					print("Server ended the session. Reconnect again if you want to continue the session")
					exit(0)
				print("recv:  ",str(msg))
		else:
			break
			exit(0)
if __name__=='__main__':
	global prog_status
	prog_status="run"
	host='192.168.1.6'
	port=7777
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((host,port))

	#logging format
	format = "%(asctime)s:%(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

	exit_str=s.recv(1024)
	exit_str=exit_str.decode()
	s.send(str.encode('DoNe'))
	msg=s.recv(1024)
	print(msg.decode())
	s.send(str.encode("Initiating a Chat Session..."))

	print('\n'+('='*20)+"Chat Session starts"+('='*20)+'\n')
	sen = threading.Thread(target=send_msg, args=(s,),daemon=False)
	recv= threading.Thread(target=recv_msg, args=(s,),daemon=False)

	sen.start()
	recv.start()

	signal(SIGINT, handler)

	#sen.join()
	#recv.join()

	s.shutdown(socket.SHUT_RDWR)
	s.close()
