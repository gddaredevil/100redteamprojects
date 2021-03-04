import socket
import logging
class tcp_connect:
    def __init__(self, ip ,port):
        self.ip = ip
        self.port=int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.format = "%(asctime)s : %(message)s"
        logging.basicConfig(format=self.format, level=logging.INFO, datefmt="%H:%M:%S")
    def serv(self):
        self.sock.bind(('',self.port))
        print("TCP server is up and listening")
        self.sock.listen(5)
        conn, address = self.sock.accept()
        logging.info("Client at {} established a connection successfully".format(list(address)[0]))
    def cli(self):
        self.sock.connect((self.ip,self.port))
        logging.info("Connecting to the server at {} through port {}...".format(self.ip,self.port))
    def __del__(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
