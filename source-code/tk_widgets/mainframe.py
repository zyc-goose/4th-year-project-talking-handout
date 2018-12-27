from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from component import Component
from pdfviewer import PDFViewer

class MainFrame(Component):
    def __init__(self, parent):
        super().__init__(parent, 'MainFrame')
        # Left Frame: PDF Viewer
        pdfpath = filedialog.askopenfilename()
        self.viewer = PDFViewer(self, pdfpath)
        self.viewer.configure(
            width=300, height=300
        )
        # Right Frame: Control Panel
        self.panel = PDFViewer(self)
        self.panel.configure(
            width=300, height=300,
            borderwidth=10, relief='ridge'
        )
        # Grid Configuration
        self.viewer.grid(row=0, column=0, sticky=(N,S,E,W))
        self.panel.grid(row=0, column=1, sticky=(N,S,E,W))
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        # Bindings
        self.frame.bind('<Configure>', self.print)
    
    def print(self, event):
        print(event.width, event.height)