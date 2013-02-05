#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import StateParser

WordDelimiters = {0x020,0x01000001}
LineDelimiters = {0x01000004}

CursorMoveKeys = {0x01000012,0x01000013,0x01000014,0x01000015}

class SmartTextbox(QtGui.QTextEdit):
    parser = StateParser.StateParser()

    def keyPressEvent(self, event):
        QtGui.QTextEdit.keyPressEvent(self, event)
        cposition = self.textCursor().position()
        character = None if event.key() in CursorMoveKeys else event.text()
        # TODO make this unicode aware
        def characterAtOrNone(position):
            character = self.document().characterAt(position)
            print character
            print character.isMark()
            # TODO find out what that \x00 character is, and why it's harrasing me
            return None if (character.isNull() or character is u'\x00') else character.toAscii()

        '''
        For the cursor's left character the ternary is in place because we receive the
        event after the key is inputed. As such we need the pre insertion cursors left
        and right values.
        '''
        cursor = (characterAtOrNone(cposition - 1 if character is None else cposition - 2),
                  characterAtOrNone(cposition))
        

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

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())

