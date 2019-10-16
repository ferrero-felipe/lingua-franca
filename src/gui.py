import tkinter as Tk
from tkinter import ttk
from tkinter import StringVar
from tkinter.ttk import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import specgram
from recording import record, play
plt.style.context("classic")

class GuiApp():
    def __init__(self):
        self.root = Tk.Tk()
        self.root.title('Lingua Franca')
        self.root.geometry('700x600')
        self.btn_start = Tk.Button(self.root, text="Record", command=self.make_recording)
        self.btn_start.grid(column=0, row=0, sticky='we', padx=20, pady=10)
        self.btn_play = Tk.Button(self.root, text="Play", command=self.play_recording)
        self.btn_play.grid(column=0, row=1, sticky='ew', padx=20)
        self.btn_load = Tk.Button(self.root, text="Load File", command=self.load_recording)
        self.btn_load.grid(column=0, row=2, sticky='ewn', padx=20, pady=10)
        self.status_v = StringVar()
        self.status_v.set("No audio yet.")
        self.status = Label(self.root, textvariable=self.status_v)
        self.status.grid(column=0, row=3, columnspan=2, sticky='ewn', padx=20, pady=20)
        self.audio = []

    def make_recording(self):
        self.status_v.set('Recording...')
        self.root.update_idletasks()
        self.audio = record()
        self.status_v.set('Ready to identify.')
        self.root.update_idletasks()

    def play_recording(self):
        play(self.audio)
        print(self.audio)


    def load_recording(self):
        self.status_v.set('Ready to identify.')
        self.root.update_idletasks()

if __name__ == '__main__':
    gui = GuiApp()
    gui.root.mainloop()
    print('Thank you!')