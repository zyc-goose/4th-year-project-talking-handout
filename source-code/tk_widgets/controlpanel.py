from tkinter import *
from tkinter import ttk

from component import Component
from pageseg import PageSegmentation
from textrec import TextRecognition

class ControlPanel(Component):
    def __init__(self, parent):
        super().__init__(parent, 'ControlPanel')
        # Mode Selector
        self.selector = ModeSelector(self)
        self.selector.configure(padding=10)
        # Mode Container
        self.container = ModeContainer(self)
        self.container.configure(padding=10)
        # Grid Configuration
        self.selector.grid(row=0, column=0, sticky=NSEW)
        self.container.grid(row=1, column=0, sticky=NSEW)


class ModeSelector(Component):
    def __init__(self, parent):
        super().__init__(parent, 'ModeSelector')
        # Labelled Frame
        self.labelframe = ttk.Labelframe(self.frame)
        self.labelframe.configure(text='Mode Selector', padding=10)
        # Radio Buttons
        self.mode = StringVar()
        self.rbPageSeg = ttk.Radiobutton(self.labelframe)
        self.rbPageSeg.configure(
            text='Page Segmentation',
            variable=self.mode, value='PageSeg',
            command=self.onModeChange
        )
        self.rbTextRec = ttk.Radiobutton(self.labelframe)
        self.rbTextRec.configure(
            text='Text Recognition',
            variable=self.mode, value='TextRec',
            command=self.onModeChange
        )
        # Grid Configuration
        self.labelframe.grid(row=0, column=0, sticky=NSEW)
        self.rbPageSeg.grid(row=0, column=0, sticky=W)
        self.rbTextRec.grid(row=1, column=0, sticky=W)

    def onModeChange(self):
        print('onModeChange')
        event = dict(name='<ModeChange>', mode=self.mode.get())
        self.emitEvent('ControlPanel', event)


class ModeContainer(Component):
    def __init__(self, parent):
        super().__init__(parent, 'ModeContainer')
        # Modes
        self.mode = None
        self.modeEntity = None
        # Page Segmentation Mode
        self.pageSegMode = PageSegmentation(self)
        # Text Recognition Mode
        self.textRecMode = TextRecognition(self)
        # Listeners
        self.addListener('<ModeChange>', self.handleModeChange)
    
    def handleModeChange(self, event):
        print('handleModeChange')
        # Hide previous mode
        if self.modeEntity:
            self.modeEntity.forget()
        # Show new mode
        modeName = event['mode']
        print(modeName)
        if modeName == 'PageSeg':
            self.modeEntity = self.pageSegMode
        elif modeName == 'TextRec':
            self.modeEntity = self.textRecMode
        else:
            self.modeEntity = None
        print(self.modeEntity)
        if self.modeEntity:
            self.modeEntity.grid(row=0, column=0)