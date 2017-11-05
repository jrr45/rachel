import numpy as np
import scipy.signal as signal

import pyaudio

def make_linear_sine_chirp(f1, f2, rate, nframes, gain):
    """ make chirp linear in frequency starting
        at f1 and ending at f2 """
    n = np.arange(nframes)
    fa = (f2-f1)/float(2*nframes)
    wc = 2*np.pi*(f1+fa*n)/float(rate)
    return gain*np.sin(wc*n)

class SoundProcessor(object):
    def __init__(self, rate=44100, channels=1, 
                 chunksize=1024, data_format=pyaudio.paInt16):
        self.rate = rate
        self.data_format = data_format
        self.channels = channels
        self.chunksize = chunksize

        if self.data_format == pyaudio.paInt16:
            self.dtype = np.int16
        else:
            raise Exception('data_format has to be pyaudios paInt16')

        self.p = pyaudio.PyAudio()

    def audio_signal_listener(self, record_seconds):
        lstream = self.p.open(format=self.data_format,
                              channels=self.channels,
                              rate=self.rate,
                              input=True,
                              frames_per_buffer=self.chunksize)

        frames = [] # A python-list of chunks(np.ndarray)
        for _ in range(0, int(self.rate/self.chunksize*record_seconds)):
            data = lstream.read(self.chunksize)
            frames.append(np.fromstring(data, dtype=self.dtype))

        #Convert the list of numpy-arrays into a 1D array (column-wise)
        numpydata = np.hstack(frames)

        # close stream
        lstream.stop_stream()
        lstream.close()
        #p.terminate()

        return numpydata

    def audio_signal_player(self, data):
        rstream = self.p.open(format=self.data_format,
                         channels=self.channels,
                         rate=self.rate,
                         output=True)

        rstream.write(data.astype(self.dtype).tostring())

        rstream.stop_stream()
        rstream.close()
        #p.terminate()

class SoundDetector(object):
    """ detector makes and stores templates
        for match filtering against the incoming data"""
    def __init__(self, rate, win_type='hann'):
        self.rate = rate
        self.win_type = win_type

    def make_template(self, params, mode='linear_chirp'):
        #params should be a dict
        if mode == 'linear_chirp':
            f1 = params['f1']
            f2 = params['f2']
            T = params['T']
            gain = params['gain']
            nframes = int(T*self.rate)
            template = make_linear_sine_chirp(f1, f2, self.rate, nframes, gain)
            win = signal.get_window(self.win_type, nframes)
        else:
            raise Exception('Wrong input. Mode has to be "linear_chirp".')
        self.template = template*win

    def match_filter(self, data):
        return signal.correlate(data, self.template, mode='same')

    def get_detection_time(self, data):
        # returns in seconds  from start of data
        corr = self.match_filter(data)
        detect_time = np.argmax(corr)/float(self.rate)
        return detect_time

def run_rachel(sound_processor, detector, produce_sound, parsed, 
               rate, gain, buffer_time):
    if produce_sound:
        tot_nframes = int((parsed['T']+parsed['start_T'])*rate)
        nframes = int(parsed['T']*rate)
        pad_size = tot_nframes-nframes
        data = np.zeros(tot_nframes)

        data[pad_size:] = make_linear_sine_chirp(parsed['f1'], 
                                                 parsed['f2'], 
                                                 rate, 
                                                 nframes,
                                                 gain)

        sound_processor.audio_signal_player(data)
        time_of_detection = None
    else:
        record_seconds = parsed['T']+parsed['start_T']+buffer_time

        #starts the audio listener
        data = sound_processor.audio_signal_listener(record_seconds)

        print('calculating the detection time ... ')
        time_of_detection = detector.get_detection_time(data)
        print('detection time =', time_of_detection)

    return time_of_detection