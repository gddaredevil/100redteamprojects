import socket

host=input("Enter the ip address you want to assign to the server : ")
port=int(input("Enter the port number : "))
connection=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connection.bind((host, port))
print("UDP server is all set and ready!")

mess=connection.recvfrom(1024)
addr=mess[1]
print(addr[0]," established a connection on port ",addr[1]," with GD UDP chat Server")
msg=mess[0]
msg=msg.decode()
print(msg)

connection.sendto(str.encode("You are now connected to the TCP chat session of GD"),addr)
status="recv"
while(True):
	if(status=="recv"):
		print("recv: ",end='')
		mess=connection.recvfrom(1024)
		msg=mess[0]
		msg=msg.decode()
		addr=mess[1]
		if("oVeR" in msg):
			status='send'
		print(msg.replace('oVeR',''))
		if('QuiT' in msg):
			break
	elif(status=="send"):
#		print("send: ",end='')
		msg=input()
		connection.sendto(msg.encode(),addr)
		if('oVeR' in msg):
			status='recv'
		if('QuiT' in msg):
			break
connection.shutdown(socket.SHUT_RDWR)
connection.close()
