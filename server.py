import socket
import constants

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

    # Send a thank you message to the client
    c.send(b'Thank you for connecting')

    # close the connection with the client
    c.close()