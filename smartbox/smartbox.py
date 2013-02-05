#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from utils import *
from PyQt4 import QtGui, QtCore

WordDelimiters = {0x020,0x01000001}
LineDelimiters = {0x01000004}

CursorMoveKeys = {0x01000012,0x01000013,0x01000014,0x01000015}

class Parser:
    state = 'linear'
    def checkState(self, event):
        pass
    def processEvent(self, event):
        if event.isKeyEvent():
            a = 1
            #print("got key event")
            #print(event.getAttrib('left')+" : "+event.getAttrib('right'))
        else:
            a = 1
            #print("got cursor event")
            #print(event.getAttrib('left')+" : "+event.getAttrib('right'))
    def __useLinearMethod(self, event):
        pass
    def __useLRMethod(self, event):
        pass

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox,self).__init__()
        self.doc = self.document()
        self.parser = Parser()
    def keyPressEvent(self , event):
        QtGui.QTextEdit.keyPressEvent(self, event)
        cursor = self.textCursor()
        print(cursor.position())
        if event.key() in CursorMoveKeys:
            toProc = Event('cursor')
            toProc.addAttrib('left', self.doc.characterAt(cursor.position()-1))
            toProc.addAttrib('right',self.doc.characterAt(cursor.position()))
        else:
            toProc = Event('key')
            toProc.addAttrib('left', self.doc.characterAt(cursor.position()-1))
            toProc.addAttrib('right',self.doc.characterAt(cursor.position()))
        
        self.parser.checkState(toProc)
        self.parser.processEvent(toProc)

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
    #print("In progress...")
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
