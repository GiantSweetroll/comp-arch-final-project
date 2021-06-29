from operator import add
import socket
import constants
from _thread import *
from res_maker import handle_request
import threading

def createNewThread(c, addr):
    # Make a variable to contain the threading variable, it will use handle_request as the 
    # function to be run 
    thread = threading.Thread(target=handle_request,args=(c,addr))
    
    # starting the thread
    thread.start()
    

# Create socket object
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
    
    # Set a limit for maximum worker threads into 30 
    if(threading.active_count()-1 <=30):
        # a function to create new worker thread to handle incoming requests
        createNewThread(c,addr)
    
    else:
        print("Maximum connection exceeded")

    
    # Checking the worker threads, it will use the threading active acount function
    # deducted by 1 to exclude the main thread count
    print(f"[ACTIVE CONNECTIONS OR ACTIVE THREADS] {threading.active_count()-1}")
    
    
    