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
            width=300, height=500,
            borderwidth=4, relief='ridge'
        )
        # Right Frame: Control Panel
        self.panel = PDFViewer(self)
        self.panel.configure(
            width=300, height=500,
            borderwidth=4, relief='ridge'
        )
        # Status Bar
        self.status = StatusBar(self)
        self.status.configure(
            height=30
        )
        # Grid Configuration
        self.viewer.grid(row=0, column=0, sticky=NSEW)
        self.panel.grid(row=0, column=1, sticky=NSEW)
        self.status.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        # Bindings
        self.frame.bind('<Configure>', self.print)
    
    def print(self, event):
        print(event.width, event.height)


class StatusBar(Component):
    def __init__(self, parent):
        super().__init__(parent, 'StatusBar')
        # Status Label
        self.statusText = StringVar()
        self.statusText.set('Ready')
        self.status = ttk.Label(self.frame)
        self.status.configure(textvariable=self.statusText)
        # Listeners
        self.addListener('<StatusUpdate>', self.handleStatusUpdate)
        # Grid Configuration
        self.status.grid(row=0, column=0, sticky=W)
    
    def handleStatusUpdate(self, event):
        self.statusText.set(event['message'])