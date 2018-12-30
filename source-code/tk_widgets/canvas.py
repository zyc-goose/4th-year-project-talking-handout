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
        self.canvas.bind('<Button-1>', self.handleClickB1)
        self.canvas.bind('<B1-Motion>', self.handleMotionB1)
        self.canvas.bind('<B1-ButtonRelease>', self.handleReleaseB1)
        self.canvas.bind('<Motion>', self.handleMotion)
        # Listeners
        self.addListener('<ResponseRects>', self.handleResponseRects)
        # Set Initial State
        self.setState(
            image=None, page=0, width=350, height=495,
            rects=[]
        )
    
    def insideRect(self, rect, x, y):
        x0, y0, x1, y1 = self.decodeRect(*rect['coords'])
        return x0 <= x <= x1 and y0 <= y <= y1
    
    def findRectAt(self, x, y):
        rects = self.state['rects']
        for rect in rects:
            if self.insideRect(rect, x, y):
                return rect
        return None
    
    def encodeRect(self, x0, y0, x1, y1):
        """From canvas coordinates to PDF coordinates."""
        canvasWidth, canvasHeight = self.state['width'], self.state['height']
        imageWidth, imageHeight = self.state['image'].size
        nx0 = int(x0 / canvasWidth * imageWidth)
        nx1 = int(x1 / canvasWidth * imageWidth)
        ny0 = int(y0 / canvasHeight * imageHeight)
        ny1 = int(y1 / canvasHeight * imageHeight)
        return (nx0, ny0, nx1, ny1)
    
    def decodeRect(self, nx0, ny0, nx1, ny1):
        """From PDF coordinates to canvas coordinates."""
        canvasWidth, canvasHeight = self.state['width'], self.state['height']
        imageWidth, imageHeight = self.state['image'].size
        x0 = int(nx0 / imageWidth * canvasWidth)
        x1 = int(nx1 / imageWidth * canvasWidth)
        y0 = int(ny0 / imageHeight * canvasHeight)
        y1 = int(ny1 / imageHeight * canvasHeight)
        return (x0, y0, x1, y1)
    
    def drawRects(self):
        # Delete existing rects
        self.canvas.delete('inscreen')
        # Draw new rects
        rects = self.state['rects']
        for rect in rects:
            color = 'red' if rect['selected'] else 'blue'
            canvasID = self.canvas.create_rectangle(
                *self.decodeRect(*rect['coords']),
                fill='', outline=color,
                tags=('inscreen',)
            )
            rect['canvasID'] = canvasID
    
    def requestRects(self):
        event = dict(name='<RequestRects>', page=self.state['page'])
        self.emitEvent('MainFrame', event)
    
    def handleResponseRects(self, event):
        # Delete existing rects
        self.setState(rects=event['rects'])
    
    def handleMotion(self, event):
        # Find rect under cursor
        tarRect = self.findRectAt(event.x, event.y)
        tarRectID = tarRect['id'] if tarRect else None
        # Update rectangle highlighting
        for rect in self.state['rects']:
            if rect['id'] == tarRectID:
                self.canvas.itemconfig(rect['canvasID'], outline='orange')
            else:
                self.canvas.itemconfig(rect['canvasID'], outline='blue')
    
    def handleClickB1(self, event):
        # Show event and coordinates
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<Button-1>' + coord)
        # Create active rectangle
        self.activeRect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, fill='', outline='green')
        self.arX, self.arY = event.x, event.y
    
    def handleMotionB1(self, event):
        # Show event and coordinates
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<B1-Motion>' + coord)
        # Update coordinates of active rectangle
        self.canvas.coords(self.activeRect, self.arX, self.arY, event.x, event.y)
    
    def handleReleaseB1(self, event):
        # Show event and coordinates
        coord = ' pos=(%d,%d)' % (event.x, event.y)
        self.updateStatusBar('<B1-ButtonRelease>' + coord)
        # Send active rectangle as event
        event = dict(
            name='<NewRectFinished>',
            page=self.state['page'],
            coords=self.encodeRect(*self.canvas.coords(self.activeRect))
        )
        self.emitEvent('MainFrame', event)
        # Remove active rectangle
        self.canvas.delete(self.activeRect)
        self.activeRect = None
        # Request updated rectangles
        self.requestRects()
    
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
            self.drawRects()
        