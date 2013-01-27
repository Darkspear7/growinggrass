#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Fix word storage model """

import sys
from PyQt4 import QtGui, QtCore

WordDelim = ['Space','Tab']
LineDelim = ['NewLine']

BrainiacStates = ['Linear','LR']
BrainiacCursorEvents = ['MoveLeft','MoveRight','MoveUp','MoveDown']
BrainiacKeyEvents = ['TypeWordDelim','TypeLineDelim','TypeAbc']

class Brainiac:
    state = BrainiacStates['Linear'];
    def checkState():
        pass
    def changeState():
        pass
    def LinearMethod():
        pass
    def LRMethod():
        pass
    def processEvent():
        pass
    def mapKeyCodeToEvent(keycode):
        # keycodes are used from PyQt4
        if keycode == 0x01000012:
            return BrainiacCursorEvents.['MoveLeft']
        elif keycode == 0x01000014:
            return BrainiacCursorEvents['MoveRight']
        elif keycode == 0x01000013:
            return BrainiacCursorEvents['MoveUp']
        elif keycode == 0x01000015:
            return BrainiacCursorEvents['MoveDown']
        elif keycode == 0x01000004:
            return BrainiacKeyEvents['TypeLineDelim']
        elif keycode == 0x01000001:
            return == BrainiacKeyEvents['TypeWordDelim']
        elif keycode == 0x20:
            return == BrainiacKeyEvents['TypeWordDelim']
        elif keycode >= 0x21 and keycode <= 0x0ff:
            return == keycode

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox, self).__init__()
    
    def keyPressEvent(self , event):
        print(str(event.key())+" : "+event.text())
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
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
