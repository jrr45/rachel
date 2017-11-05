import sound_processing as sp
import numpy as np
import ConfigParser

import pyaudio as pa
import wave
import struct
import time

def main():
    config = ConfigParser.ConfigParser()
    config.readfp(open('global.ini'))

    RATE = config.getint('global', 'BITRATE')
    CHUNKSIZE = config.getint('global', 'CHUNKSIZE')
    CHANNELS = config.getint('global', 'CHANNELS')

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

    while network_is_active:
        time_of_detection = sp.run_rachel(sound_processor, detector, produce_sound, 
                                                    parsed, RATE, GAIN, BUFFER_TIME)
        time.sleep(1)
        print time_of_detection

if __name__ == '__main__':
    main()