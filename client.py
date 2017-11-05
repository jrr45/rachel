import socket
import sys
import json
import atexit

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])



# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
      if(parsed_json['request'] == "wan_you_to_send"):
            pass
        if(parsed_json['request'] == "signal_sent"):
            pass
        if(parsed_json['request'] == "signal_sent"):
            pass
        else:

print("Sent:     {}".format(data))
print("Received: {}".format(received))
