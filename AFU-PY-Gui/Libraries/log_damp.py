# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 01:02:46 2021


This function calculate damping of the time series with Logarithmic Decrement Method

inputs
---------------

Data : stream data, stream
mods : modal frequencies , float array
samples = window samples, int
overlap = overlap, float
length : Over of the max displacement, int
    
outputs
---------------

damp_ratio = damping ratio, float (%)

@author: afugur
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

def dampLog(data,mods,fs=200,samples=1024,overlap=0.33,length=500):
    n_Data = data.copy()
    f_Data = pd.DataFrame()
    
    columns = n_Data.columns
    print(columns)
    log_df = pd.Series(dtype=float)
    log_data = pd.Series(dtype=float)
    log_damp = pd.Series(dtype=float)
    
    
    log_list = []
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
            
            log_df["channel {0} - mod {1}".format(a+1,narrow+1)] = out.argmax()
            log_data["channel {0} - mod {1}".format(a+1,narrow+1)] = out[log_df["channel {0} - mod {1}".format(a+1,narrow+1)]:log_df["channel {0} - mod {1}".format(a+1,narrow+1)]+length]
            

            peaks, _ = find_peaks(log_data["channel {0} - mod {1}".format(a+1,narrow+1)], height=0)
            
            try:
                
                log1 = math.log(log_data["channel {0} - mod {1}".format(a+1,narrow+1)][peaks[0]]/log_data["channel {0} - mod {1}".format(a+1,narrow+1)][peaks[-1]])
            
                log2 = math.log(log_data["channel {0} - mod {1}".format(a+1,narrow+1)][peaks[0]]/log_data["channel {0} - mod {1}".format(a+1,narrow+1)][peaks[-1]]) + pow(2*math.pi,2)
            
                log_list.append(math.sqrt(abs(log1 / log2)) / len(peaks)*100)
                
            except IndexError:
                pass
            # log_damp["channel {0} - mod {1}".format(a+1,narrow+1)] = math.sqrt(abs(log1 / log2)) / len(peaks)
            
            # log_damp["channel {0} - mod {1}".format(a+1,narrow+1)] = log_damp["channel {0} - mod {1}".format(a+1,narrow+1)] * 100
            
            # log_damp["channel {0} - mod {1}".format(a+1,narrow+1)] = log_damp["channel {0} - mod {1}".format(a+1,narrow+1)].round(3)
                
    log_list = np.asarray(log_list)
    max_damp = []
    columns_df = []
    for narrow in range(len(mods)):
        
        max_damp.append(log_list[narrow*len(columns):len(columns)+narrow*len(columns)].max())
        columns_df.append("mod {}".format(narrow+1))
        
    
    max_damp = np.asarray(max_damp)
    max_damp = max_damp.reshape(1,len(mods))
    
    damp_ratio = pd.DataFrame(data=max_damp,columns=columns_df) 
    return damp_ratio
            