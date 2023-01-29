# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 23:22:54 2022

@author: PC
"""

from scipy.fftpack import fft
from scipy.signal import spectrogram, hanning
from scipy import signal
import obspy
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from Libraries.omegaArithmetic import intf
import math
from Libraries import filter_function


def calcModeShape(data,mods,fs=200):
    
    columns = data.columns
    f_Data = pd.DataFrame()
    modeshape_df = pd.DataFrame()
    for narrow in range(len(mods)):
        for a in range(len(columns)):
            f = filter_function.butter_bandpass_filter(data[columns[a]], mods[narrow] - 0.2, mods[narrow] + 0.2,fs=fs)
            f_Data["channel {0} - mod {1}".format(a,narrow+1)] = f

            read = intf(f_Data["channel {0} - mod {1}".format(a,narrow+1)],
                 int(fs),
                 f_lo=0.0 , f_hi=1.0e12 , 
                 times=2 , winlen=1 
                 , unwin=False)
            
            out = read
            modeshape_df["channel {0} - mod {1}".format(a+1,narrow+1)] = out
    

    max_valuesdf = pd.DataFrame()
    min_valuesdf = pd.DataFrame()    
    
    for i in range(len(mods)):
            
            max_out = np.array(modeshape_df.max())
            max_indexout = np.array(modeshape_df.idxmax())
                    
            maxvalue = max_out[len(columns) * (i):len(columns) * (i+1)].max()
            maxindexes = max_out[len(columns) * (i):len(columns) * (i+1)].argmax()
            maxindex = max_indexout[i*len(columns)]
            
            
            min_out = np.array(modeshape_df.min())
            min_indexout = np.array(modeshape_df.idxmin())
                    
            minvalue = min_out[len(columns) * (i):len(columns) * (i+1)].min()
            minindexes = min_out[len(columns) * (i):len(columns) * (i+1)].argmin()
            minindex = min_indexout[i*len(columns)] 
            
            maxvalues = modeshape_df.values[maxindex]
            minvalues = modeshape_df.values[minindex]
            
    
            max_valuesdf["mod {}".format(i+1)]=maxvalues[len(columns) * (i):len(columns) * (i+1)]
            min_valuesdf["mod {}".format(i+1)]=minvalues[len(columns) * (i):len(columns) * (i+1)]
    
    
    min_valuesdf = min_valuesdf.set_index(columns)
    max_valuesdf = max_valuesdf.set_index(columns)
     
    return max_valuesdf,min_valuesdf