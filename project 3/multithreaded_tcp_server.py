import logging
import time
import threading
import concurrent.futures
import socket
from signal import signal, SIGINT
from sys import exit
import random

global prog_status

def handler(signal_recv, frame):
	global prog_status
	s.send(str.encode(exit_str))
	prog_status="stop"
	print('SIGINT or Ctrl-C detected. Exiting gracefully...')
	exit(0)

def send_msg(s):
	while(True):
		if(prog_status == "run"):
#			print("send:",end=' ')
			msg=input()
			s.send(msg.encode())
		else:
			exit(0)
			break
#			exit(0)
	return(0)
def recv_msg(s):
	global prog_status
	while(True):
		if(prog_status == "run"):
			msg=s.recv(1024)
			if(msg):
				msg=msg.decode()
				if(exit_str in msg):
					prog_status="stop"
					exit(0)
				print("recv:  ",end='')
				print(str(msg))
		else:
			exit(0)
			break
	return(0)

if __name__=='__main__':
	prog_status="run"
	host='127.0.0.1'
	port=7777

	s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',port))

	s.listen(5)

	conn, address = s.accept()

	#logging format
	format= "%(asctime)s: %(message)s "
	logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

	logging.info(str(address[0])+' established a connection with GD multithreaded chat server')

	#exiting procedure
	exit_str=''
	for i in range(16):
		exit_str+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
	print("Session Termination String: ",exit_str)

	#exiting configuration for server and client
	conn.send(str.encode(exit_str))
	ack=conn.recv(1024)
	if(ack.decode()!='DoNe'):
		print('Error Config')
		exit(0)

	conn.send(str.encode("You are now connected to GD multithreaded chat server"))

	msg=conn.recv(1024)
	print(msg.decode())

#	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#		executor.map(thread_function, range(3))

	print('\n'+('='*20)+'Chat Session starts'+('='*20)+'\n')
	sen = threading.Thread(target=send_msg, args=(conn,),daemon=False)
	recv= threading.Thread(target=recv_msg, args=(conn,),daemon=True)

	sen.start()
	recv.start()

	signal(SIGINT, handler)

#	sen.join()
#	recv.join()

	s.shutdown(socket.SHUT_RDWR)
	s.close()
