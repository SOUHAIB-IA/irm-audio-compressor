from tkinter import *
import tkinter as tk
import pygame
import os
import wave
import playsound
import os
from tkinter import filedialog
from pydub.playback import play
from PIL import Image, ImageTk
import subprocess
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pydub import AudioSegment
import glob
import struct
from scipy.io.wavfile import write
from tkinter import scrolledtext

def Codage_LZW(s):
    asciiDict = {chr(i): i for i in range(256)}
    encodeur = []
    indx = 256 #list(asciiDict.values())[-1]+1
    c= s[0]
    for i in range(len(s)):
        if i < len(s)-1:
            n = s[i+1]
            if c+n in asciiDict:
                c = c+n
            else:
                asciiDict[c+n] = indx
                encodeur.append(asciiDict[c])
                c = n
                indx += 1
    if c+n:
        encodeur.append(asciiDict[c])
    return asciiDict,encodeur
def Decodage_LZW(code_list):
    asciiDict = {i: chr(i) for i in range(256)}
    next_code = 256
    decoded_list = []
    prev_code = code_list[0]
    decoded_list.append(asciiDict[prev_code])
    
    # Loop through the rest of the codes
    for curr_code in code_list[1:]:
        # Check if the current code is in the dictionary
        if curr_code in asciiDict:
            curr_str = asciiDict[curr_code]
        # If the current code is not in the dictionary, create a new entry
        else:
            curr_str = asciiDict[prev_code] + asciiDict[prev_code][0]
        for c in curr_str:
            decoded_list.append(c)
        
        # Add a new entry to the dictionary
        asciiDict[next_code] = asciiDict[prev_code] + curr_str[0]
        next_code += 1
        
        # Update the previous code
        prev_code = curr_code
    return decoded_list

def uniq_img(image_freq):
    new_l=[chr(int(s)) for s in image_freq]
    return new_l
def freq_from_uniq(uniq_list):
    freq_list = [ord(c) for c in uniq_list]
    return freq_list


def MSE(audio):
    n = len(audio)
    moy = np.mean(audio)
    return np.sum((audio-moy)**2)/n

def PSNR(audio):
    max_val = np.max(audio)
    mse_val = MSE(audio)
    if mse_val == 0:
        return float('inf')
    else:
        return 10*np.log10(max_val**2/mse_val)

def lire_irm(nomf):
    with open(nomf, "rb") as fb:
        indicateur=struct.unpack("3s", fb.read(3))[0]
        freq=struct.unpack("i", fb.read(4))[0]

        nbr_canaux=struct.unpack("i", fb.read(4))[0]

        nbr_echa=struct.unpack("i", fb.read(4))[0]

        profendeur=struct.unpack("i", fb.read(4))[0]
        n_max=struct.unpack("f", fb.read(4))[0]

        o_min=struct.unpack("f", fb.read(4))[0]
        data=np.frombuffer(fb.read(),np.int32)
        data_b=Decodage_LZW(list(data))
        data_bb=freq_from_uniq(data_b)
        data_audio=np.array(data_bb)
        data_hand_orgi=((data_audio/ ((2**8)-1))*n_max) +o_min
        rounded_data=np.round(data_hand_orgi)
        rounded_data = rounded_data.astype(np.int16)
        fb.close()
        mse=MSE(rounded_data )
        psnr=PSNR(rounded_data )
        if nbr_canaux==2:
            sd.play(rounded_data,freq*2)
        else:
            sd.play(rounded_data,freq)
