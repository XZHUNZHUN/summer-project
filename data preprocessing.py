# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:44:33 2019

@author: XUZHUN
"""
import os 
import pandas as pd
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tensorflow as tf
'''
get the path of all wave files
'''
wav_files = []
save_path_wav = './audio/mp3/'
save_path_spectrogram = './audio/spectrum/'


for roots, dirs, filenames in os.walk(save_path_wav):
    for filename in filenames:
        filename_path = save_path_wav + filename
        wav_files.append(filename_path)

i = 0
sample_rate = 16384
label = pd.read_csv('./data.csv')
train_wav = []
train_song_label = []
train_family_label = []
for i in range(0,12493):
    print('processing data... No.' + str(i))
    _wav, _fs = librosa.core.load(wav_files[i],sr=sample_rate)
    _wav/= np.max(np.abs(_wav))
        
    plt.figure(figsize=(25,8))
    librosa.display.waveplot(_wav[16384:32000],_fs)
    plt.show()
    plt.close()
    
    wav_bits = _wav.shape[0]

#    plt.figure()
#    librosa.display.waveplot(_wav,_fs)
#    plt.show()
#    plt.close()
    
    #sample the audio
    sample_size = int((wav_bits / _fs) // 2) #every 2 seconds sample
    if sample_size == 1:
        continue
    max_filter = 0.05                            #the maximum mean of sample
    for x in range(sample_size):
        start_pointer = np.random.randint(x*sample_rate, (x + 0.5)*sample_rate - 1)
        sample_wav = _wav[start_pointer:start_pointer+sample_rate] #sample
        
        if not sample_wav.shape[0] == sample_rate:
            break
        if np.mean(np.abs(sample_wav)) < max_filter:
            continue
        train_wav.append(sample_wav)
        train_song_label.append(label.get_value(i,'song'))
        train_family_label.append(label.get_value(i,'family'))
    i+=1    

train_family_label = np.array(train_family_label)
train_song_label = np.array(train_song_label)
train_wav = np.array(train_wav)
np.savez('./train_data.npz',train_wav,train_song_label,train_family_label)

   

