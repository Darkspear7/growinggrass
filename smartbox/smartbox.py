#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from parser import *
from PyQt4 import QtGui, QtCore

WordDelimiters = {0x020,0x01000001}
LineDelimiters = {0x01000004}

CursorMoveKeys = {0x01000012,0x01000013,0x01000014,0x01000015}


class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox,self).__init__()
        self.doc = self.document()
        self.parser = Parser()
    def keyPressEvent(self , event):
        QtGui.QTextEdit.keyPressEvent(self, event)
        cursor = self.textCursor()
        pos = cursor.position()
        if event.key() in CursorMoveKeys:
            toProc = Event('cursor')
            if event.key() == 0x01000012: toProc.addAttribute('dir','l')
            elif event.key() == 0x01000013: toProc.addAttribute('dir','u')
            elif event.key() == 0x01000014: toProc.addAttribute('dir','r')
            elif event.key() == 0x01000015: toProc.addAttribute('dir','d')
        else:
            toProc = Event('key')
            toProc.addAttribute('char', event.text())
        
        #a = self.doc.characterAt(pos-1)
        #print(a.encode('ascii'))
        toProc.addAttribute('left', self.doc.characterAt(pos-1))
        toProc.addAttribute('right',self.doc.characterAt(pos))    
        self.parser.addEvent(toProc)
        self.parser.process(self.doc.toPlainText(), pos)

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
