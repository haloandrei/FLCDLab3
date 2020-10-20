
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
        for i in self.tokenFile:
            if i[1].find(operatorNew):
                return True
        return False

    def splitProgram(self):
        file = open(self.programFile, "r")

        while (True):
            line = file.readline()
            if not line:
                break
            word = ""
            stringFlag = False
            operatorFlag = False

            specialChrFlag = False
            for i in line:
                if i in [" ", ";"]:
                    self.procesIndex(word)
                if i in ["?","<",">",":","."]:
                    operatorFlag = True
                    self.procesIndex(word)
                    word = i
                if operatorFlag:
                    if self.detectFurtherOperators(word,i):
                        word += i
                    else:
                        self.procesIndex(word)
                        word = i


                if stringFlag:
                    if specialChrFlag:
                        word += i
                    else:
                        if i == "\\":
                            specialChrFlag = True
                        else:
                            if i == "\"":
                                word += i
                                self. procesIndex(word)



                    word+= i

        file.close()

    def procesIndex(self, word):
        for i in self.tokenFile:
            if word in i:
                print("reserved")
                return
        print(word + "identif or const")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sc = OaiScanner("C:\\work\\Coding\\Python\\FLCDLab3Scanner\\p1.oai","C:\\work\\Coding\\Python\\FLCDLab3Scanner\\token.in")
    sc.procesIndex("~")
