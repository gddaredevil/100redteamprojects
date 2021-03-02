import socket

host=input("Enter the ip address you want to assign to the server : ")
port=int(input("Enter the port number: "))

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))

s.listen(5)

connection, address = s.accept()

print(address[0]," established a connection with GD TCP chat")

connection.send(b"You are now connected to the TCP chat session of GD")
msg=connection.recv(1024)
print(msg)
status="recv"
while(True):
	if(status=="recv"):
		print("recv: ",end='')
		msg=connection.recv(1024)
		msg=msg.decode()
		if("oVeR" in msg):
			status='send'
		print(msg.replace('oVeR',''))
		if('QuiT' in msg):
			break
	elif(status=="send"):
		print("send: ",end='')
		msg=input()
		connection.send(msg.encode())
		if('oVeR' in msg):
			status='recv'
		if('QuiT' in msg):
			break
s.shutdown(socket.SHUT_RDWR)
s.close()
