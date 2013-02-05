#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from utils import *
from PyQt4 import QtGui, QtCore

WordDelimiters = {0x020,0x01000001}
LineDelimiters = {0x01000004}

CursorMoveKeys = {0x01000012,0x01000013,0x01000014,0x01000015}

class Parser:
    def __init__(self):
        self.state = 'linear'
        self.actions = []
    def checkState(self, event):
        if not event.hasAttribute('left') and not event.hasAttribute('right'):
            raise Exception("check state failed")
        isLchar = not event.getAttribute('left') in {' ','\t','\u2029'}
        isRchar = not event.getAttribute('right') in {' ','\t','\u2029'}
        if (not isLchar) and (not isRchar):
            self.state = 'linear'
        elif isLchar and isRchar:
            self.state = 'lrm'
        elif isLchar and (not isRchar):
            self.state = 'lre'
        elif  (not isLchar) and isRchar:
            self.state = 'lrs'
    def addEvent(self, event):
        if event.isKeyEvent():
            if isCharWordDelimiter(event.getAttribute('char')):
                self.__addEvent('kdw')
            elif isCharLineDelimiter(event.getAttribute('char')):
                self.__addEvent('kdl')
            else:
                self.__addEvent('kc')
        else:
            self.__addEvent('cm')
    def process(self):
        print(self.state)
        print(self.actions)
        case1 = ['kc','cm'] == self.actions
        case2 = ['kc','kdw'] == self.actions
        case3 = ['kc','kdl'] == self.actions
        if self.state == 'linear':
            if case1 or case2 or case3: self.__useLinearMethod()
        elif self.state == 'lrs':
            if case1: self.__useLRMethod(1,'s')
            if case2: self.__useLRMethod(2,'s')
            if case3: self.__useLRMethod(3,'s')
        elif self.state == 'lrm':            
            if case1: self.__useLRMethod(1,'m')
            if case2: self.__useLRMethod(2,'m')
            if case3: self.__useLRMethod(3,'m')
            if ['cm','kdw'] == self.actions: self.__useLRMethod(4,'m')
            if ['cm','kdl'] == self.actions: self.__useLRMethod(4,'m')
        elif self.state == 'lre':
            if case1: self.__useLRMethod(1,'e')
            if case2: self.__useLRMethod(2,'e')
            if case3: self.__useLRMethod(3,'e')
    def __useLinearMethod(self):
        print('using linear for emit')
        self.actions = []
    def __useLRMethod(self, case, subParser):
        if case == 1:
            print('LR emit change word')
        elif subParser == 's':
            print('LRS emit word')
        elif subParser == 'm':
            print('LRM emit change word, change word')
        elif subParser == 'e':
            print('LR emit change word')
        self.actions = []
    def __addEvent(self, chars):
        if len(self.actions) > 0:
            if not self.actions[-1]==chars:
                self.actions.append(chars)
        else:
            self.actions.append(chars)

class SmartTextbox(QtGui.QTextEdit):
    def __init__(self):
        super(SmartTextbox,self).__init__()
        self.doc = self.document()
        self.parser = Parser()
    def keyPressEvent(self , event):
        QtGui.QTextEdit.keyPressEvent(self, event)
        cursor = self.textCursor()
        if event.key() in CursorMoveKeys:
            toProc = Event('cursor')
            toProc.addAttribute('left', self.doc.characterAt(cursor.position()-1))
            toProc.addAttribute('right',self.doc.characterAt(cursor.position()))
        else:
            toProc = Event('key')
            toProc.addAttribute('char', event.text())
            toProc.addAttribute('left', self.doc.characterAt(cursor.position()-1))
            toProc.addAttribute('right',self.doc.characterAt(cursor.position()))
            
        
        self.parser.addEvent(toProc)
        self.parser.process()
        self.parser.checkState(toProc)

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
