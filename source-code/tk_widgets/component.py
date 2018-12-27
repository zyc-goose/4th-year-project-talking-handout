from tkinter import *
from tkinter import ttk

class Component:
    """
    Super class for all Tk components except the root widget.
    """
    def __init__(self, parent, className):
        """
        args:
            parent - Parent component
            className - Name of the component
        """
        self.parent = parent
        self.parent.children.append(self)
        self.children = []
        self.frame = ttk.Frame(parent.frame)
        self.listeners = {}
        self.className = className
        self.state = {}

    def configure(self, **config):
        self.frame.configure(**config)
    
    def grid(self, **config):
        self.frame.grid(**config)
    
    def addListener(self, eventName, callback):
        """Add an event listener to this component. A listener
        is a callback function which will be called when a certain
        event happens."""
        if eventName in self.listeners:
            self.listeners[eventName].append(callback)
        else:
            self.listeners[eventName] = [callback]
    
    def removeListener(self, eventName, callback):
        if eventName in self.listeners:
            self.listeners.pop(eventName)
    
    def emitEvent(self, target, event):
        """Emit an event from this component. The mechanism keeps
        passing the event to parent components until it reaches
        the component with className equals to 'target'."""
        if target == self.className:
            self.handleEvent(event)
        else:
            self.parent.emitEvent(target, event)

    def handleEvent(self, event):
        """The event handling mechanism keeps passing event to
        all child components recursively. In this process, the
        event will be handled in every component which contains
        a matching event listener."""
        eventName = event['name']
        if eventName in self.listeners:
            for callback in self.listeners[eventName]:
                callback(event)
        for child in self.children: # passdown
            child.handleEvent(event)
    
    def setState(self, newState=None, **kwargs):
        """Update self.state with new key-value pairs.
        'self.state' contains necessary information for
        rendering a component. User should implement the
        'self.afterSetState' method in order to re-render
        the component."""
        if isinstance(newState, dict):
            self.state.update(newState)
        self.state.update(**kwargs)
        self.afterSetState()
    
    def afterSetState(self):
        """To be implemented by user."""
        pass
            