import socket
import constants
from _thread import *
from res_maker import handle_request

def createNewThread(c, addr):
    # Send a thank you message to the client
    c.send(b'Thank you for connecting')

    # Connect to res_maker
    handle_request(c, addr)

    # Close the connection with the client
    c.close

def multiThread(c, addr):
    # The function to create new thread
    start_new_thread(createNewThread, (c, addr))

# Create socket obnject
s = socket.socket()
print("Socket successfully created")

# Configure port
port = constants.port

# Bind the port
s.bind(('', port))
print(f"Socket binded to {port}")

# put the socket into listening mode
s.listen(5)
print("Socket is listening")

while True:
    # Establish connection with client
    c, addr = s.accept()
    print("Got connection from", addr)
    
    # Starting one new thread 
    multiThread(c, addr)
    
    
    