import socketserver
import json

SERVERHOST, SERVERPORT = "localhost", 9998

class MyTCPHandler(socketserver.BaseRequestHandler):
    registered = False
    server_address = ()
    
    def play_sound():
        pass
    
    def wait_for_signal():
        pass
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        
        parsed_json = json.load(self.data)
        
        if(parsed_json['command'] == "want_you_to_send"):
            if (not self.registered):
                self.finish()
                return
            self.request.sendto(json.dumps({'request' : 'ready_to_send'}), self.client_to_send)
            
        if(parsed_json['command'] == "send_signal"):
            if (not self.registered):
                self.finish()
                return
            time_sent = self.play_sound()
            self.request.sendto(json.dumps({'request' : 'signal_sent',
                                            'time_sent' : time_sent}), self.client_to_send)
            
        if(parsed_json['command'] == "wait_for_signal"):
            if (not self.registered):
                self.finish()
                return
            time_recieved = wait_for_signal()
            self.request.sendto(json.dumps({'request' : 'signal_recieved',
                                            'time_recieved' : time_recieved}), self.client_to_send)
            
        if(parsed_json['command'] == "registered"):
            self.registered = True
        else:
            print("Received: {}".format(self.data))
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        
        server.serve_forever()
