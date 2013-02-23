# Event class for smartbox, most events are either a key event or
# a cursor event

from functools import reduce
from PyQt4 import QtGui, QtCore

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

class StringBuffer:
    def getString(self): pass
    def getSubstring(self, start, length): pass
    def find(self, string): pass
    def findForward(self, start, string): pass
    def findBackward(self, start, string): pass
    def replace(self, match, replace): pass
    def replaceForward(self, match, replace, start): pass
    def replaceBackward(self, match, replace, start): pass
    def getCharAt(self, pos): pass
    def insert(self, string, pos): pass
    def append(self, string): pass
    def remove(self, start, length): pass
    def getLength(self): pass

NonPrintable = {'\x00','\x0003','\u2029','\0'}

class QtStringBuffer(StringBuffer):
    def __init__(self, textCursor):
        self.cursor = textCursor
        self.doc = self.cursor.document()
    def getString(self):
        return self.doc.toPlainText()
    def getSubstring(self, start, length):
        # first get the range of indices
        # map those to get the characters at the indices
        # reduce the list of characters to a string
        chars = list(map(lambda x: self.doc.characterAt(x), range(start, start+length)))
        if not len(chars) > 0:
            return None
        return reduce(lambda cur, prev: cur + prev, chars)
    def find(self, string):
        position = self.doc.find(string).position()
        return position - len(string)
    def findForward(self, string, start):
        position = self.doc.find(string, start).position()
        print(string+", "+str(len(string)))
        return position - len(string)
    def findBackward(self, string, start): 
        position =  self.doc.find(string, start, QtGui.QTextDocument.FindBackward).position()
        return position - len(string)
    def replace(self, match, replace):
        print(self.cursor.position())
        pos = self.find(match)
        if not pos == None:
            self.remove(pos, len(match))
            self.insert(replace, pos)
    def replaceForward(self, match, replace, start): 
        print(self.cursor.position())
        pos = self.findForward(match, start)
        if not pos == None:
            self.remove(pos, len(match))
            self.insert(replace, pos)        
    def replaceBackward(self, match, replace, start): 
        print(self.cursor.position())
        pos = self.findBackward(match, start)
        if not pos == None:
            self.remove(pos, len(match))
            self.insert(replace, pos)
    def insert(self, string, pos):
        if pos >= self.doc.characterCount(): pos = self.getLength() - 1
        current = self.cursor.position()
        self.cursor.setPosition(pos)
        self.cursor.insertText(string)
        if current >= self.doc.characterCount(): current = self.getLength() - 1
        self.cursor.setPosition(current)
    def append(self, string): 
        self.insert(string, self.doc.characterCount() - 1)
    def remove(self, start, length):
        current = self.cursor.position()
        print(current)
        self.cursor.setPosition(start)
        for x in range(length): self.cursor.deleteChar()
        if current >= self.doc.characterCount(): current = self.getLength() - 1
        self.cursor.setPosition(current)
    def getLength(self):
        return self.doc.characterCount()
    def getCharAt(self, pos):
        return self.doc.characterAt(pos)
    def findChar(self, char):
        for x in range(0, self.getLength()):
            c = self.doc.characterAt(x)
            if c == char:
                return x
        return None
    def findCharForward(self, char, start):
        for x in range(start, self.getLength()+2):
            c = self.doc.characterAt(x)
            if c == char:
                return x
        return None        
    def findCharBackward(self, char, start):
        for x in range(-1, start)[::-1]:
            c = self.doc.characterAt(x)
            if c == char:
                return x
        return None
