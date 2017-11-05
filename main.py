from __future__ import print_function

import sound_processing as sp
import numpy as np
#import ConfigParser
from multiprocessing import Process

import pyaudio as pa
import wave
import struct
import time

import server
import client

import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--server_address', metavar=('address', 'port'), type=str,
                        nargs=2, help='address of the werbserver')
    args = parser.parse_args()
    
    isserver = False
    serverhost = "localhost"
    serverport = 9999
    if args.server_address:
        isserver = True
        serverhost = args.server_address[0]
        serverport = args.server_address[1]
    
    #config = ConfigParser.ConfigParser()
    #config.readfp(open('global.ini'))

    RATE = 3000#config.getint('global', 'BITRATE')
    CHUNKSIZE = 1000#config.getint('global', 'CHUNKSIZE')
    CHANNELS = 3000#config.getint('global', 'CHANNELS')

    BUFFER_TIME = 2 #maybe make this a command line arg
    GAIN = 1000

    produce_sound = True
    network_is_active = True

    #------------------------------

    #COMMUNICATION SHIT GOES HERE
    #WHEN A MESSAGE IS RECEIVED, IT SHOULD
    #CONTAIN (f1, f2, T, when_it_starts)

    #simulating parameters
    f1 = 2000
    f2 = 4000
    T = 0.5
    start_T = 1
    #------------------------------

    parsed = {'f1':f1, 'f2':f2, 'T':T, 'start_T':start_T}

    sound_processor = sp.SoundProcessor(rate=RATE, 
                                        channels=CHANNELS, 
                                        chunksize=CHUNKSIZE)
    chirp_params = {'f1':parsed['f1'], 
                    'f2':parsed['f2'], 
                    'T':parsed['T'], 
                    'gain':GAIN}
    detector = sp.SoundDetector(RATE, win_type='hann')
    detector.make_template(chirp_params, mode='linear_chirp')

    if (isserver):
        p = Process(target=server.start_server)
        p.start()
        p.join()
        input('Press Enter to start calling: ')
            
    client.start_client(serverhost, int(serverport), start=isserver)

if __name__ == '__main__':
    main()