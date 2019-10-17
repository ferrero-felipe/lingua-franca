import tkinter as tk
from tkinter import ttk
from recording import record, play
import pygubu
from identify import identify, createGraph
from functions import getAudio
import soundfile as sf
from PIL import Image, ImageTk
import os
from tkinter.filedialog import askopenfilename

class Application(object):
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.withdraw()
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file

        builder.add_from_file('gui.ui')
        
        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', self.root)
        builder.connect_callbacks(self)
        self.status = self.builder.get_object('label')
        self.plot = self.builder.get_object('plot')

        # STARTING IMAGE
        img = Image.open('copy.png')
        img.thumbnail((350,219), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(img)
        self.plot.configure(image=tkimage)
        self.plot.image = tkimage # keep a reference!
        self.plot.pack()


        self.audio = []
        self.sr = 44100
    
    def make_recording(self):
        self.status.configure(text='Recording...')
        self.root.update_idletasks()
        self.audio, self.sr = record()
        self.status.configure(text='Ready to identify.')
        createGraph()
        self.plotGraph()
        self.root.update_idletasks()

    def play_recording(self):
        play(self.audio, sr=self.sr)
        print(self.audio)

    def load_recording(self):
        audio = askopenfilename()
        self.audio, self.sr = getAudio(audio)
        sf.write('../data/test.ogg', self.audio, self.sr)
        self.status.configure(text='Ready to identify.')
        createGraph()
        self.plotGraph()
        self.root.update_idletasks()

    def identify_recording(self):
        language = identify()
        self.status.configure(text=language)
        self.root.update_idletasks()

    def plotGraph(self):
        img = Image.open('graph.png')
        img.thumbnail((350,219), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(img)
        self.plot.configure(image=tkimage)
        self.plot.image = tkimage # keep a reference!
        self.plot.pack()
       
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
    print('Thank You.')