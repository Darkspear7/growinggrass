# Smarty the startbox i guess

from utils import *
from math import *

Entities = {0:'unknown', 1:'word', 2:'sentence', 3:'paragraf'}
Hiearchy = {'paragraf':[2, 1],
            'sentence':[1]}

class Entity:
    def __init__(self, delimiters):
        self.delimiters = delimiters
    def getDelimiters(self):
        return self.delimiters

NonCharacters = {'\x00','\2029'}
Word  = Entity([' ','\t','\r','\x00','\u2029','\x0003','\n'])
Sentence = Entity(['\r','\x00','\u2029','\x0003','\n'])

class NavigationModule:
    def __init__(self,stringBuffer, pos = 0):
        self.sbuffer = stringBuffer
        self.position = pos
        self.location = 0
    def move(self, direction, char = None):
        if direction == 'left':
            if not self.sbuffer.getCharAt(self.position - 1) in NonCharacters:
                self.position -= 1
        elif direction == 'right':
            if not char == None:
                self.position += 1
            elif not self.sbuffer.getCharAt(self.position + 1) in NonCharacters:
                self.position += 1
        self.checkLocation(char)
    def moveAt(self, position):
        pass
    def getPosition(self):
        return self.position
    def getLocation(self):
        return self.location
    def checkLocation(self, char = None):
        if char == None:
            if self.location == 0:
                tmp = map(lambda x: self.sbuffer.findCharForward(x,self.position), Word.getDelimiters())
                f = min([x for x in tmp if not x == None])
                tmp = map(lambda x: self.sbuffer.findCharBackward(x,self.position), Word.getDelimiters()) 
                b = max([x for x in tmp if not x == None])
                print(self.sbuffer.getSubstring(b + 1, f - b - 1))
                self.location = 1

               
