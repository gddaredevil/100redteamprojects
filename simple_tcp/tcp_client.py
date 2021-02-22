import socket

host = '127.0.0.1' #Localhost
port = 7777 #random unreserved port

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.AF_INET means it will use ipv4 type ip address
#sock.SOCK_STREAM means it will use TCP/IP protocol for data transmission
#sock.SOCK_DGRAM means it will use UDP protocol for data transmission

s.connect((host,port))
#It connects to the mentioned ip address through the specified port

msg=s.recv(1024)
#Any messages sent by server are received in chunks of 1024 bytes

while msg:
	print("Received Message: "+msg.decode())
	msg=s.recv(1024)

#As long as messages are incoming, the loop keeps on running and receiving messages

s.close()
#close the socket connection in the end
