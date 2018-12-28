from tkinter import *
from tkinter import ttk

from component import Component
from canvas import MainCanvas

from PIL import Image, ImageTk
import pdf2image

class PDFViewer(Component):
    def __init__(self, parent, abspath=None):
        super().__init__(parent, 'PDFViewer')
        # Read PDF images
        try:
            self.images = pdf2image.convert_from_path(abspath)
        except:
            self.images = None
        # Main PDF Canvas
        self.canvas = MainCanvas(self)
        
        # PDF Page Navigator
        self.navigator = Navigator(self)
        # Grid Configuration
        self.canvas.grid(row=0, column=0, sticky=(N,S,E,W))
        self.navigator.grid(row=1, column=0)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.columnconfigure(0, weight=1)
        # Listeners
        self.addListener('<PageChange>', self.handlePageChange)
        # Set Initial State
        if self.images:
            curPage, totalPage = 1, len(self.images)
        else:
            curPage, totalPage = 0, 0
        self.setState(
            curPage=curPage, totalPage=totalPage,
            images=self.images
        )
    
    def handlePageChange(self, event):
        self.setState(curPage=event['newPage'])
    
    def afterSetState(self):
        curPage, totalPage = self.state['curPage'], self.state['totalPage']
        if curPage > 0:
            image = self.state['images'][curPage - 1]
        else:
            image = None
        self.navigator.setState(curPage=curPage, totalPage=totalPage)
        self.canvas.setState(image=image)


class Navigator(Component):
    def __init__(self, parent):
        super().__init__(parent, 'Navigator')
        # Navigation Buttons
        self.prevButton = ttk.Button(self.frame, text='prev')
        self.nextButton = ttk.Button(self.frame, text='next')
        # Label for Page Number
        self.pageStrVar = StringVar()
        self.pageLabel = ttk.Label(self.frame, textvariable=self.pageStrVar)
        # Grid Configuration
        self.prevButton.grid(row=0, column=0)
        self.nextButton.grid(row=0, column=2)
        self.pageLabel.grid(row=0, column=1)
        # Bindings
        self.prevButton.configure(command=self.onClickPrev)
        self.nextButton.configure(command=self.onClickNext)
        # Set Initial State
        self.setState(curPage=0, totalPage=0)
    
    def afterSetState(self):
        self.pageStrVar.set('%d / %d' % 
            (self.state['curPage'], self.state['totalPage'])
        )
    
    def onPageChange(self, newPage):
        event = dict(name='<PageChange>', newPage=newPage)
        self.emitEvent('PDFViewer', event)
    
    def onClickPrev(self):
        curPage, totalPage = self.state['curPage'], self.state['totalPage']
        if curPage > 1:
            self.onPageChange(curPage - 1)
    
    def onClickNext(self):
        curPage, totalPage = self.state['curPage'], self.state['totalPage']
        if curPage < totalPage:
            self.onPageChange(curPage + 1)

