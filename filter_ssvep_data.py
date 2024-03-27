# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:41:31 2024

@author: Andres Segura & Tynan Gacy
"""

from pylab import *
from scipy.signal import firwin, lfilter, filtfilt,freqz,hilbert
import matplotlib.pyplot as plt
import numpy as np
import import_ssvep_data

#%% Part 2

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

#%% Part 3

def filter_data(data,b):
    
    eeg_data=data['eeg']
    filtered_data=filtfilt(b, a=1, x=eeg_data,axis=1)
    
    
    return filtered_data

#%% Part 4

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
#%% Part 5


def plot_ssvep_amplitudes(data,envelope_a,envelope_b,channel_to_plot,ssvep_freq_a,ssvep_freq_b,subject):

    # Pull data from directory
    channels=data['channels']
    fs=data['fs']
    event_samples=data['event_samples']
    event_durations=data['event_durations']
    event_type=data['event_types']

    # Limit to channel to plot
    is_channel=channels==channel_to_plot #Boolean array for channel to plot
    envelope_data_to_plot_a=envelope_a[is_channel] # Limit envelope_a to channel
    envelope_data_to_plot_b=envelope_b[is_channel] # Limit envelope_b to channel
    
    # Generate x axis in time(s)
    time_in_s=np.arange(0,len(envelope_data_to_plot_a[0])*1/fs,1/fs) # 
    
    # Create figure and subplots
    fig, axs = plt.subplots(2,1,sharex=True)
    # Plot event start and end times and types
    for sample, duration, event_type in zip(event_samples, event_durations, event_type):
        start_time = sample / fs
        end_time = (sample + duration) / fs

        axs[0].set_title(f'Subject {subject} SSVEP Amplitudes')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Flash Frequency')
        axs[0].grid()
        axs[0].plot(start_time, event_type, 'bo')  # Dot at the start time
        axs[0].plot(end_time, event_type, 'bo')    # Dot at the end time
        axs[0].plot([start_time, end_time], [event_type, event_type], color='b', linewidth=2) # Line between start/end

            
    axs[1].set_title('Envelope Comparison')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Voltage (uV')
    axs[1].grid()
    axs[1].plot(time_in_s,np.squeeze(envelope_data_to_plot_a/10e-6),label='12Hz Envelope')
    axs[1].plot(time_in_s,np.squeeze(envelope_data_to_plot_b/10e-6),label='15Hz Envelope')

        
    plt.tight_layout()
    plt.legend()
    plt.show()

    
    
    return None
#%% Part 6

def plot_filtered_spectra(data,filtered_data,envelope,channels=['Fz','Oz']):
    
    
    epoch_start_time=0
    epoch_end_time=20
    
    event_samples=data['event_samples']
    event_duration=data['event_durations']
    event_type=data['event_types']
    fs=data['fs']
    
    #Epoch raw data
    raw_data_epochs,data_time,is_trial_15Hz=import_ssvep_data.epoch_ssvep_data(data,epoch_start_time,epoch_end_time)
    raw_data_epochs=raw_data_epochs[is_trial_15Hz] #Select first frequency
    #Epoch filtered data
    filtered_data_epochs,data_time,is_trial_15Hz=import_ssvep_data.epoch_generic_data(filtered_data,epoch_start_time,epoch_end_time, event_samples,event_duration,event_type,fs)
    filtered_data_epochs=filtered_data_epochs[is_trial_15Hz] #Select first frequency
    #epoch envelope data
    envelope_epochs,data_time,is_trial_15Hz=import_ssvep_data.epoch_generic_data(envelope,epoch_start_time,epoch_end_time, event_samples,event_duration,event_type,fs)
    envelope_epochs=envelope_epochs[is_trial_15Hz] #Select first frequency
    
    #Compute power spectrum of data_epochs
    data_epochs_fft,fft_frequencies =import_ssvep_data.get_frequency_spectrum(raw_data_epochs,fs)
    #Compute power spectrum of filered_epochs
    filtered_epochs_fft,fft_frequencies =import_ssvep_data.get_frequency_spectrum(filtered_data_epochs,fs)
    #Compute power spectrum of envelope_epochs
    envelope_epochs_fft,fft_frequencies =import_ssvep_data.get_frequency_spectrum(envelope_epochs,fs)
    
    #Compute the FFT magnitude
    data_epochs_fft_magnitude=np.absolute(data_epochs_fft)
    filtered_epochs_fft_magnitude=np.absolute(filtered_epochs_fft)
    envelope_epochs_fft_magnitude=np.absolute(envelope_epochs_fft)
    
    #Compute the power
    #Generate power array
    power_array=np.zeros(data_epochs_fft_magnitude.shape)
    power_array=2 #Array of dimension m,n,l with value=2
    #Compute the power by squaring each element
    data_epochs_fft_power=np.power(data_epochs_fft_magnitude,power_array)
    filtered_epochs_fft_power=np.power(filtered_epochs_fft_magnitude,power_array)
    envelope_epochs_fft_power=np.power(envelope_epochs_fft_magnitude,power_array)
    
    #Compute the mean
    data_epochs_fft_mean=np.mean(data_epochs_fft_power, axis=0)
    filtered_epochs_fft_mean=np.mean(filtered_epochs_fft_power, axis=0)
    envelope_epochs_fft_mean=np.mean(envelope_epochs_fft_power, axis=0)
    
    #Normalize to the highest power. Use array broadcasting to handle dimensions mismatch
    data_epochs_fft_normalized=data_epochs_fft_mean/np.max(data_epochs_fft_mean,axis=1)[:,np.newaxis]
    filtered_epochs_fft_normalized=filtered_epochs_fft_mean/np.max(filtered_epochs_fft_mean,axis=1)[:,np.newaxis]    
    envelope_epochs_fft_normalized=envelope_epochs_fft_mean/np.max(envelope_epochs_fft_mean,axis=1)[:,np.newaxis]
    
    
    #Compute the FFT power in dB
    data_epochs_fft_db= np.log10(data_epochs_fft_normalized)
    filtered_epochs_fft_db= np.log10(filtered_epochs_fft_normalized)
    envelope_epochs_fft_db= np.log10(envelope_epochs_fft_normalized)
    
    
    
    return None
