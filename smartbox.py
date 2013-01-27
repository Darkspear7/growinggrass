#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Fix word storage model """

import sys
from PyQt4 import QtGui, QtCore

def enum(*sequential, **named):
    enums = dict(zip(sequential,range(len(sequential))),**named)
    return type('Enum',(),enums)

BrainiacStates = enum('Linear','LR')

class Brainiac:
    state = BrainiacStates.Linear;

    def processEvent():
        pass

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox, self).__init__()
    
    def keyPressEvent(self , event):
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
