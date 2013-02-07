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
    parser = None

    def updateParser(self, cursor, char):
        nextParser       = None
        left, right      = cursor
        isNonAlfanumeric = lambda x: x in [None, "", " ", "\n", "\t"]
        # TODO again, make the darn thing unicode aware
        isAlfanumeric = lambda x: x in map(lambda x: chr(x), range(33,126))

        # linear parser
        if isNonAlfanumeric(left) and isNonAlfanumeric(right):
            nextParser = LinearParser()

        # lr parsers
        if char is None:
            if isAlfanumeric(left) and isAlfanumeric(right):
                nextParser = LRMParser()
            if isNonAlfanumeric(left) and isAlfanumeric(right):
                nextParser = LRSParser()
            if isAlfanumeric(left) and isNonAlfanumeric(right):
                nextParser = LREParser()
        

        if nextParser is None:
            if char is not None and self.parser is not None:
                self.parser.updateChar(char)
        else:
            print "PARSER {}".format(nextParser.__class__)
            if self.parser is not None:
                self.parser.terminate()
            self.parser = nextParser
            if char is not None:
                self.parser.updateChar(char)
