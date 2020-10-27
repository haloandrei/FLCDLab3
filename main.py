import re


class HashTable(object):
    def __init__(self, length = 17):
        self.array = [None for i in range(0,length)]
        self.fill = 0

    def hash(self, key):
        sumString = 0
        for i in key:
            sumString += ord(i)
        return sumString % len(self.array)

    def add(self, symbol):
        self.fill += 1
        if self.fill > len(self.array):
            self.double()
        index = self.hash(symbol)
        if self.array[index] is not None:
            for val in self.array[index]:
                if (val == symbol):
                    break
                else:
                    self.array[index].append(symbol)
        else:
            self.array[index] = []
            self.array[index].append(symbol)

    def get(self, symbol):
        index = self.hash(symbol)
        if self.array[index] is None:
            return None
        else:
            for val in self.array[index]:
                if (val == symbol):
                    return symbol
            return None

    def double(self):
        print("hashTable expanded")
        newHtb = HashTable(len(self.array) * 2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue
            for val in self.array[i]:
                newHtb.add(val)
        self.array = newHtb.array

class OaiScanner(object):
    def __init__(self, file, token):
        self.tokenFile = token
        self.programFile = file
        self.specTokens = []
        self.PIF = []
        self.ST = HashTable(3)
        self.getTokens()
        self.word = ""
        self.stringFlag = False
        self.operatorFlag = False
        self.specialChrFlag = False


    def getTokens(self):
        file = open(self.tokenFile, "r")

        while( True):
            line = file.readline()
            if not line:
                break
            tokeni = line.split()
            tokenCode = int(tokeni[0])
            tokenString = tokeni[1]
            self.specTokens.append([tokenCode, tokenString])
        file.close()
        #print(self.specTokens)

    def detectFurtherOperators(self,op,newch):
        operatorNew = op + newch
        for i in self.specTokens:
            if i[1].find(operatorNew) != -1:
                return True
        return False
    #
    # def splitOnTokens(self):
    #     file = open(self.programFile, "r")
    #     while (True):
    #         line = file.readline()
    #         if not line:
    #             break
    #         for i in self.specTokens:
    #             prings = "\"(" + i[1] + ")\""
    #             mapTokens = {}
    #             words = {}
    #
    #         print(line)

    def checkLetter(self, i):
        if i in [" ", ";", "\n"] and self.stringFlag!=True:
            self.procesIndex(self.word)
            self.operatorFlag = False
            self.procesIndex(i)
            return
        if self.operatorFlag:
            if self.detectFurtherOperators(self.word, i):
                self.word += i
                return
            else:
                self.procesIndex(self.word)
                self.operatorFlag = False
                self.checkLetter(i)
                return
        if i in ["?", "<", ">", "~", ".","(",")","{","}",":","+","-","/","*","#"]:
            self.procesIndex(self.word)
            self.operatorFlag = True
            self.word += i
            return
        if i=="\"" and self.stringFlag!=True:
            self.stringFlag = True
            self.procesIndex(self.word)
            self.word = i
            return
        if self.stringFlag:
            if self.specialChrFlag:
                self.word += i
                self.specialChrFlag = False
                return
            else:
                if i == "\\":
                    self.specialChrFlag = True
                    return
                else:
                    if i == "\"":
                        self.word += i
                        self.procesIndex(self.word)
                        self.stringFlag = False
                        return
                    else:
                        self.word += i
                        return
        self.word += i
        return
    def splitProgram(self):
        file = open(self.programFile, "r")

        while (True):
            line = file.readline()
            if not line:
                break

            for i in line:
                self.checkLetter(i)

        file.close()
    def isConst(self, word):
        if word[0] in ["0","1","2","3","4","5","6","7","8","9", "\""]:
            return True
        return False

    def procesIndex(self, word):
        #check for .. as error
        self.word = ""
        if word == "" or word == "\n" or word == " ":
            return
        for i in self.specTokens:
            if i[1]==word:
                self.PIF.append([word, -1])
                return
        if self.isConst(word):
            self.PIF.append(["const", self.ST.fill+1])
        else: self.PIF.append(["id", self.ST.fill+1])
        self.ST.add(word)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sc = OaiScanner("C:\\work\\Coding\\Python\\FLCDLab3Scanner\\p2.oai","C:\\work\\Coding\\Python\\FLCDLab3Scanner\\token.in")
    sc.splitProgram()
    for i in sc.PIF:
        print(i)
