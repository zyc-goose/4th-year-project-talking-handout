from tkinter import *
from tkinter import ttk

from component import Component
from PIL import Image, ImageTk
from math import sqrt

class MainCanvas(Component):
    def __init__(self, parent):
        super().__init__(parent, 'MainCanvas')
        # Canvas
        # self.vscroll = ttk.Scrollbar(self.frame, orient=VERTICAL)
        self.canvas = Canvas(self.frame)
        self.canvas.configure(
            width=350, height=600
        )
        # Grid Configuration
        self.canvas.grid(row=0, column=0, sticky=(N,S,E,W))
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        # Bindings
        self.frame.bind('<Configure>', self.handleConfigure)
        self.canvas.bind('<Button-1>', self.handleClick)
        self.canvas.bind('<B1-Motion>', self.handleMotion)
        self.canvas.bind('<B1-ButtonRelease>', self.handleRelease)
        # Set Initial State
        self.setState(image=None, width=350, height=600)
    
    def handleClick(self, event):
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<Button-1>' + coord)
    
    def handleMotion(self, event):
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<B1-Motion>' + coord)
    
    def handleRelease(self, event):
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<B1-ButtonRelease>' + coord)
    
    def handleConfigure(self, event):
        width = event.width
        height = int(width * sqrt(2))
        self.setState(width=width, height=height)
    
    def afterSetState(self):
        image = self.state['image']
        if image:
            width, height = self.state['width'], self.state['height']
            image = image.resize((width, height), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)
        