def lire_irm2(nomf):
    with open(nomf, "rb") as fb:
        indicateur=struct.unpack("3s", fb.read(3))[0]
        freq=struct.unpack("i", fb.read(4))[0]

        nbr_canaux=struct.unpack("i", fb.read(4))[0]

        nbr_echa=struct.unpack("i", fb.read(4))[0]

        profendeur=struct.unpack("i", fb.read(4))[0]
        n_max=struct.unpack("f", fb.read(4))[0]

        o_min=struct.unpack("f", fb.read(4))[0]
        data=np.frombuffer(fb.read(),np.int32)
        data_b=Decodage_LZW(list(data))
        data_bb=freq_from_uniq(data_b)
        data_audio=np.array(data_bb)
        data_hand_orgi=((data_audio/ ((2**8)-1))*n_max) +o_min
        rounded_data=np.round(data_hand_orgi)
        rounded_data = rounded_data.astype(np.int16)
        fb.close()
        mse=MSE(rounded_data )
        psnr=PSNR(rounded_data )
        
    return f"\n\n indicateur de format:{indicateur}\n\n frequence d'echantillonage:{freq}\n\n nombre de canaux:{nbr_canaux}\n\n profondeur en bit:{profendeur}\n\n la valeur de MSE:{mse}\n\n la valeur de PSNR:{psnr}"
def get_files_names(cwd,extensions):
    files = []
    for file in os.listdir(cwd):
        if file.endswith(extensions):
            files.append(os.path.basename(file))
    return files
extensions = ('.mp3', '.wav','.flac','.mp2','.aac','.ogg','.irm','au')
        

