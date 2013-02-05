# Event class for smartbox, most events are either a key event or
# a cursor event

from collections import namedtuple

EventAttributes = {'left': str, 'right': str}
KeyEventAttributes = {'delim': str,'char': str}
CursorEventAttributes = {'direction': int}

WordDelimiters = {' ','\t'}
LineDelimiters = {'\n','\r'}

def isCharWordDelimiter(char):
    return char in WordDelimiters
def isCharLineDelimiter(char):
    return char in LineDelimiters

class Event:
    """i think this is a documentation string, i`m not sure"""
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
        if self.isKeyEvent():
            testType = (name in KeyEventAttributes)
            testType = (testType and isinstance(value,KeyEventAttributes[name]))
        elif self.isCursorEvent():
            testType = (name in CursorEventAttributes)
            testType = (testType and isinstance(value,CursorEventAttributes[name]))
        
        testType = (testType or  (name in EventAttributes and isinstance(value,EventAttributes[name])))
        if testType:
            setattr(self,name,value)
        else:
            print(name)
            print(KeyEventAttributes)
            print(name in KeyEventAttributes)
            raise Exception("Invalid attribute for event type")
    def getAttribute(self,name):
        return getattr(self, name, None)
    def hasAttribute(self,name):
        return hasattr(self,name)
