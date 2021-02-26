import socket

ipAddress = input("Enter the ip address of the server you want to connect to : ")
port = int(input("Enter the port number : "))
host=(ipAddress,port)

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(str.encode("Connection Status Acknowledged"),host)
mess=s.recvfrom(1024)
msg=mess[0]
msg=msg.decode()
addr=mess[1]
print("Message: ",msg)
status="send"
while(True):
	if(status=="send"):
#		print("send: ",end='')
		msg=input()
		s.sendto(msg.encode(),host)
		if('oVeR' in msg):
			status='recv'
		if('QuiT' in msg):
			break
	elif(status=='recv'):
		print("recv: ",end='')
		mess=s.recvfrom(1024)
		addr=mess[1]
		msg=mess[0]
		msg=msg.decode()
		if("oVeR" in msg):
			status='send'
		print(msg.replace('oVeR',''))
		if('QuiT' in msg):
			break
s.shutdown(socket.SHUT_RDWR)
s.close()
