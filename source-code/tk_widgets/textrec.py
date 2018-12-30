from tkinter import *
from tkinter import ttk

from component import Component

class TextRecognition(Component):
    def __init__(self, parent):
        super().__init__(parent, 'TextRecognition')
        # Labelled Frame
        self.labelframe = ttk.Labelframe(self.frame)
        self.labelframe.configure(text='Text Recognition', padding=10)
        # Buttons
        self.buttonNew = ttk.Button(self.labelframe)
        self.buttonNew.configure(
            text='Fuck'
        )
        self.buttonOpen = ttk.Button(self.labelframe)
        self.buttonOpen.configure(
            text='Shit'
        )
        self.buttonSave = ttk.Button(self.labelframe)
        self.buttonSave.configure(
            text='Bitch'
        )
        # Grid Configuration
        self.labelframe.grid(row=0, column=0, sticky=NSEW)
        self.buttonNew.grid(row=0, column=0, sticky=W)
        self.buttonOpen.grid(row=0, column=1)
        self.buttonSave.grid(row=0, column=2, sticky=E)