#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Fix word storage model """

import sys
from PyQt4 import QtGui, QtCore

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox, self).__init__()
        self.words = []
        self.chars = []
    
    def keyPressEvent(self , event):
        if event.key() == QtCore.Qt.Key_Space:
            if self.chars != []:
                word = ""
                for c in self.chars:
                    word = word + c
                self.words.append(word)
                self.chars = []
                
            text = ""
            for w in self.words:
                text = text + w + "\n"
            QtGui.QMessageBox.about(self,'Message', text)
        elif event.key() == QtCore.Qt.Key_Backspace:
            if self.chars != []:
                self.chars.pop()
        elif event.text() != []:
            self.chars.append(event.text())
        
        QtGui.QTextEdit.keyPressEvent(self, event)

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):               
        textEdit = SmartTextbox()
        self.setCentralWidget(textEdit)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  