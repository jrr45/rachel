import socketserver
import json
import queue
import time

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    client_list = set()
    client_to_send = ("", 0)
    signal_sent = False
    signal_queue = queue.Queue()
    signal_time = time.Time()
    signals_recieved = set()
    
    def send_signal(self):
        if (self.signal_queue.empty()):
            return
        self.client_to_send = self.signal_queue.get(block=False)
        self.signal_sent = False
        self.signals_recieved = set()
        self.request.sendto(json.dumps({'command' : 'want_you_to_send'}), self.client_to_send)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        parsed_json = json.load(self.data)
        
        if(parsed_json['request'] == "register"):
            self.client_list.add(self.client_address)
            self.signal_queue(self.client_address)
            self.request.sendto(json.dumps({'command' : 'registered'}), self.client_address)
            
        if(parsed_json['request'] == "start"):
            self.send_signal()
            
        if(parsed_json['request'] == "ready_to_send"):
            if (self.client_address == self.client_to_send):
                self.signals_recieved = set()
                self.request.sendto(json.dumps({'command' : 'send_signal'}), self.client_to_send)
                
        if(parsed_json['request'] == "signal_sent"):
            self.signal_sent = True
            self.time.signal_time = time.time(parsed_json['time_sent'])
            
        if(parsed_json['request'] == "signal_recieved"):
            self.signals_recieved.add((self.client_address, parsed_json['time_recieved']))
            if (len(self.signals_recieved)-1 == len(self.client_list)):
                self.process_times()
                time.sleep(1)
                self.send_signal()
        else:
        # just send back the same data with error
            self.request.sendto({'command' : 'invalid_request', 
                                 'request' : parsed_json['request']}, self.client_address)
    
    def process_times(self):
        print(self.signal_time)
        print(self.signals_recieved)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
