# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:18:14 2021

@author: Quasarlight
"""

import streamlit as st
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import librosa as lb
import seaborn as sns
import random
from os import listdir
from os.path import isfile, join

##### A renseigner #####
directory='C:/Users/romua/Documents/Formation_data_scientist/ASD/dataset/'

#DEFINITION DES FONCTIONS

##Fonction d'affichage du signal audio
def plot_audio(audio_data, fe):
    t = np.arange(len(audio_data))/fe 
    plt.plot(t, audio_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

#Fonctions d'affichage du Spectrogramme "classique"
def spectrogram(audio, fe, dt):
    return np.abs(lb.stft(audio,n_fft = int(dt*fe),hop_length = int(dt*fe/2)))

def plot_spectrogram(audio, fe, dt, hop_length):
    im = np.abs(lb.stft(audio,n_fft = int(dt*fe),hop_length=hop_length))
    sns.heatmap(np.rot90(im.T), cmap='inferno', vmin=0, vmax=np.max(im)/3)
    loc, labels = plt.xticks()
    l = np.round((loc-loc.min())*len(audio)/fe/loc.max(), 2)
    plt.xticks(loc, l)
    loc, labels = plt.yticks()
    l = np.array(loc[::-1]*fe/2/loc.max(), dtype=int)
    plt.yticks(loc, l)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

#Fontions d'affichage en echelle MEL et dB pour l'amplitude
def logMelSpectrogram(audio, params, fe):
    stfts = lb.stft(audio,n_fft = int(params['n_fft']),hop_length = int(params["frame_step"]),center = False).T
    power_spectrograms = np.real(stfts * np.conj(stfts))
    linear_to_mel_weight_matrix = lb.filters.mel(sr=fe,n_fft=int(params['n_fft']) + 1,n_mels=params['num_mel_bins'],
                                fmin=params['lower_edge_hertz'],fmax=params['upper_edge_hertz']).T
    mel_spectrograms = np.tensordot(power_spectrograms,linear_to_mel_weight_matrix, 1)
    return (np.log(mel_spectrograms + 1e-8).astype(np.float16))


def plot_logMelSpectrogram(audio, params, fe):
    sns.heatmap(np.rot90(logMelSpectrogram(audio, params, fe)), cmap='inferno', vmin = -6)
    loc, labels = plt.xticks()
    l = np.round((loc-loc.min())*len(audio)/fe/loc.max(), 2)
    plt.xticks(loc, l)
    plt.yticks([])
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Mel)")
    
class File_charge:
    def __init__(self, path):
        self.path = path 
        
    def load_file(self):
        dirs = os.listdir(self.path)
        df = list()
        for dir in dirs:
            df.append((self.path+"/"+dir))
        df = pd.DataFrame(df, columns = ['audio_file'])
        df = df.reset_index()
        return  df
    
def load_audio(audio_path):
    return lb.load(audio_path, sr=None)

@st.experimental_memo
def fetch_new_imgs(new):
    if new:
        i=str(random.choice(range(10,99,1)))
        j=str(random.choice(range(10,99,1)))
    else:
        i='10'
        j='10' 
    return i,j           

#FIN DES FONCTIONS

#STREAMLIT
st.set_page_config(layout="wide")

st.title('D??tection Son_atyPyque')


options = ['Introduction', 'DataViz', 'AutoEncodeur', 'Mod??le de classification', 'Conclusion']
genre = st.sidebar.radio("Sommaire", options, index = 1)

if genre == 'Introduction':
    st.subheader('Introduction')    

if genre == 'DataViz':
    st.subheader('DataViz')
    st.image('.\R??partition des extraits.jpg')
    option = st.selectbox('S??lection de mod??le',['Slider','Toycar','ToyConveyor','Valve','Fan',"Pump"])   
    new=st.button('Nouveaux extraits') 
    
    i,j=fetch_new_imgs(new)
    samples,fe = lb.load(directory+option+'/train/normal_id_02_000000'+i+'.wav', sr=None)
    samples_a,fe_a = lb.load(directory+option+'/test/anomaly_id_02_000000'+j+'.wav', sr=None)
    col1, col2 = st.columns(2)
        
    #FIGURES
    with col1:
        st.subheader('Signal audio normal\n')
        #Trac?? signal audio
        fig1=plt.figure(figsize=(12,7))
        plot_audio(samples, fe)
        st.pyplot(fig1)
     
        #Possibilit?? d'??couter le son pour mieux comprendre le trac??
        st.subheader('Extrait')
        st.audio(directory+option+'/train/normal_id_02_000000'+i+'.wav')
        
    with col2:
            
        st.subheader('Signal audio anormal\n')
        #Trac?? signal audio
        fig3=plt.figure(figsize=(12,7))
        plot_audio(samples_a, fe)
        st.pyplot(fig3)
     
        #Possibilit?? d'??couter le son pour mieux comprendre le trac??
        st.subheader('Extrait')
        st.audio(directory+option+'/test/anomaly_id_02_000000'+i+'.wav')   
             
    with st.expander('Param??tres spectrogramme'):
         st.markdown('Compromis ?? trouver entre pr??cision et volume de donn??es')
         nfft=st.slider('nfft',256,1024,1024,256)
         frame_step=st.slider('frame step',0,1024,512,256)
         mel_bins=st.slider('d??coupe fr??quentielle',64,256,128,64)
         params = {'n_fft': nfft,'frame_step': frame_step,'lower_edge_hertz': 0,'upper_edge_hertz': 8000,'num_mel_bins': mel_bins}
         dt=0.01
         hop_length = int(dt*fe/2)            
            
    col3, col4 = st.columns(2)
        
    with col3:
        st.subheader('Spectrogramme normal')
                
        #Trac?? spectrogramme "classique"
        fig2=plt.figure(figsize=(15,7))
        plot_logMelSpectrogram(samples, params, fe)
        plt.title('Spectrogramme Log Mel - Son normal')
        st.pyplot(fig2)
            
    with col4:
        st.subheader('Spectrogramme anormal')
            
        fig4=plt.figure(figsize=(15,7))
        plot_logMelSpectrogram(samples_a, params, fe_a)
        plt.title('Spectrogramme Log Mel - Son anormal')
        st.pyplot(fig4)
    
    
    
elif genre == 'AutoEncodeur':
    st.header('AutoEncodeur')
    st.subheader("D??marche")
    st.markdown("Dans un premier temps les images sont d??coup??es en format  plus petits pour ??tre trait??es plus facilement par le r??seau de neurone")
    st.image('.\D??composition des images.jpg')
        
    st.subheader("Principe de l'architecture")
    st.text('\n')
    col1, col2, col3 = st.columns([2,6,1])
    with col1:
        st.write("")
    with col2:
        st.image('.\\Autoencodeur.png')
    with col3:
        st.write("")
    
    st.text('\n')
    st.markdown("L'autoencodeur extrait les features de l'image en entr??e en r??duisant progressivement la dimension des couches")
    st.markdown("Le d??codeur remonte jusqu'?? la dimension initiale")
    st.markdown("Le but est de reconstruire le meiux possible les images d'entrainement, pour d??tecter les erreurs de reconstruction des cas anormaux lors du test ")
        
    st.subheader('Reconstruction')
    st.image('.\Reconstruction des images.jpg')
    st.markdown("Le fait de grouper les images en batchs lisse l'image de sortie")
    st.markdown("On sent qu'on perd la d??pendance temporelle, qu'il serait possible de retrouver en introduisant des neurones r??currents dans le r??seau") 
    
    st.subheader("R??partition de l'erreur")
    col4, col5, col6 = st.columns([1,6,1])
    with col4:
        st.write("")
    with col5:
        st.image('.\Distribution des pertes.jpg')
    with col6:
        st.write("")
    
    
    st.markdown("Il n'y a pas de distinction nette entre les cas normaux et anormaux, le taux de d??tection est donc assez varible et le taux de faux n??gatifs d??pend fortement du seuil")
            
    st.subheader('R??sultats')
    st.image('.\M??triques en fonction du seuil.jpg')
    st.markdown("On obtient malgr?? tout un seuil optimum qui maximise l'accuracy et la pr??cision")
    
    
    
elif genre =='Mod??le de classification':
    st.subheader('Mod??le Classification Pompe')
    # st.image('./Classification.png')

    
    st.subheader("Descriptif du dataset")
    st.markdown("L'objectif est de pr??dire si le spectrogramme en entr??e de notre mod??le correspond ?? une pompe normale ou anormale.")
    st.markdown("Ne disposant que des donn??es sonores normales dans notre dataset d'entra??nement, la parade choisie est de consid??rer que les donn??es d'entra??nement de la pompe sont de classe 0 (classe normale)")
    st.markdown("En parall??le nous consid??rons que les donn??es sonores d'entra??nement des autres machines (fan, slider, valve) sont de classe 1 (classe anormal)")
    col1, col2, col3     = st.columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        st.image('./image_classification.PNG')
    with col3:
        st.write("")

    st.subheader('R??partition des donn??es entre machines normales et machines anormales')
    col3_0, col3_1, col3_2  = st.columns([1,10,1])
    with col3_0:
        st.write("")
    
    with col3_1:
        
        st.image('./repartition_machines_normale_anormale.PNG')
    with col3_2:
        st.write("")

    

    st.markdown("Ayant transformer nos donn??es sonores en images, nous utiliserons un r??seau de neurones convolutif (CNN) comme classifieur")
    st.subheader("Architecture du r??seau CNN LeNet")
    col4, col5, col6 = st.columns([2,5,1])
    with col4:
        st.write("")
    with col5:
        st.image('./image_rzo_neurones.png')
    with col6:
        st.write("")
    
    
    st.markdown("""<style>.big-font {font-size:25px ;}</style>""", unsafe_allow_html=True)

    
     
    result_list = ["accuracy", "confusion matrix", "classification_report", "ROC curve"]
    st.subheader('R??sultat')
    selected_result = st.selectbox("", result_list)
    
    col7, col8, col9 = st.columns([2,8,1])
    with col7:
        st.write("")
    with col8:
        if selected_result == "confusion matrix":
            st.image('./matrice_confusion.PNG')
        elif selected_result == "accuracy":
           
            st.markdown('<p class="big-font">pr??cision du mod??le : 0.71</p>', unsafe_allow_html=True)
          
           
        elif selected_result == "ROC curve":
            st.image('./Courbe_ROC.PNG')

        elif selected_result =="classification_report":
            st.image('./rapport_classification.PNG')
    with col9:
        st.write("")

elif genre =='Conclusion':
    st.subheader('Conclusion')

    