"""
This function calculate damping of the time series with Half-Power Method

inputs
---------------

Data : stream data, dataframe
mods : modal frequencies , float array
samples = window samples, int
overlap = overlap, float

outputs
---------------

damp_ratio = damping ratio, float (%)

Created on Mon Oct 25 22:19:35 2021

@author: afugur
"""


from scipy.fftpack import fft
from scipy.signal import spectrogram, hanning
from scipy import signal

import obspy
import pandas as pd
import numpy as np
from Libraries import filter_function

def dampHalf(data,mods,fs=200,samples=1024,overlap=0.33):
    
    columns = data.columns
    f_Data = pd.DataFrame()
    
    for narrow in range(len(mods)):
        
        for a in range(len(columns)):
            f = filter_function.butter_bandpass_filter(data[columns[a]], mods[narrow] - 0.2, mods[narrow] + 0.2,fs=fs)
            f_Data["channel {0} - mod {1}".format(a,narrow+1)] = f
            
        
    M = samples
    NFFT = M
    win = signal.windows.hamming(M)
    overlap_samples = int(round(M*overlap)) # overlap in samples
    
    freq_df = pd.DataFrame()
    mean_df = pd.DataFrame()
    
    
    for narrow in range(len(mods)):
        for a in range(len(columns)):
            
            t, f, S = spectrogram(f_Data["channel {0} - mod {1}".format(a,narrow+1)]
                              ,fs=int(fs)
                              ,window=win
                              ,nperseg=M
                              ,noverlap=overlap_samples,nfft=NFFT)
        
            avg_S1 = np.mean(S,axis=1)
        
            freq_df["Frequencies"] = t
            mean_df["channel {0} - mod {1}".format(a,narrow+1)] = avg_S1

    half_list = []
    
    for narrow in range(len(mods)):
        for a in range(len(columns)):
            # fa
            index_max = mean_df["channel {0} - mod {1}".format(a,narrow+1)].idxmax()
            
            x = [mean_df["channel {0} - mod {1}".format(a,narrow+1)][index_max-1],mean_df["channel {0} - mod {1}".format(a,narrow+1)][index_max]]
            
            y = [freq_df['Frequencies'][index_max-1], freq_df['Frequencies'][index_max]]

            amp_new = (mean_df["channel {0} - mod {1}".format(a,narrow+1)].max()) * 0.707
            
            fa = np.interp(amp_new, x, y)
            # fb
            x2 = [mean_df["channel {0} - mod {1}".format(a,narrow+1)][index_max],
            mean_df["channel {0} - mod {1}".format(a,narrow+1)][index_max+1]]
            y2 = [freq_df['Frequencies'][index_max], freq_df['Frequencies'][index_max+1]]
            
            fb = np.interp(amp_new, x2, y2)
            
            half_damp = (fb-fa) / (fb+fa)
            half_damp = half_damp * 100
            half_list.append(half_damp)
            
            
    half_list = np.asarray(half_list)
    max_damp = []
    columns_df = []
    for narrow in range(len(mods)):
        
        max_damp.append(half_list[narrow*len(columns):len(columns)+narrow*len(columns)].max())
        columns_df.append("mod {}".format(narrow+1))
        
    
    max_damp = np.asarray(max_damp)
    max_damp = max_damp.reshape(1,len(mods))
    
    damp_ratio = pd.DataFrame(data=max_damp,columns=columns_df)
        
    return damp_ratio

