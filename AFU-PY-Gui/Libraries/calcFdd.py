import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

def calcFDD(self,data,fs,ff,prominence=30,overlap=66,window="hann",ndf=3):
    
    freqs = pd.DataFrame()
    df = pd.Series(dtype=float)
    df2 = pd.DataFrame()

    number_channels=data.shape[1] # Number of channels
    freq_max = fs/2 # Nyquist frequency
    number_segments = fs/ff # number of point per segments
    overlap = overlap /100
    noverlap = number_segments // (1/overlap) # Number of overlapping points


    PSD_matr = np.zeros((number_channels, number_channels, int((number_segments)/2+1)), dtype=complex) 
    S_val = np.zeros((number_channels, number_channels, int((number_segments)/2+1))) 
    S_vec = np.zeros((number_channels, number_channels, int((number_segments)/2+1)), dtype=complex) 


    # Calculating Auto e Cross-Spectral Density
    for _i in range(0, number_channels):
        for _j in range(0, number_channels):
            _f, _Pxy = signal.csd(data[:, _i],data[:, _j], fs=fs, nperseg=number_segments, noverlap=noverlap, window=window)
            PSD_matr[_i, _j, :] = _Pxy
        
    for _i in range(np.shape(PSD_matr)[2]):
        U1, S1, _V1_t = np.linalg.svd(PSD_matr[:,:,_i])
        U1_1=np.transpose(U1) 
        S1 = np.diag(S1)
        S_val[:,:,_i] = S1
        S_vec[:,:,_i] = U1_1
        
    for _i in range(number_channels):
        
        self.fd.plot(_f[:], 10*np.log10(S_val[_i, _i])) # decibel #Amplitude verileri
        
        self.fd.set_xlim(left=0, right=freq_max)
        self.fd.xaxis.set_major_locator(MultipleLocator(freq_max/10))
        self.fd.xaxis.set_major_formatter(FormatStrFormatter('%g'))
        self.fd.xaxis.set_minor_locator(MultipleLocator(freq_max/100))
        self.fd.set_title("Singular values plot - (Freq. res. ={0})".format(ff))
        self.fd.set_xlabel('Frequency [Hz]')
        self.fd.set_ylabel(r'dB $[g^2/Hz]$')
        self.fd.set_xlim(0,20)


    self.fd.grid()   
    self.chart_type.draw()
    # Calculate Mode Shape
    
    deltaf=ndf*ff
    
    f = np.linspace(0, int(freq_max), int(freq_max*(1/ff)+1)) # spectral lines

    Freq = []
    index = []
    Fi = []
    
    for _x in _f:
        
        lim = (_x - deltaf, _x + deltaf) # frequency bandwidth where the peak is searched
        idxlim = (np.argmin(abs(f-lim[0])), np.argmin(abs(f-lim[1])))
        # ratios between the first and second singular value 
        diffS1S2 = S_val[0,0,idxlim[0]:idxlim[1]]/S_val[1,1,idxlim[0]:idxlim[1]]
        maxDiffS1S2 = np.max(diffS1S2) # looking for the maximum difference
        idx1 = np.argmin(abs(diffS1S2 - maxDiffS1S2))
        idxfin = idxlim[0] + idx1 
    # =============================================================================
        # Modal properties
        fr_FDD = f[idxfin] # Frequency
        fi_FDD = S_vec[0,:,idxfin] # Mode shape
        idx3 = np.argmax(abs(fi_FDD))
        fi_FDDn = fi_FDD/fi_FDD[idx3] # normalised (unity displacement)
        fiFDDn = np.array(fi_FDDn)
        
        Freq.append(fr_FDD)
        Fi.append(fiFDDn)
        index.append(idxfin)
            
    Freq = np.array(Freq)
    Fi = np.array(Fi)
    index = np.array(index)   
    
    Freq = np.unique(Freq,axis=0)
    Fi = Fi.T
    
    
    
    b = []
    
    for _i in range(number_channels):
            freqs["hz"]=(_f[:])
            x = 10*np.log10(S_val[_i, _i])
            peaks, _ = find_peaks(x, prominence=prominence)
            b.append(peaks)
            
    df2 = pd.DataFrame(b)      
    try :
        for a in range(5):
            mod_freqs = []
            
            for i in df2[a]:
                try:
                    
                    mod_freqs.append(freqs["hz"][i])
                    
                except KeyError:
                    pass
            df["mod {0}".format(a+1)] = mod_freqs
    except KeyError:
        pass  
    
    return df