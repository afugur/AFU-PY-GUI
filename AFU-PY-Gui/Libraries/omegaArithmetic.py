# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 00:55:29 2021

    Numerically integrate a time series in the frequency domain.
    
    This function integrates a time series in the frequency domain using
    'Omega Arithmetic', over a defined frequency band.
    
    Parameters
    ----------
    a : array_like
        Input time series.
    fs : int
        Sampling rate (Hz) of the input time series.
    f_lo : float, optional
        Lower frequency bound over which integration takes place.
        Defaults to 0 Hz.
    f_hi : float, optional
        Upper frequency bound over which integration takes place.
        Defaults to the Nyquist frequency ( = fs / 2).
    times : int, optional
        Number of times to integrate input time series a. Can be either 
        0, 1 or 2. If 0 is used, function effectively applies a 'brick wall' 
        frequency domain filter to a.
        Defaults to 1.
    winlen : int, optional
        Number of seconds at the beginning and end of a file to apply half a 
        Hanning window to. Limited to half the record length.
        Defaults to 1 second.
    unwin : Boolean, optional
        Whether or not to remove the window applied to the input time series
        from the output time series.
    
    Returns
    -------
    out : complex ndarray
        The zero-, single- or double-integrated acceleration time series.
   

@author: afugur
"""

import numpy as np

def intf(a, fs, f_lo=0.0 , f_hi=1.0e12 , times=1 , winlen=1 , unwin=False):
    
    a = a - a.mean()                        # Convert time series to zero-mean
    if np.mod(a.size,2) != 0:               # Check for even length time series
        odd = True
        a = np.append(a, 0)                 # If not, append zero to array
    else:
        odd = False
    f_hi = min(fs/2, f_hi)                  # Upper frequency limited to Nyquist
    winlen = min(a.size/2, winlen)          # Limit window to half record length
    
    ni = a.size                             # No. of points in data (int) 
    nf = float(ni)                          # No. of points in data (float)
    fs = float(fs)                          # Sampling rate (Hz)
    df = fs/nf                              # Frequency increment in FFT
    stf_i = int(f_lo/df)                    # Index of lower frequency bound
    enf_i = int(f_hi/df)                    # Index of upper frequency bound
    
    window = np.ones(ni)                    # Create window function
    es = int(winlen*fs)                     # No. of samples to window from ends
    edge_win = np.hanning(es)               # Hanning window edge 
    window[: int( es/2) ] = edge_win[: int(es/2) ]
    window[ int(-es/2) : ] = edge_win[int(-es/2) :]
    a_w = a*window
    
    FFTspec_a = np.fft.rfft(a_w)            # Calculate complex FFT of input
    FFTfreq = np.fft.fftfreq(ni, d=1/fs)[: int(ni/2) +1]
    
    w = (2*np.pi*FFTfreq)                   # Omega
    iw = (0+1j)*w                           # i*Omega
    
    mask = np.zeros(int( ni/2) + 1)                 # Half-length mask for +ve freqs
    mask[stf_i:enf_i] = 1.0                 # Mask = 1 for desired +ve freqs
    
    EPS = 0.1 # Dummy value
    
    if times == 2:                          # Double integration
        FFTspec = -FFTspec_a*w / ((w+EPS)**3 )
        # FFTspec = -FFTspec_a*w / ((w)**3 )
    elif times == 1:                        # Single integration
        FFTspec = FFTspec_a*iw / ((iw+EPS)**2)
        # FFTspec = FFTspec_a*iw / ((iw)**2)
    elif times == 0:                        # No integration
        FFTspec = FFTspec_a
    else:
        print('Error')
    
    FFTspec *= mask                         # Select frequencies to use
    
    out_w = np.fft.irfft(FFTspec)           # Return to time domain
    
    if unwin == True:
        out = out_w*window/(window+EPS)**2  # Remove window from time series
    else:
        out = out_w
    
    if odd == True:                         # Check for even length time series
        return out[:-1]                     # If not, remove last entry
    else:        
        return out