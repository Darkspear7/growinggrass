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
    def print(self):
        print("Delimiter : " + self.name + " ,keycode : " + str(self.keycode))
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

class Brainiac:
    def __init__(self):
        self.cursor = Cursor()
        self.delimiters = []
        self.delimiters.append(Delimiter(0x20,"space"))
        self.delimiters.append(Delimiter(0x01000001,"tab"))

    def checkState(self):
        pass
    def changeState(self):
        pass
    def LinearMethod(self):
        pass
    def LRMethod(self):
        pass
    def print(self):
        print(self.delimiters)

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        self.brain = Brainiac()
        for x in self.brain.delimiters:
            x.print()
        super(SmartTextbox, self).__init__()
        self.doc = self.document()
        self.cursor = self.textCursor()
    
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
