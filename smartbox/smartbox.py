#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from parser import *
from smarty import *
from PyQt4 import QtGui, QtCore

WordDelimiters = {0x020,0x01000001}
LineDelimiters = {0x01000004}

CursorMoveKeys = {0x01000012,0x01000013,0x01000014,0x01000015}


class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox,self).__init__()
        self.doc = self.document()
        self.sstream = QtStringBuffer(self.textCursor())
        self.nav = NavigationModule(self.sstream)
    def keyPressEvent(self , event):
        if event.key() in CursorMoveKeys:
            if event.key() == 0x01000012:
                self.nav.move('left')
            elif event.key() == 0x01000014:
                self.nav.move('right')
        else:
            self.nav.move('right', event.text())
        QtGui.QTextEdit.keyPressEvent(self, event)
        #print(self.doc.characterAt(1).encode('ascii'))

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
