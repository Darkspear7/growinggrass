#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Fix word storage model """

import sys
from PyQt4 import QtGui, QtCore

WordDelim = {'space','tab'}
LineDelim = {'newline'}

keyMapper  = {0x20:'space',0x01000001:'tab',0x01000004:'newline',0x01000012:'left',0x01000014:'right',0x01000013:'up',0x01000015:'up'}

BrainiacStates = ['Linear','LR']
BrainiacCursorEvents = ['MoveLeft','MoveRight','MoveUp','MoveDown']
BrainiacKeyEvents = ['TypeWordDelim','TypeLineDelim','TypeAbc']



class Brainiac:
    state = BrainiacStates[0]
    def checkState(self):
        pass
    def changeState(self):
        pass
    def LinearMethod(self):
        pass
    def LRMethod(self):
        pass
    def processEvent(self,keycode):
        self.mapKeyCodeToEvent(keycode)
        
        
    def mapKeyCodeToEvent(self,keycode):
        # keycodes are used from PyQt4
        return keyMapper[keycode]

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        self.brain = Brainiac()
        super(SmartTextbox, self).__init__()
        self.doc = self.document()
        self.cursor = self.textCursor()
    
    def keyPressEvent(self , event):
        self.brain.processEvent(event.key())
        QtGui.QTextEdit.keyPressEvent(self, event)
        pos = self.textCursor().position()
        print(str(pos) +" : "+ self.doc.characterAt(pos-1) +", "+ self.doc.characterAt(pos))

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
    
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
