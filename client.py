import socket
import constants

# create a socket object
s = socket.socket()

# define the port on which you want to connect
port = constants.port

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server
print(s.recv(1024))
# Close the connection
s.close()