from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from component import Component
from uuid import uuid4
import json, os

class PageSegmentation(Component):
    def __init__(self, parent):
        super().__init__(parent, 'PageSegmentation')
        # Current Active File
        self.filepath = ''
        self.filebuf = []
        # Labelled Frame
        self.labelframe = ttk.Labelframe(self.frame)
        self.labelframe.configure(text='Page Segmentation', padding=10)
        # File IO Buttons
        self.buttonNew = ttk.Button(self.labelframe)
        self.buttonNew.configure(
            text='New', command=self.onClickNew
        )
        self.buttonOpen = ttk.Button(self.labelframe)
        self.buttonOpen.configure(
            text='Open', command=self.onClickOpen
        )
        self.buttonSave = ttk.Button(self.labelframe)
        self.buttonSave.configure(
            text='Save', command=self.onClickSave
        )
        # Mode Related Buttions
        self.modeButtons = ttk.Frame(self.labelframe)
        self.varListen = StringVar()
        self.buttonListen = ttk.Button(self.modeButtons)
        self.buttonListen.configure(
            textvariable=self.varListen, command=self.onClickListen
        )
        self.buttonDelete = ttk.Button(self.modeButtons)
        self.buttonDelete.configure(
            text='Delete', command=self.onClickDelete
        )
        # Current File Name
        self.varFileName = StringVar()
        self.filenameLabel = ttk.Label(self.labelframe)
        self.filenameLabel.configure(
            textvariable=self.varFileName, padding=(1,5)
        )
        # Listeners
        self.addListener('<RequestRects>', self.handleRequestRects)
        self.addListener('<SelectRect>', self.handleSelectRect)
        self.addListener('<DeselectRect>', self.handleDeselectRect)
        self.addListener('<FileBufferChanged>', self.handleFileBufferChanged)
        # Grid Configuration
        self.labelframe.grid(row=0, column=0, sticky=NSEW)
        self.buttonNew.grid(row=0, column=0, sticky=W)
        self.buttonOpen.grid(row=0, column=1)
        self.buttonSave.grid(row=0, column=2, sticky=E)
        self.filenameLabel.grid(row=1, column=0, columnspan=3, sticky=W)
        self.modeButtons.grid(row=2, column=0, columnspan=3)
        self.buttonListen.grid(row=0, column=0)
        self.buttonDelete.grid(row=0, column=1)
        # Initial State
        self.setState(filename='', listen=False, modified=False)
    
    def setFilePath(self, filepath):
        self.filepath = filepath
        self.setState(filename=os.path.basename(filepath))
    
    def readFile(self, filepath):
        if not filepath:
            return False
        with open(filepath, 'r') as fin:
            self.filebuf = json.load(fin)
            print(self.filebuf)
        return True
    
    def writeFile(self, filepath):
        if not filepath:
            return False
        with open(filepath, 'w') as fout:
            json.dump(self.filebuf, fout, indent=4)
        return True
    
    def onClickNew(self):
        filepath = filedialog.asksaveasfilename()
        if filepath:
            self.setFilePath(filepath)
            self.filebuf = []
            event = dict(name='<FileBufferChanged>', modified=True)
            self.emitEvent('MainFrame', event)
    
    def onClickOpen(self):
        filepath = filedialog.askopenfilename()
        if self.readFile(filepath):
            self.setFilePath(filepath)
            event = dict(name='<FileBufferChanged>', modified=False)
            self.emitEvent('MainFrame', event)
    
    def onClickSave(self):
        if self.writeFile(self.filepath):
            self.updateStatusBar('File saved')
            self.setState(modified=False)
    
    def onClickListen(self):
        if self.state['listen']:
            self.setState(listen=False)
            self.removeListener('<NewRectFinished>', self.handleNewRectFinished)
        else:
            self.setState(listen=True)
            self.addListener('<NewRectFinished>', self.handleNewRectFinished)
    
    def onClickDelete(self):
        prevlen = len(self.filebuf)
        self.filebuf = list(filter(
            lambda x: x['selected'] == False, self.filebuf
        ))
        numDeleted = prevlen - len(self.filebuf)
        if numDeleted:
            event = dict(name='<FileBufferChanged>', modified=True)
            self.emitEvent('MainFrame', event)
            self.updateStatusBar('Deleted %d rectangle(s)' % (numDeleted))
    
    def handleNewRectFinished(self, event):
        rect = dict(
            id=str(uuid4()),
            page=event['page'],
            selected=False,
            coords=event['coords']
        )
        self.filebuf.append(rect)
        self.updateStatusBar('New Rectangle Received')
        event = dict(name='<FileBufferChanged>', modified=True)
        self.emitEvent('MainFrame', event)
    
    def handleRequestRects(self, event):
        res = dict(
            name='<ResponseRects>',
            rects=list(filter(lambda x: x['page'] == event['page'], self.filebuf))
        )
        self.emitEvent('MainFrame', res)
    
    def handleSelectRect(self, event):
        for rect in self.filebuf:
            if rect['id'] == event['id']:
                rect['selected'] = True
            else:
                rect['selected'] = False
    
    def handleDeselectRect(self, event):
        for rect in self.filebuf:
            rect['selected'] = False
    
    def handleFileBufferChanged(self, event):
        self.setState(modified=event['modified'])
    
    def afterSetState(self):
        fileStr = 'Current File: '
        if self.state['filename']:
            status = '(modified)' if self.state['modified'] else '(saved)'
            fileStr += self.state['filename'] + status
        self.varFileName.set(fileStr)
        if self.state['listen']:
            self.varListen.set('Listen: ON')
        else:
            self.varListen.set('Listen: OFF')
