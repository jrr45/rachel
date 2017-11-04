#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 15:37:07 2017

@author: jcalbert
"""

MULTICAST_ADDR = ('224.0.0.1',8005)

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class MulticastListener(DatagramProtocol):
    def startProtocol(self):
        print 'Started Listening'

        self.transport.joinGroup(MULTICAST_ADDR[0])

    #Run when data comes in
    def datagramReceived(self, datagram, address):
        #For now, just print
        print datagram
#        #eventually, decide:
         # see if this is an "I will send" message or an "I received" message
         # process that data

#Run the listener
reactor.listenMulticast(MULTICAST_ADDR[1], MulticastListener())
reactor.run()


class MulticastSender(DatagramProtocol):
    pass

sender = reactor.listenUDP(0, MulticastSender())
sender.write('test message',MULTICAST_ADDR)
