### Day 2
These files emulate a half duplex UDP connection.

Make sure to install socket module for python. It comes with every python installation by default. Due to any issues, if running the script displays the error message: "No module named socket" or something similar, install the module with the command 

`pip3 install socket`

The word `oVeR` is used to shift the turns of being the sender and receiver.
The word `QuiT` is used to end the current session of communication.

udp_server.py assigns the specified ip address to the server and listens on the specified port for incoming connections. 
udp_client.py makes a connection request to the server with the specified ip address through the specified port.

Assign the loopback address 127.0.0.1 for the server or your local ip address assigned by the DHCP server. The communication can happen only inside a local network with these programs. Communication between different networks isn't possible.
As it is a UDP connection. Three-way handshake and connection overhead won't be necessary. But, UDP is not a reliable form of transmission for important information.


