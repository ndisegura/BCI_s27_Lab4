# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:41:31 2024

@author: asegura
"""

from pylab import *
from scipy.signal import firwin, lfilter, filtfilt,freqz,hilbert
import matplotlib.pyplot as plt

def make_bandpass_filter(low_cutoff,high_cutoff,filter_type='hann',filter_order=10,fs=1000):
    
    if filter_type==None: filter_type='hann'
    fNQ = fs/2                                     #Compute the Niqyst rate
    taps_number = filter_order                     # Define the filter order
    #Wn = [low_cutoff/fNQ ,high_cutoff/fNQ]         # ... and specify the cutoff frequency normalized to Nyquest rate
    Wn = [low_cutoff ,high_cutoff]         # ... and specify the cutoff frequency normalized to Nyquest rate
    #filter_coefficients  = firwin(taps_number, Wn, window=filter_type, pass_zero='bandpass')              # ... build lowpass FIR filter,
    filter_coefficients  = firwin(taps_number, Wn, window=filter_type, pass_zero=False,fs=fs)              # ... build lowpass FIR filter,
    
    w, h = freqz(filter_coefficients)                      #Compute the frequency response
    
    
    fig, axs = plt.subplots(2)
    axs[0].set_title('Digital filter frequency response')
    axs[0].plot(w*fNQ/3.1416, 20 * np.log10(abs(h)), 'b')
    axs[0].set_ylabel('Amplitude [dB]', color='b')
    axs[0].set_xlabel('Frequency [Hz]')
    ax2 = axs[0].twinx()
    angles = np.unwrap(np.angle(h))
    ax2.plot(w*fNQ/3.1416, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid(True)
    ax2.axis('tight')
    axs[1].set_title('Digital filter impulse response')
    axs[1].plot(filter_coefficients, 'b')
    axs[1].set_ylabel('Amplitude ', color='b')
    axs[1].set_xlabel('Sample Number  [1/fs]')
    axs[1].grid(True)
    
    
    plt.tight_layout()
    plt.show()
    
    return filter_coefficients

def filter_data(data,b):
    
    eeg_data=data['eeg']
    filtered_data=filtfilt(b, a=1, x=eeg_data,axis=1)
    
    
    return filtered_data

def get_envelope(data,filtered_data,channel_to_plot=None,ssvep_frequency=None):
    
    #Get the channels names
    channels=data['channels']
    fs=data['fs']
    
    #Get the envelope
    envelope=np.abs(hilbert(filtered_data,axis=1))
    
    #Plot the selected channels
    if channel_to_plot is not None:
        #Create Boolean array from channel to plot
        is_channel=channels==channel_to_plot #Select channel to plot
        #select the channel to plot using the boolean array
        filtered_data_to_plot=filtered_data[is_channel]
        envelope_data_to_plot=envelope[is_channel]
        #setup the figure to plot
        fig, ax = plt.subplots()
        #plot the data and scale to micro-volts
        ax.plot(np.squeeze(filtered_data_to_plot/10e-6),'r',label='Filtered data')
        ax.plot(np.squeeze(envelope_data_to_plot/10e-6),'b',label='Envelope')
        ax.set_ylabel('Voltage [uV]', color='b')
        ax.set_xlabel('Sample Number', color='b')
        
        if ssvep_frequency is not None:
            ax.set_title(f'{ssvep_frequency} BPF Data')
        else:
            ax.set_title(f'Unknown Frequency Isolated')
        
        plt.tight_layout()
        plt.show()
        
            
      
    return envelope
    
    #np.abs(scipy.signal.hilbert(signal))

