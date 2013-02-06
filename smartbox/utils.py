# Event class for smartbox, most events are either a key event or
# a cursor event

from collections import namedtuple

EventAttributes = {'left': str, 'right': str}
KeyEventAttributes = {'delim': str,'char': str}
CursorEventAttributes = {'dir': str}

class Event:
    def __init__(self, eventType):
        if eventType == "key":
            self.__type = 1
        elif eventType == "cursor":
            self.__type = 2
        else:
            raise Exception("Invalid event type")
    def isKeyEvent(self):
        return self.__type == 1
    def isCursorEvent(self):
        return self.__type == 2
    def addAttribute(self,name,value):
        valid = self.__addAttr(name, value)
        if self.isKeyEvent():
            valid = valid or self.__addKattr(name, value)
        elif self.isCursorEvent():
            valid = valid or self.__addCattr(name, value)
        if not valid:
            raise Exception("Invalid attribute for event type")
    def getAttribute(self,name):
        return getattr(self, name, None)
    def hasAttribute(self,name):
        return hasattr(self,name)
    def __addKattr(self, name, value):
        if name in KeyEventAttributes:
            if isinstance(value,KeyEventAttributes[name]):
                setattr(self, name, value)
                return True
        return False
    def __addCattr(self, name, value):
        if name in CursorEventAttributes:
            if isinstance(value,CursorEventAttributes[name]):
                setattr(self, name, value)
                return True
        return False
    def __addAttr(self, name, value):
        if name in EventAttributes:
            if isinstance(value,EventAttributes[name]):
                setattr(self, name, value)
                return True
        return False

def readLeft(text, pos, delimiters):
    pass
