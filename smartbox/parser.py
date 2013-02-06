# Parser class

from utils import *

NonCharacters = {'\0','\x00','\x0003','\u2029'}
WordDelimiters = {' ','\t'}
LineDelimiters = {'\n','\r'}

def isCharWordDelimiter(char):
    return char in WordDelimiters
def isCharLineDelimiter(char):
    return char in LineDelimiters
def isCharNotDelimiter(char):
    return (not isCharWordDelimiter(char)) and (not isCharLineDelimiter(char)) and (not char in NonCharacters)

ParserStates = {'linear','lrs','lrm','lre'}
# the boolean values answer to the questions:
# is left character printable ?
# is right character printable ?
StateCriteria = {(False,False):'linear',
                 (False,True):'lrs',
                 (True,True):'lrm',
                 (True,False):'lre'}

LinearCriteria = [['kc','kdw'],['kc','kdl'],['kc','cm']]
LRCriteria = [['kc','cm']]
LRSCriteria = [['kc','kdw'],['kc','kdl']]
LRMCriteria = [['kdw'],['kdl'],['kc','kdw'],['kc','kdl']]
LRECriteria = [['kc','kdw'],['kc','kdl']]

class Parser:
    def __init__(self):
        self.state = 'linear'
        self.actions = []
    def addEvent(self, event):
        if self.__validateEvent(event):
            # add the event in the list of actions
            left = event.getAttribute('left')
            right = event.getAttribute('right')
            if event.isKeyEvent():
                char = event.getAttribute('char')
                if isCharWordDelimiter(char):  eType = 'kdw' 
                elif isCharLineDelimiter(char): eType = 'kdl'
                else: eType = 'kc'
                toAdd = {'type':eType,'left':left,'right':right,'char':char}
                self.__addEvent(toAdd)
            elif event.isCursorEvent():
                direction = event.getAttribute('dir')
                toAdd = {'type':'cm','left':left,'right':right,'dir':direction}
                self.__addEvent(toAdd)
            else:
                raise Exception("Something went wrong")
        else:
            raise Exception("Only instances of Event can be added")
    def process(self, text, cursorPos):
        # check the actions list
        # if the first event in the actions list is a navigational one
        if self.actions[0]['type'] == 'cm':
            #check state and remove the event
            self.__checkState()
            self.actions = []
        # else if the event is a printable one
        else:
           #check to see if it falls in one of the criterions for emiting for the current state
            #if emitting occured check state and clear the actions list
            events = [x['type'] for x in self.actions]
            emited = False
            if self.state == 'linear': emited  = self.__useLinear(events, text, cursorPos)
            elif self.state == 'lrs': emited  = self.__useLRS(events, text, cursorPos)
            elif self.state == 'lrm': emited  = self.__useLRM(events, text, cursorPos)
            elif self.state == 'lre': emited  = self.__useLRE(events, text, cursorPos)
            if emited:
                    self.__checkState()
                    self.actions = []                
    def __checkState(self):
        # take the left and right characters from the last event
        isLchar = isCharNotDelimiter(self.actions[-1]['left'])
        isRchar = isCharNotDelimiter(self.actions[-1]['right'])
        # check the state criterion statisfied and switch to that
        self.state = StateCriteria[(isLchar,isRchar)]
    def __validateEvent(self, event):
        if isinstance(event, Event):
            check1 = event.hasAttribute('left') and event.hasAttribute('right')
            check2 = event.hasAttribute('char')
            check3 = event.hasAttribute('dir')
            if event.isKeyEvent():
                return check1 and check2
            elif event.isCursorEvent():
                return check1 and check3
            else:
                raise Exception("something went wrong")
        else:
            return False
    def __addEvent(self, event):
        if len(self.actions) > 0:
            if not event['type'] == self.actions[-1]['type']:
                self.actions.append(event)
        else:
            self.actions.append(event)
    def __useLinear(self, events, text, cursorPos):
        if events in LinearCriteria:
            if events[-1] == 'cm':
                if self.actions[-1]['dir'] == 'r': loffset, roffset = 2, 1
                if self.actions[-1]['dir'] == 'l': loffset, roffset = 1, 0
                word = self.__readLeft(text, cursorPos - loffset)
                word = word + self.__readRight(text, cursorPos - roffset)                
            else:
                word = self.__readLeft(text, cursorPos -2)
            print('using linear method for emit : '+ word)
            return True
        return False
    def __useLRS(self, events, text, cursorPos):
        if events in LRCriteria:
            loffset = 1
            roffset = 0
            if self.actions[-1]['dir'] == 'r': loffset, roffset = 2, 1
            if self.actions[-1]['dir'] == 'l': loffset, roffset = 0,-1
            word = self.__readLeft(text, cursorPos - loffset)
            word = word + self.__readRight(text, cursorPos - roffset)
            print('using lrs method for change : '+ word)
            return True
        elif events in LRSCriteria:
            word = self.__readLeft(text, CursorPos -2)
            print('using lrs method for emit : '+ word)
            return True
        return False
        print('using lrs method for emit')
    def __useLRM(self, events, text, cursorPos):
        if events in LRCriteria:
            word = self.__readLeft(text, cursorPos - 1)
            word = word + self.__readRight(text, cursorPos)
            print('using lrm method for change : '+ word)
            return True
        elif events in LRMCriteria:
            word1 = self.__readLeft(text, cursorPos - 2)
            word2 = self.__readRight(text, cursorPos)
            print('using lrm method for change, change : '+word1+" : "+word2)
            return True
        return False        
    def __useLRE(self, events, text, cursorPos):
        if events in LRCriteria:
            loffset = 1
            if self.actions[-1]['dir'] == 'r': loffset = 2
            word = self.__readLeft(text, cursorPos - loffset)
            print('using lre method for change : '+word)
            return True
        elif events in LRECriteria:
            word = self.__readLeft(text, cursorPos - 2)
            print('using lre method for change : '+word)
            return True
        return False
    def __readLeft(self,text, pos):
        word = []
        try:
            while isCharNotDelimiter(text[pos]) and pos >= 0:
                word.insert(0,text[pos])
                pos = pos - 1
        except IndexError:
            return "".join(word)
        return "".join(word)
    def __readRight(self,text, pos):
        word = []
        try:
            while isCharNotDelimiter(text[pos]):
                word.append(text[pos])
                pos = pos + 1
        except IndexError:
            return "".join(word)
        return "".join(word)        
