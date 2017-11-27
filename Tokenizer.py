import re
from nltk.stem.porter import *

class Tokenizer:
    def __init__(self):
        self.stopWordList = set()
        self.doc_length = 0
        #self.populateStopWord()

    '''
    def populateStopWord(self):
        src = "/Users/adityajoshi/UCI/Quarter 2/IR/StopWordsList.txt"
        file = open(src,"r")
        lines = file.readlines()
        for word in lines:
            splt = word.split("\n")
            self.stopWordList.add(splt[0])
        file.close()
    '''
    def stopWord(self,word):
        if word in self.stopWordList:
            return True
        return False

    def getWordMap(self,lines):
        pos = 1
        wordMap = {}
        stemmer = PorterStemmer()
        for line in lines:
            regex = "[^a-zA-Z0-9]"
            wordList = re.split(regex,line.lower())

            for word in wordList:
                #skip for blank word
                if word == "":
                    continue
                #skip for stop word
                '''if self.stopWord(word):
                    continue'''
                key = str()
                self.doc_length += 1
                try:
                    key = stemmer.stem(word)
                except IndexError:
                    key = word

                if key in wordMap:
                    wordMap[key].append(pos)
                else:
                    wordMap[key] = list()
                    wordMap[key].append(pos)
                pos += 1
        return wordMap

    def tagWiseScore(self,tag,elementText,scoreMap):
        regex = "[^a-zA-Z0-9]"
        wordList = re.split(regex, elementText.lower())
        stemmer = PorterStemmer()

        for word in wordList:
            if word == "":
                continue
            if self.stopWord(word):
                continue
            key = str()
            try:
                key = stemmer.stem(word)
            except IndexError:
                key = word

            if key in scoreMap:
                scoreMap[key] += tag
            else:
                scoreMap[key] = tag

        return scoreMap

    def anchorScore(self,score,elementText,scoreMap):
        regex = "[^a-zA-Z0-9]"
        #print elementText
        wordList = re.split(regex, elementText.lower())
        stemmer = PorterStemmer()

        for word in wordList:
            if word == "":
                continue
            if self.stopWord(word):
                continue
            key = str()
            try:
                key = stemmer.stem(word)
            except IndexError:
                key = word

            if key in scoreMap:
                scoreMap[key] += score
            else:
                scoreMap[key] = score

        return scoreMap






