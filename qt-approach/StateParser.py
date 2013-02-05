class Parser:
    def __init__(self):
        self.store = ""

    def updateChar(self, char):
        if char in self.delimiters:
            if len(self.store) > 0:
                self.emit()
        else:
            self.store += char

    def emit(self):
        value = self.store
        self.store = ""
        if len(value) > 0: 
            print value
        return value

    def terminate(self):
        self.emit()

class LinearParser(Parser):
    delimiters = ["", " ", "\t", "\n"]

class LRParser(Parser):
    delimiters = []

class LRSParser(LRParser):
    pass

class LRMParser(LRParser):
    pass

class LREParser(LRParser):
    pass

class StateParser:
    def __init__(self):
        self.position = None
        self.parser   = None


    def updateParser(self, cursor, char, position, key_event):
        if self.position is None:
            self.position = position
        else:
            pass
        
        left, right = cursor
        back  = left[0] if len(left) > 0 else None
        front = right[0] if len(right) > 0 else None

        nonAlphabet = [None, "", " ", "\n", "\t"]
        alphablet   = map(lambda x: chr(x), range(33,126))

        # linear parser
        leftP, rightP = ((lambda x: back in x)(nonAlphabet), (lambda x: front in x)(nonAlphabet))
        nextParser = None
        if leftP and rightP:
            nextParser = LinearParser()


        # lr parsers
        if char is None:
            if back in alphablet and front in alphablet:
                nextParser = LRMParser()
            if back in nonAlphabet and front in alphablet:
                nextParser = LRSParser()
            if back in alphablet and front in nonAlphabet:
                nextParser = LREParser()
        

        if nextParser is None:
            if char is not None and self.parser is not None:
                self.parser.updateChar(char)
        else:
            #print "PARSER {}".format(nextParser.__class__)
            if self.parser is not None:
                self.parser.terminate()
            self.parser = nextParser
            if char is not None:
                self.parser.updateChar(char)


    def notify(self, key_event):
        e_object = key_event.GetEventObject()
        cursor_position = e_object.GetInsertionPoint()
        cursor = (e_object.GetRange(cursor_position - 1, cursor_position), e_object.GetRange(cursor_position, cursor_position + 1))
        char = chr(key_event.GetRawKeyCode()) if key_event.GetRawKeyCode() in range(256) else None
        self.updateParser(cursor, char, cursor_position, key_event)
        key_event.Skip()
