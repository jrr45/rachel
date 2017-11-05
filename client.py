from __future__ import print_function

import socket
import json

#SERVERHOST, SERVERPORT = "localhost", 9998

class Client():
    def __init__(self, serverhost="localhost", serverport=999):
        self.registered = False
        self.server_address = ()
        self.SERVERHOST = serverhost
        self.SERVERPORT = serverport
    
    def play_sound(self):
        pass
    
    def wait_for_signal(self):
        pass
    
    def beginlistening(self, start=False):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.SERVERHOST, self.SERVERPORT))
            
            # begin calling
            if (start):
                sock.sendall(json.dumps({'request' : 'start'}))
            
            while(True):
                received = str(sock.recv(1024), "utf-8")
                print("{} wrote:".format(self.client_address[0]))
                
                parsed_json = json.load(received)
                
                if(parsed_json['command'] == "want_you_to_send"):
                    if (not self.registered):
                        self.finish()
                        return
                    sock.sendall(json.dumps({'request' : 'ready_to_send'}))
                    
                if(parsed_json['command'] == "send_signal"):
                    if (not self.registered):
                        self.finish()
                        return
                    time_sent = self.play_sound()
                    sock.sendall(json.dumps({'request' : 'signal_sent',
                                                    'time_sent' : time_sent}))
                    
                if(parsed_json['command'] == "wait_for_signal"):
                    if (not self.registered):
                        self.finish()
                        return
                    time_recieved = self.wait_for_signal()
                    sock.sendall(json.dumps({'request' : 'signal_recieved',
                                                'time_recieved' : time_recieved}))
                
                if(parsed_json['command'] == "registered"):
                    self.registered = True
                else:
                    print("Received: {}".format(self.data))
            
def start_client(serverhost="localhost", serverport=9999, start=False):
    client = Client(serverhost="localhost", serverport=999)
    client.beginlistening(start=False)
