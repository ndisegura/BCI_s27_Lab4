# -*- coding: utf-8 -*-
"""
andres Segura & Tynan Gacy
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
subject=1
#data_file=f'{cwd}{data_directory}SSVEP_S{subject}.npz'


#%% Cell1 Load the Data

data=import_ssvep_data.load_ssvep_data(subject,data_directory)

#%% Cell2 Design a Filter

#Filter out the 15Hz signals
low_cutoff=10
high_cutoff=14
filter_type='hann'
filter_order=1000
fs=data['fs']
filter_coefficients=filter_ssvep_data.make_bandpass_filter(low_cutoff,high_cutoff,filter_type,filter_order,fs)

#Filter out the 12Hz signals
low_cutoff=13
high_cutoff=17
filter_type='hann'
filter_order=1000
fs=data['fs']
filter_coefficients=filter_ssvep_data.make_bandpass_filter(low_cutoff,high_cutoff,filter_type,filter_order,fs)
