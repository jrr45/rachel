#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:37:07 2017

@author: jcalbert
"""

"""
MSG TYPES:

1: I am sending a signal

2: I recieved a signal    
    
"""




MULTICAST_ADDR = ('224.0.0.1',8005)

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
from time import time
import sys

class MulticastListener(DatagramProtocol):
    def startProtocol(self):

        self.transport.setTTL(5)
        self.transport.joinGroup(MULTICAST_ADDR[0])

        print('Announcing start')
        msg = "Came online at: {}".format(repr(time()))
        
        self.transport.write(msg.encode(), MULTICAST_ADDR)

        print('Started Listener')

    #Run when data comes in
    def datagramReceived(self, datagram, address):
        #For now, just print
        print("Got data from {} at local time: \n{}".format(address, repr(time())))
        print("Data: {}".format(datagram))
        print("-"*40)
#        #eventually, decide:
         # see if this is an "I will send" message or an "I received" message
         # process that data
         
class MulticastSender(DatagramProtocol):  
    def startProtocol(self):
        self.transport.setTTL(5)

    pass


if sys.argv[-1] == '-s':
    print("Starting listener")
    reactor.listenMulticast(MULTICAST_ADDR[1], MulticastListener())
    reactor.run()

elif sys.argv[-1] == '-c':
    assert(0)
    print("Starting sender")
    sender = reactor.listenUDP(0, MulticastSender())
    sender.write(repr(time()).encode(),MULTICAST_ADDR)
