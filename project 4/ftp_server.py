from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
import getpass

authorizer = DummyAuthorizer()
username=input()
password=getpass.getpass()
#Each letter in perm parameter signifies a specific functionality
authorizer.add_user('username','password','.',perm='elradfmw')
#authorizer.add_anonymous('os.getcwd()',perm='elradfmw')

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("192.168.1.9",1470),handler)
server.serve_forever()
