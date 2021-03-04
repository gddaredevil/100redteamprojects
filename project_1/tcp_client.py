import socket

host=input("Enter the ip address of the server you want to connect to : ")
port=int(input("Enter the port number : "))

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

msg=s.recv(1024)
print(msg.decode())
s.send(b"Connection Status Acknowledged")
# Status variable keeps track and synchronises server and client to alternatively act as sender and recepient
status="send"
while(True):
	if(status=="send"):
		print("send: ",end='')
		msg=input()
		s.send(msg.encode())
		if('oVeR' in msg):
			status='recv'
		if('QuiT' in msg):
			break
	elif(status=='recv'):
		print("recv: ",end='')
		msg=s.recv(1024)
		msg=msg.decode()
		if("oVeR" in msg):
			status='send'
		print(msg.replace('oVeR',''))
		if('QuiT' in msg):
			break
s.shutdown(socket.SHUT_RDWR)
s.close()
