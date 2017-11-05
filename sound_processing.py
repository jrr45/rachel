import numpy as np
import scipy.signal as signal

import matplotlib.pyplot as plt
from matplotlib import gridspec

import pyaudio
import wave
import struct

def make_linear_sine_chirp(f1, f2, rate, nframes, gain):
    """ make chirp linear in frequency starting
        at f1 and ending at f2 """
    n = np.arange(nframes)
    fa = (f2-f1)/float(2*nframes)
    wc = 2*np.pi*(f1+fa*n)/float(rate)
    return gain*np.sin(wc*n)

def audio_signal_listener(RECORD_SECONDS,RATE=44100,CHUNKSIZE=1024,CHANNELS=2):

    FORMAT=pyaudio.paInt16

    # initialize portaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNKSIZE)

    frames = [] # A python-list of chunks(np.ndarray)
    for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
        data = stream.read(CHUNKSIZE)
        frames.append(np.fromstring(data, dtype=np.int16))

    #Convert the list of numpy-arrays into a 1D array (column-wise)
    numpydata = np.hstack(frames)

    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    return numpydata

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
            nframes = int(T*rate)
            template = make_linear_sine_chirp(f1, f2, rate, nframes, gain)
            win = signal.get_window(self.win_type, nframes)
        else:
            raise Exception('Wrong input. Mode has to be "linear_chirp".')
        self.template = template*win

    def match_filter(self, data):
        return np.correlate(data, self.template, mode='same')

    def get_detection_time(self, data):
        # returns in seconds  from start of data
        max_corr = self.match_filter(data)
        dect_time = np.argmax(max_corr)/float(self.rate)
        return dect_time*self.rate

if __name__ == '__main__':

    def plot_corr(data, template, corr):
        fig = plt.figure(figsize=(8, 8), tight_layout=True)
        gs = gridspec.GridSpec(3, 1)

        ax1 = plt.subplot(gs[0])
        ax1.plot(np.arange(data.shape[-1]), data)

        ax2 = plt.subplot(gs[1])
        ax2.plot(np.arange(template.shape[-1]), template)

        ax3 = plt.subplot(gs[2])
        ax3.plot(np.arange(corr.shape[-1]), corr)

        plt.show()

    rate = 100
    f1 = 10
    f2 = 20
    T  = 10
    chirp_T = 1
    chirp_nframes = int(chirp_T*rate)
    nframes = int(T*rate)
    pad_size = (nframes-chirp_nframes)/2
    gain = 1000

    f0 = 20
    w0 = 2*np.pi*f0/float(rate)
    noise = 1000*np.random.random(nframes)
    data = np.zeros(nframes)
    pp = 200
    data[pad_size-pp:-pad_size-pp] = make_linear_sine_chirp(f1, f2, rate, chirp_nframes, gain)
    #data[pad_size:-pad_size] = gain*np.sin(w0*np.arange(chirp_nframes))
    data += noise

    chirp_params = {'f1':f1, 'f2':f2, 'T':chirp_T, 'gain':gain}

    det = SoundDetector(rate, win_type='hann') # window type in scipy
    det.make_template(chirp_params, mode='linear_chirp')

    print det.get_detection_time(data)

    template = det.template

    corr = det.match_filter(data)

    print data.shape, template.shape, corr.shape

    plot_corr(data, template, corr)