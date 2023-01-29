# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 17:04:33 2021

@author: afugur
"""

from scipy.signal import butter, lfilter
from scipy import signal

def butter_bandpass_filter(data, lowcut, highcut,fs= 200, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def butter_highpass_filter(data, lowcut, highcut,fs= 200, order=3):
    global y
    sos = butter(lowcut, highcut, 'hp', fs=200, output='sos')
    y = signal.sosfilt(sos, data)
    return y
