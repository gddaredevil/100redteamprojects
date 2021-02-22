import socket

host='127.0.0.1'
port=7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',port))
#Assign the specified port to server socket to listen for connections

s.listen(5)
#listen for a maximum of 5 connections before quitting

connection, address = s.accept()
#accept() returns two values: connection status and ip address of the client connected

print(address[0]," established a connection with the Server")

connection.send(b"You are now connected to the TCP server by GD_DAREDEVIL\n")
#A welcome message configured to be sent to every client on making a connection

msg="This is how a simple TCP server and client communication happens. Server binds itself to an ip address and a port and keeps listening for the incoming connections.\nClient sends a connection request to the server and boom, They are connected.\nTCP mode of transmission is reliable as it is connection-oriented."
connection.send(msg.encode())
#message has to be encoded into bitstreams before sending

connection.close()