class MusicPlayer():
    def __init__(self,root):
        self.root = root
        # Title of the window
        self.root.title("MusicPlayer")
        # Window Geometry
        self.root.geometry("1070x300")
        self.root.resizable(False, False)
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()

        # Creating the Track Frames for Song label & status label
        trackframe = LabelFrame(self.root,text="Song Track",font=("Mona Sans",15,"bold"),bg="#b7dffd",fg="white",bd=5,relief=GROOVE)
        trackframe.place(x=300,y=0,width=500,height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe,textvariable=self.track,width=20,font=("Mona Sans",18,"bold"),bg="Orange",fg="gold").grid(row=0,column=0,padx=10,pady=5)

        
        # Inserting Status Label
        trackstatus = Label(trackframe,textvariable=self.status,font=("Mona Sans",18,"bold"),bg="orange",fg="gold").grid(row=0,column=1,padx=10,pady=5)

            # Creating Button Frame
        buttonframe = LabelFrame(self.root, text="Control Panel", font=("Mona Sans",15,"bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        buttonframe.place(x=300, y=100, width=500, height=100)

        # Inserting Play Button
        playbtn = Button(buttonframe, text="PLAYSONG", command=self.play_hand, width=10, height=1, font=("Mona Sans",16,"bold"), fg="navyblue", bg="pink").grid(row=0, column=0, padx=10, pady=5)

        # Inserting Pause Button
        pausebtn = Button(buttonframe, text="PAUSE", command=self.stop_hand, width=8, height=1, font=("Mona Sans",16,"bold"), fg="navyblue", bg="pink").grid(row=0, column=1, padx=10, pady=5)

        # Inserting Browse Button
        browsebtn = Button(buttonframe, text="BROWSE", command=self.browse_file, width=8, height=1, font=("Mona Sans",16,"bold"), fg="navyblue", bg="pink").grid(row=0, column=2, padx=10, pady=5)
        
        # Creating Convert Frame
        convertframe = LabelFrame(self.root,text="Convert Panel",font=("Mona Sans",15,"bold"),bg="#0E2E2A",fg="white",bd=5,relief=GROOVE)
        convertframe.place(x=300,y=200,width=500,height=100)
        # Inserting Play Button
        convertTo = Label(convertframe,text="To : ", font=("Mona Sans",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=0,padx=10,pady=5)
        
        
        # CODAGE Menu Option
        menu_var = StringVar()
        menu_var.set('Select extension')
        menu_values = ['mp3', 'ogg', 'wav', 'flac', 'mp2', 'aiff', 'au', 'wma', 'aifc','irm']
        menu = OptionMenu(convertframe, menu_var, *menu_values)
        menu.config(fg="white", bg="#222222", width=12) 
        # Afficher le menu déroulant
        menu.grid(row=0,column=1,padx=10,pady=5)


        def getinfo():
            file = self.track.get()
            extension = get_extention(file)
            if extension == 'irm':
                phrase = lire_irm2(file)
            else:
                audio = AudioSegment.from_file(file)
                fe = audio.frame_rate
                nbrc = audio.channels
                smp = audio.sample_width
                ar = np.array(audio.get_array_of_samples())
                mse=MSE(ar)
                psnr=PSNR(ar)
                phrase = "Fréquence d'echantillonage: {}\n\nNombre de canaux: {}\n\nProfondeur en bit: {}\n\n la valeur de MSE:{} \n\n la valeur de PSNR: {}".format(fe, nbrc, smp,mse,psnr)
            
            # Remove the existing Text widget from the panel
            for widget in panel.winfo_children():
                if isinstance(widget, Text):
                    widget.pack_forget()
            
            # Create a new Text widget with the information and pack it into the panel
            info_text = Text(panel, height=10, width=33)
            info_text.insert("1.0", phrase)
            info_text.pack()



        def get_files_names(cwd,extensions):
            files = []
            for file in os.listdir(cwd):
                if file.endswith(extensions):
                    files.append(os.path.basename(file))
            return files

        def get_extention(nomf):
                    i = nomf.rfind(".")
                    if i == -1:
                        return ""
                    else:
                        return nomf[i+1:]

        def convert_to_irm(fichir_original,nomf):
            file = AudioSegment.from_file(file=fichir_original,format=get_extention(fichir_original))
            nbr_canaux=file.channels
            freq=file.frame_rate
            profendeur=file.sample_width
            
            data=np.array(file.get_array_of_samples(),dtype=float)
            
            sapm1=data-np.min(data)
            o_min=np.min(data)
            n_max=np.max(sapm1)
            data_haand=(sapm1/n_max)*((2**8)-1)
            new_new_data=uniq_img(data_haand)
            D,commp_data=Codage_LZW(new_new_data)

            nbr_echa=len(data)//nbr_canaux
            with open(nomf, "wb") as fb:
                fb.write(struct.pack("3s","IRM".encode("ascii")))
                fb.write(struct.pack("i",freq))
                fb.write(struct.pack("i",nbr_canaux))
                fb.write(struct.pack("i",nbr_echa))
                fb.write(struct.pack("i",profendeur))
                fb.write(struct.pack("f",n_max))
                fb.write(struct.pack("f",o_min))
                fb.write(np.array(commp_data).tobytes())
                fb.close()

        def convetir0(nomf_initial,form):
            if not os.path.isfile(nomf_initial):
                raise ValueError(f"Input file '{nomf_initial}' not found")

            file = AudioSegment.from_file(nomf_initial)

            nom_final=nomf_initial[:nomf_initial.index('.')]+'_'+form+'.'+form  

            if form == "wma" or form == "aifc":
                subprocess.call(['ffmpeg','-i',nomf_initial,nom_final])
            else:
                file.export(nom_final,format=form)

       
        def convetir1(nomf_initial,form):
            if form=='irm':
                nom_final=nomf_initial[:nomf_initial.index('.')]+'_'+form+'.'+form 
                convert_to_irm(nomf_initial,nom_final)
            else:
                convetir0(nomf_initial,form)
            
        def convert_irm_to_other(fichir_original,ext):
            with open(fichir_original, "rb") as fb:
                indicateur=struct.unpack("3s", fb.read(3))[0]
                freq=struct.unpack("i", fb.read(4))[0]
                nbr_canaux=struct.unpack("i", fb.read(4))[0]
                nbr_echa=struct.unpack("i", fb.read(4))[0]
                profendeur=struct.unpack("i", fb.read(4))[0]
                n_max=struct.unpack("f", fb.read(4))[0]
                o_min=struct.unpack("f", fb.read(4))[0]
                data=np.frombuffer(fb.read(),np.int32)
                data_b=Decodage_LZW(list(data))
                data_bb=freq_from_uniq(data_b)
                data_audio=np.array(data_bb)
                data_hand_orgi=((data_audio/ ((2**8)-1))*n_max) +o_min
                rounded_data=np.round(data_hand_orgi)
                if profendeur==1:
                    rounded_data = rounded_data.astype(np.int8)
                elif profendeur==2:
                    rounded_data = rounded_data.astype(np.int16)
                elif profendeur==4:
                    rounded_data = rounded_data.astype(np.int32)
                fb.close()
        
            nom_final=fichir_original[:fichir_original.index('.')]+'_'+ext+'.'+ext
            # create new AudioSegment object
            sound = AudioSegment(rounded_data.tobytes(),sample_width=profendeur,frame_rate=freq,channels=nbr_canaux)
            # export new audio file with desired extension
            sound.export(nom_final, format=ext)
       

        def convert():
            exten=menu_var.get()
            ext=get_extention(self.track.get())
            if ext=='irm':
                convert_irm_to_other(self.track.get(),exten)
            else:
                convetir1(self.track.get(),exten)
        

        # Inserting Play Button
        convbtn = Button(convertframe,text="Convert",command = convert,width=10,height=1,font=("Mona Sans",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=2,padx=10,pady=5)
        refreshbtn = Button(convertframe,text="Refresh",command=self.update_playlist,width=10,height=1,font=("Mona Sans",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=3,padx=10,pady=5)
        # Create a panel widget for the calculated information
        panel = Frame(root, width=200, bg='pink')
        panel.pack(side='right', fill='y')

        # Create a label widget inside the panel
        result_label = Label(panel, text='Audio Information', bg='White', font=('Mona Sans', 15))
        result_label.pack(padx=30, pady=20)
        infobtn = Button(panel, text="Get Info", command=getinfo, width=8, height=1, font=("Mona Sans",16,"bold"), fg="navyblue", bg="pink")
        infobtn.pack(side='top', padx=10, pady=5)        
        # Creating Playlist Frame
        songsframe = LabelFrame(self.root,text="Song Playlist",font=("Mona Sans",15,"bold"),bg="grey",fg="white",bd=5,relief=GROOVE)
        songsframe.place(x=0,y=0,width=300,height=295)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe,yscrollcommand=scrol_y.set,selectbackground="green",selectmode=SINGLE,font=("Mona Sans",12,"bold"),bg="silver",fg="navyblue",bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir(os.getcwd())
        # Fetching Songs
        self.playlist.delete(0, END) # clear existing items in listbox
        songtracks = get_files_names(os.getcwd(), extensions)
        for track in songtracks:
            self.playlist.insert(END, track)
     
    def play_hand(self):
            i=0
            while self.playlist.get(ACTIVE)[i]!=".":
                i+=1
            ext=self.playlist.get(ACTIVE)[i+1:]

            if ext=='irm':
                self.track.set(self.playlist.get(ACTIVE))
                # Displaying Status
                self.status.set("-Playing")
            
                lire_irm(self.playlist.get(ACTIVE))
            else:
                def playsong(self):
                    # Displaying Selected Song title
                    self.track.set(self.playlist.get(ACTIVE))
                    # Displaying Status
                    self.status.set("-Playing")
                    # Loading Selected Song
                    pygame.mixer.music.load(self.playlist.get(ACTIVE))
                    # Playing Selected Song
                    pygame.mixer.music.play()
                playsong(self)       
    def stop_hand(self):
        i=0
        while self.playlist.get(ACTIVE)[i]!=".":
            i+=1
        ext=self.playlist.get(ACTIVE)[i+1:]

        if ext=='irm':
            self.status.set("-Paused")
            sd.stop(self.playlist.get(ACTIVE))
        else:
            def pausesong(self):
                # Displaying Status
                self.status.set("-Paused")
                # Paused Song
                pygame.mixer.music.pause()
            pausesong(self)

    def update_playlist(self):
            self.playlist.delete(0, END) # clear existing items in listbox
            songtracks = get_files_names(os.getcwd(), extensions)
            for track in songtracks:
                self.playlist.insert(END, track)
               
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        # update the track variable with the selected file path
        self.track.set(file_path)

def main():
    root = Tk()
    MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()