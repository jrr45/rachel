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

    BUFFER_TIME = 5 #maybe make this a command line arg

    #------------------------------

    #COMMUNICATION SHIT GOES HERE
    #WHEN A MESSAGE IS RECEIVED, IT SHOULD
    #CONTAIN (f1, f2, T, when_it_starts)

    #simulating parameters
    f1 = 200
    f2 = 400
    T  = 10
    when_it_starts = 3
    chirp_T = 4
    chirp_nframes = int(chirp_T*RATE)
    nframes = int(T*RATE)
    pad_size = (nframes-chirp_nframes)/2
    gain = 1000

    f0 = 250
    w0 = 2*np.pi*f0/float(RATE)
    noise = 1000*np.random.random(nframes)
    data = np.zeros(nframes)
    pp = 200
    data[pad_size-pp:-pad_size-pp] = sp.make_linear_sine_chirp(f1, f2, RATE, chirp_nframes, gain)
    #data += noise

    p = pa.PyAudio()

    pstream = p.open(format=pa.paInt16,
                     channels=CHANNELS,
                     rate=RATE,
                     output=True)

    pstream.write(data.astype(np.int16).tostring())

    pstream.stop_stream()
    pstream.close()

    p.terminate()

    #------------------------------

    record_seconds = T+when_it_starts+BUFFER_TIME

    #starts the audio listener
    data = sp.audio_signal_listener(record_seconds, RATE=RATE, 
                                                    CHUNKSIZE=CHUNKSIZE, 
                                                    CHANNELS=CHANNELS)

    chirp_params = {'f1':f1, 'f2':f2, 'T':chirp_T, 'gain':gain}
    detector = sp.SoundDetector(RATE, win_type='hann')
    det.make_template(chirp_params, mode='linear_chirp')

    time_of_detection = det.get_detection_time(data)

if __name__ == '__main__':
    main()