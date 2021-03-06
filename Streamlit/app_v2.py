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
genre = st.sidebar.radio("Sommaire", options, index = 0)

if genre == 'Introduction':
    
    col1,col2,col3 = st.columns(3)
    with col2:
        st.image('.\logo_datascientest.jpg')
    st.header('Introduction')

    left, middle, right = st.columns([5,1,5])
    with left:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("   - 22 Milliards d'euros : Montant estim?? en France des co??ts li??s ?? la maintenance, principalement d'urgence, des machines de production.")
        st.markdown("   - Entre 10 et 15% des accidents du travail entrainant des arr??ts sup??rieurs ou ??gaux ?? 4 jours seraient d?? ?? des d??faillances techniques.")
        st.markdown("   - D??tecter les d??faillances ?? l'aide d'enregistrements sonores pourrait ??tre une m??thode simple et peu co??teuse pour pr??venir ces incidents.")
    with right:
        st.image('.\ligne_de_prod.jpg')
        
    st.markdown("")
    st.markdown("Nous avons essay?? de mettre en place un algorithme permettant de d??tecter ces d??faillances techniques via l'??tude de spectrogrammes provenant d'enregistrement sonores de machines plac??es dans des conditions r??elles.")
    
    st.subheader('Du son au spectrogramme')

    st.markdown("Les donn??es sonores ne sont pas facilement exploitable en l'??tat, une transformation s'impose.")
    st.markdown("En traitement du signal, on pr??f??rera utiliser les spectrogrammes associ??s ?? ces enregistrements")
    st.markdown("Les spectrogramme ont l'avantage de mettre en avant les fr??quences sonores, bien plus exploitable.")
    st.markdown("")
    st.markdown("")
    sns.set()
    
    left, right = st.columns(2)

    with left :
    
        cb_freq_1 = st.checkbox('Fr??quence 1', value = True)
        freq_1 = st.slider(label = 'Fr??quence 1', min_value = 1.0, max_value = 10.0, step = 0.1, value = 3.0)
        ampli_1 = st.slider(label = 'Amplitude 1', min_value = 1.0, max_value = 2.0, step = 0.1, value = 2.0)
        cb_freq_2 = st.checkbox('Fr??quence 2', value = False)
        freq_2 = st.slider(label = 'Fr??quence 2', min_value = 1.0, max_value = 10.0, step = 0.1, value = 6.0)
        ampli_2 = st.slider(label = 'Amplitude 2', min_value = 1.0, max_value = 2.0, step = 0.1, value = 1.5)
        cb_freq_3 = st.checkbox('Fr??quence 3', value = False)
        freq_3 = st.slider(label = 'Fr??quence 3', min_value = 1.0, max_value = 10.0, step = 0.1, value = 7.0)
        ampli_3 = st.slider(label = 'Amplitude 3', min_value = 1.0, max_value = 2.0, step = 0.1, value = 1.0)

        checked = [cb_freq_1, cb_freq_2, cb_freq_3]
        freq_list = [freq_1, freq_2, freq_3]
        ampli_list = [ampli_1, ampli_2, ampli_3]
        signal_global = 1
        
        x_signal = np.linspace(0, 2*np.pi, 200)

    with right :

        fig_signal, (ax1, ax2) = plt.subplots(2, figsize = (12, 12))
        
        for i in range(3):
            if checked[i]:
                sinus = ampli_list[i] * np.sin(x_signal*freq_list[i])
                signal_global *= ampli_list[i] * sinus
                ax1.plot(x_signal, sinus, ':')
                ax2.plot([freq_list[i], freq_list[i]], [0, ampli_list[i]])
        ax2.set_xlim([0, 11])
        ax1.plot(x_signal, signal_global, 'black')

        st.pyplot(fig_signal)

    
    st.markdown("Afin de garder la variation du signal dans le temps, on utilise l'algorithme de Short Time Fourier Transform :")
    st.image('.\stft.png')
 

if genre == 'DataViz':
    st.subheader('DataViz')
    col1,col2,col3 = st.columns([1,6,1])
    with col2:
        st.image('.\R??partition des extraits.jpg',width=700)
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
        
    st.subheader("Principe")
    st.text('\n')
    st.markdown("Id??e de base: reconnaitre les patterns sp??cifiques ?? une machine en bon ??tat de martche pour signaler lorsqu'ils ne sont plus d??tect??s")
    
    col1, col2, col3 = st.columns([1,7,1])
    with col2:
        st.image('.\\Autoencodeur.png', caption="Architecture d'un autoencodeur")
    
    st.text('\n')
    st.markdown("L'autoencodeur extrait les features de l'image en entr??e en r??duisant progressivement la dimension des couches")
    st.markdown("Le d??codeur remonte jusqu'?? la dimension initiale")
    st.markdown("Le but est de reconstruire le meiux possible les images d'entrainement, pour d??tecter les erreurs de reconstruction des cas anormaux lors du test ")
    
    st.subheader("D??marche")
    st.markdown("Dans un premier temps les images sont d??coup??es en format  plus petits pour ??tre trait??es plus facilement par le r??seau de neurone")
    st.image('.\D??composition des images.jpg',width=700,caption='D??composition des extraits')    
    
    st.markdown('Puis le mod??le est entrain?? sur les extraits normaux afin de reconstruire les images')
    st.image('.\Reconstruction des images.jpg',caption='Reconstruction des images')
    st.markdown("Le fait de grouper les images en batchs lisse l'image de sortie")
    st.markdown("On sent qu'on perd la d??pendance temporelle, qu'il serait possible de retrouver en introduisant des neurones r??currents dans le r??seau") 
    
    st.subheader("R??partition de l'erreur")
    col4, col5, col6 = st.columns([1,6,1])
    with col5:
        st.image('.\Distribution des pertes.jpg')
    
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
    st.header('Conclusion')
    st.subheader('Synth??ses des mod??les')

    st.markdown("**Synth??se AE : **")
    _, col5, _ = st.columns([1,6,1])
    with col5:
        st.image('./result_ae.PNG',width=600)
    st.markdown("")

    st.markdown("**Synth??se Classifieur : **")
    _, col5, _ = st.columns([1,15,1])
    with col5:
        st.image('./result_classif.PNG',width=700)
    st.markdown("")

    st.subheader('Probl??mes rencontr??s')

    st.markdown("   - La taille du jeu de donn??es")
    
    st.markdown("   - Inexp??rience ")

    st.markdown("   -   Technicit?? de la probl??matique")
    
    st.subheader('Pistes d\'am??lioration')
    st.markdown("**Pour l'Auto-Encodeur** : ")
    st.markdown("   - La prise en compte de la temporalit??")
    st.markdown("   - L'utilisation de masques sur les donn??es d'entr??es")
    st.markdown("   - Faire une augmentation des donn??es")


    st.markdown("**Pour les classifieurs** : ")
    st.markdown("   - L'optimisation des couches")
    st.markdown("   - Faire une augmentation des donn??es de la classe minoritaire")
    st.markdown("   - Utiliser d'autres classifieurs plus performants.")

    st.markdown("**Approche mixte** :")
    st.markdown("   - Classer des images issues de l'encodeur")
    
    st.subheader("Mise en production")
    st.markdown("   - Sous condition d'am??lioration des performances des mod??les, d??ploiement possible.")
    st.image('./deploiement.PNG')

    


    
