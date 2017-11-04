import numpy as np
import scipy.signal as signal

import matplotlib.pyplot as plt
from matplotlib import gridspec

import pyaudio
import wave
import struct

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

def make_linear_sine_chirp(f1, f2, rate, nframes):
    """ make chirp linear in frequency starting
        at f1 and ending at f2 """
    n = np.arange(nframes)
    fa = (f2-f1)/float(2*nframes)
    wc = 2*np.pi*(f1+fa*n)/float(rate)
    return gain*np.sin(wc*n)

class SoundDetector(object):
    
    """ detector makes and stores templates
        for match filtering them against incoming data"""

    def __init__(self, rate, win_type='hamming'):
        self.rate = rate
        self.win_type = win_type

    def make_template(self, params, mode='linear_chirp'):
        if mode == 'linear_chirp':
            f1 = params['f1']
            f2 = params['f2']
            T = params['T']
            gain = params['gain']
            nframes = int(T*rate)
            template = make_linear_sine_chirp(f1, f2, rate, nframes)
            win = signal.get_window(self.win_type, nframes)
        else:
            raise Exception('Wrong input. Mode has to be "linear_chirp".')
        self.template = template*win

    def match_filter(self, data):
        return np.correlate(data, self.template, mode='same')

    def get_detection_time(self, data):
       max_corr = self.match_filter(data)
       dect_time = np.argmax(max_corr)/float(self.rate)
       return dect_time

if __name__ == '__main__':
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
    data[pad_size-pp:-pad_size-pp] = make_linear_sine_chirp(f1, f2, rate, chirp_nframes)
    #data[pad_size:-pad_size] = gain*np.sin(w0*np.arange(chirp_nframes))
    data += noise

    chirp_params = {'f1':f1, 'f2':f2, 'T':chirp_T, 'gain':gain}

    det = SoundDetector(rate, win_type='hann')
    det.make_template(chirp_params, mode='linear_chirp')

    print det.get_detection_time(data)*rate

    template = det.template

    corr = det.match_filter(data)

    print data.shape, template.shape, corr.shape

    plot_corr(data, template, corr)

    """
    width = p.get_sample_size(sformat)

    p = pyaudio.PyAudio()

    stream = p.open(format=sformat,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=nframes)

    frames = []
    for i in range(int(record_time*rate/float(nframes))):
        frames.append(stream.read(nframes))

    stream.stop_stream()
    stream.close()
    p.terminate()
    """

    """

    sig_nframes = 1024

    wc = 2*np.pi/float(rate)
    f1 = 300
    f2 = 600
    n = np.arange(nframes)
    phi = wc*np.linspace(f1, f2, nframes)*n

    sig_data = list(10000*np.sin(phi))

    #add gaussian noise
    noise = 8000*np.random.normal(0.0, 1.0, nframes)
    noisy_data = data + noise

    win_size = 500
    nwins = int(nframes/win_size)
    for w in range(nwins):  
        iidx = w*win_size
        fidx = (w+1)*win_size

        noisy_win = noisy_data[iidx:fidx]
        data_win = data[iidx:fidx]

        corr = np.correlate(noisy_win, data_win, mode='same')

        fig = plt.figure(figsize=(8, 8), tight_layout=True)
        gs = gridspec.GridSpec(3, 1)

        ax1 = plt.subplot(gs[0])
        ax1.plot(noisy_win)

        ax2 = plt.subplot(gs[1])
        ax2.plot(data_win)

        ax3 = plt.subplot(gs[2])
        ax3.plot(corr)

        plt.show()

    """
    """
    rate = 1000
    nframes = 1000
    pad = 2000
    tot_frames = 2*pad+nframes
    w = 2*np.pi*10/float(rate)
    n = np.arange(nframes)

    sig1 = np.zeros(tot_frames)
    sig2 = np.zeros(tot_frames)
    sig1[pad:-pad] = np.cos(w*n)
    sig2[pad:-pad] = np.sin(w*n)
    corr = np.correlate(sig1, sig2, mode='same')

    fig = plt.figure(figsize=(8, 8), tight_layout=True)
    gs = gridspec.GridSpec(3, 1)

    ax1 = plt.subplot(gs[0])
    ax1.plot(sig1)

    ax2 = plt.subplot(gs[1])
    ax2.plot(sig2)

    ax3 = plt.subplot(gs[2])
    ax3.plot(corr)

    plt.show()

    asd
    """

    #plt.plot(data)
    #plt.show()

    """

    output_path = '/home/leoschendes/Desktop'+'/'+output_name

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(width)
    wf.setframerate(rate)
    for x in data:
        pv = struct.pack('h', x)
        wf.writeframes(pv)
    wf.close()

    """