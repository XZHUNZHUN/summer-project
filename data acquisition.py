# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 13:39:52 2019

@author: XUZHUN
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from pydub import AudioSegment
#get the audio id
f = open('./occurrence.txt','rb')
audio_ids = []
audio_types = []
audio_family = []
lines = f.readlines()
i = 0
for line in lines:
    i += 1
    line = line.decode()                #byte to str
    rows = line.strip('\n').split('\t') #spilit in tab
    rows = [x for x in rows if x != ''] #remove the ''

    if i > 1 and rows[4]=='Peter Boesman':
        try:
            family_idx = rows.index('SPECIES') - 3
        except:
            family_idx = 31
      
        audio_ids.append(rows[1].split('@')[0]) #get the audio id, spliting with @
        audio_types.append(rows[10])
        audio_family.append(rows[family_idx])
  
        
f.close()

dist_call = pd.value_counts(audio_types) #distribution of call
dist_fa = pd.value_counts(audio_family) #distribution of family

'''
draw the fig showing the distribution of type of bird song and family type

'''
family_data = dist_fa[dist_fa.values>500] #12493 piece
'''
Tyrannidae        2098
Furnariidae       1615
Thamnophilidae    1463
Muscicapidae      1065
Thraupidae         929
Emberizidae        790
Troglodytidae      777
Picidae            728
Psittacidae        676
Columbidae         653
Parulidae          583
Cisticolidae       571
Fringillidae       545
'''
plt.figure(figsize=(20,8),dpi=80)
_x = family_data.index
_y = family_data.values
plt.bar(_x,_y,color="green")
plt.xticks(fontsize=10)
plt.yticks(fontsize=17)
plt.xlabel('famlily type',fontsize=20)
plt.ylabel('number',fontsize=20)
#plt.title('distribution of family type')
plt.show()
plt.close()
#filer the family
df = pd.DataFrame(np.transpose([audio_ids,audio_types,audio_family]),columns=['id','song','family']) #combine the items

famliy_not_index = []
i = 0
for family in audio_family:
    if not _x.contains(family):
        famliy_not_index.append(i)
    i+=1
df = df.drop(index=famliy_not_index)
#filter the call type
type_song = ['song','Song','song?','short song','long song','excited song','subsong','rising song',
             'song 1', 'song 2']
type_call = ['call','Call','long call','interaction calls', 'soft calls', 'chasing call', 
             'excited calls','interaction call', 'call?', 'alarm call', 'call perched','calls']
type_songCall = ['call, song','song and call','call and song', 'song, call']
type_flight = ['flight call', 'call flight', 'display flight', 'display calls']
type_dawn = ['dawn song','dawn chorus','Day-time song']
type_rattle = ['rattle call', 'rattle', 'drum', 'rattle song', 'drumming', 'booming']

#classify by song
def type_transfer(x):
    if x in type_song:
        return 0
    elif x in type_call:
        return 1
    elif x in type_songCall:
        return 2
    elif x in type_flight:
        return 3
    elif x in type_dawn:
        return 4
    elif x in type_rattle:
        return 5
    else:
        return 6

#create dictionary
dic_df = {}
for x in dist_call.index:
    dic_df[x]=type_transfer(x)
for x in family_data.index:
    dic_df[x]=list(family_data.index).index(x)
df = df.replace(dic_df)

#plot song distribution
song_type = pd.value_counts(df.song.values)
plt.figure(figsize=(20,8),dpi=80)
_x = ['song','call','other','song,call','flight call','rattle','dawn call']
_y = song_type.values
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.bar(_x,_y,color="red")
plt.xlabel('sound type',fontsize=20)
plt.ylabel('number',fontsize=20)
#plt.title('distribution of sound type',fontsize=32)
plt.show()
#df.to_csv("./data.npz",index=None)
a = [100,45,69,351,533,] 
b=['clap', 'cowbell', 'crash', 'hat', 'kick', 'ride', 'snare', 'tom']


'''