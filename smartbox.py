#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Fix word storage model """

import sys
from PyQt4 import QtGui, QtCore

class Delimiter:
    def __init__(self, keycode, name):
        self.keycode = keycode
        self.name = name
    def getKeycode(self):
        return self.keycode
    def getName(self):
        return self.name
class Cursor:
    def __init__(self):
        self.position = -1
        self.left = -1
        self.right = -1
    def setPosition(self, pos):
        self.position = pos
    def setToLeft(self, char):
        self.left = char
    def setToRight(self, char):
        self.right = char
    def getPosition(self):
        return self.position
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right

class KeyEvent:
    def __init__(self,key):
        self.key = key
    def print(self):
        if self.key in Delim:
            
        print(self.key)

class CursorEvent:
    def __init__(self,key,pos,charLeft,charRight):
        if key == 0x01000012:
            self.direction = "left"
        elif key == 0x01000014:
            self.direction = "right"
        elif key == 0x01000013:
            self.direction = "up"
        elif key == 0x01000015:
            self.direction = "down"
        self.position = pos
        self.left = charLeft
        self.right = charRight
    def print(self):
        print("move : " + self.direction + " where left: " + self.left + ", right: " + self.right) 

class Brainiac:
    def __init__(self):
        self.cursor = Cursor()
    def checkState(self):
        pass
    def changeState(self):
        pass
    def LinearMethod(self):
        pass
    def LRMethod(self):
        pass
    def processKeyEvent(self,event):
        event.print()
    def processCursorEvent(self,event):
        event.print()

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        self.brain = Brainiac()
        super(SmartTextbox, self).__init__()
        self.doc = self.document()
        self.cursor = self.textCursor()
    
    def keyPressEvent(self , event):
        if event.key() in Chars:
            kevent = KeyEvent(event.key())
            self.brain.processKeyEvent(kevent)
        if event.key() in CursorKeys:
            pos = self.textCursor().position()
            cevent = CursorEvent(event.key(),pos,self.doc.characterAt(pos-2),self.doc.characterAt(pos-1))
            self.brain.processCursorEvent(cevent)
        QtGui.QTextEdit.keyPressEvent(self, event)

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
        
    def initUI(self):               
        textEdit = SmartTextbox()
        self.setCentralWidget(textEdit)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()
    
def main():
    app = QtGui.QApplication(sys.argv)
    print(Chars)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
