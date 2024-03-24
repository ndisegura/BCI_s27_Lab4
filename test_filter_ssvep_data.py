# -*- coding: utf-8 -*-
"""
Andres Segura & Tynan Gacy
BME 6770: BCI's Lab 04
Dr. David Jangraw
3/11/2024

This script intends to ...


"""

# Inport the necessry modules
import os
import sys
import matplotlib.pyplot as plt
import import_ssvep_data
import filter_ssvep_data

#Make sure relative path work
cwd=os.getcwd()
sys.path.insert(0,f"{cwd}\course_software\SsvepData\\")

#Close previosly drawn plots
plt.close('all')

#Build data file string
data_directory=f'{cwd}/course_software/SsvepData/'
#data_directory = './SsvepData/'
subject=1
#data_file=f'{cwd}{data_directory}SSVEP_S{subject}.npz'


#%% Cell1 Load the Data

data=import_ssvep_data.load_ssvep_data(subject,data_directory)

#%% Cell2 Design a Filter

#Filter out the 15Hz signals
low_cutoff=10
high_cutoff=14
filter_type='hann'
filter_order=2000
fs=data['fs']
filter_coefficients_band_pass_12Hz=filter_ssvep_data.make_bandpass_filter(low_cutoff,high_cutoff,filter_type,filter_order,fs)

#Filter out the 12Hz signals
low_cutoff=13
high_cutoff=17
filter_type='hann'
filter_order=2000
fs=data['fs']
filter_coefficients_band_pass_15Hz=filter_ssvep_data.make_bandpass_filter(low_cutoff,high_cutoff,filter_type,filter_order,fs)

"""
A) How much will 12Hz oscillations be attenuated by the 15Hz filter? How much will 15Hz 
oscillations be attenuated by the 12Hz filter?

According to the frequency response plot. Each frequency will be attenuated by approximately  -27dBc

B) Experiment with higher and lower order filters. Describe how changing the order changes 
the frequency and impulse response of the filter

Increasing the order of the filter improves the attenuation of the adjacent signals (e.g. 15Hz for the 12Hz Bandpass filter),
but also incrases the lenght of the impulse response. Similarly, reducing the order of the filter decrases the attenuation of 
adjacent frequencies, but it also reduces the length of the impulse response.

"""
#%% Cell 3 Filter the EEG signals

#Filter 12Hz signals
filtered_data_12Hz=filter_ssvep_data.filter_data(data,filter_coefficients_band_pass_12Hz)

#Filtered 15Hz signals
filtered_data_15Hz=filter_ssvep_data.filter_data(data,filter_coefficients_band_pass_15Hz)


#%% Cell 4 Calculate the Envelope

# Get envelope for 12Hz
envelope_12Hz=filter_ssvep_data.get_envelope(data, filtered_data_12Hz[:,:],'Oz',12)
#envelope_12Hz=filter_ssvep_data.get_envelope(data, filtered_data_12Hz[:,145000:164000],'Oz',12)

# Get envelope for 15Hz
envelope_15Hz=filter_ssvep_data.get_envelope(data, filtered_data_15Hz[:,:],'Oz',15)
#envelope_15Hz=filter_ssvep_data.get_envelope(data, filtered_data_15Hz[:,145000:164000],'Oz',15)

#%% Cell 5 Plot amplitudes

# Plot amplitudes for Oz

filter_ssvep_data.plot_ssvep_amplitudes(data,envelope_12Hz,envelope_15Hz,'Oz',12,15,subject)

#%% Cell 6 Examine Spectra

#filter_ssvep_data.plot_filtered_spectra(data,filtered_data,envelope)


