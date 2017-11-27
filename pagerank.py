import os
import lxml
from lxml import html
import json
import pickle
from urlparse import urljoin, urlparse

class PageRank:

    def __init__(self):
        self.blockedList = ['script']
        self.DocUrl = {}
        self.UrlDoc = {}
        self.outAdjacencyList = {}
        self.inAdjacencyList = {}
        self.PageRank = {}
        self.max_pagerank = 0
        self.min_pagerank = 100000
        self.anchortext = {}
        self.stopWordList = set()
        self.populateStopWord()


    def makeAdjacencyList(self):
        src = "D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW"

        folder = os.listdir(src)

        for directory in folder:
            currDir = src + "/" + directory
            if not os.path.isdir(currDir):
                continue
            files = os.listdir(currDir)

            for file in files:
                # print file
                currFile = currDir + "/" + file
                url = self.DocUrl[directory + "/" + file]
                # skip for directory
                if not os.path.isfile(currFile):
                    continue
                input = open(currFile, "r")
                data = input.read()
                try:
                    elements = lxml.html.fromstring(data);
                except:
                    print "Invalid File"
                    continue
                # line will store token of full document
                lines = list()

                for element in elements.xpath("//a"):
                    dict = element.attrib
                    if dict.has_key("href") == False:
                        continue
                    url1 = "http://" + url
                    out_url  = urljoin(url1,dict["href"])
                    out_url = out_url[7:]
                    docIDIN = self.UrlDoc[url]
                    if out_url in self.UrlDoc:
                        docIDOUT = self.UrlDoc[out_url]
                        #add anchor text in output url
                        if element.text != None and self.stopWord(element.text.lower())== False:
                            if docIDOUT in self.anchortext:
                                self.anchortext[docIDOUT].add(element.text)
                            else:
                                self.anchortext[docIDOUT] = set()
                                self.anchortext[docIDOUT].add(element.text)
                         #insert entry in both in and out adjancency list
                        self.insertAdjacencyListOut(docIDIN,docIDOUT)
                        self.insertAdjacencyListIn(docIDOUT,docIDIN)

                print "File done...",file
            print "Directory done...",directory
    def reverseMap(self):
        src = "D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW/bookkeeping.json"
        with open(src) as file:
            self.DocUrl = json.load(file)

        self.UrlDoc = {}
        print "Loading...."
        for entry in self.DocUrl:
            self.UrlDoc[self.DocUrl[entry]] = entry
        file2 = open("ReverseMapofDocs.json","a")
        json.dump(self.UrlDoc,file2)
        print "Done!!"

    def populateStopWord(self):
        src = "D:/UCI/CS221_IR/HW3/IR_projecct3/Part2_search/anchor_stopword.txt"
        file = open(src, "r")
        lines = file.readlines()
        for word in lines:
            splt = word.split("\n")
            self.stopWordList.add(splt[0].lower().strip())
        print self.stopWordList
        file.close()
    def stopWord(self,word):
        if word.strip() in self.stopWordList:
            return True
        return False
    def insertAdjacencyListOut(self, IN, OUT):

        if IN not in self.outAdjacencyList:
            self.outAdjacencyList[IN] = set()
        self.outAdjacencyList[IN].add(OUT)

    def insertAdjacencyListIn(self, OUT, IN):

        if OUT not in self.inAdjacencyList:
            self.inAdjacencyList[OUT] = set()
        self.inAdjacencyList[OUT].add(IN)

    def calculatePageRank(self,d = 0.85):
        for doc in self.DocUrl:
            self.PageRank[doc] = 1

        for i in range(0,5):
            for docOut in self.DocUrl:
                sum = 0
                self.PageRank[docOut] = (1 - d)
                if docOut in self.inAdjacencyList:
                    for docIn in self.inAdjacencyList[docOut]:
                        sum += float(self.PageRank[docIn]*1.0) / float(len(self.outAdjacencyList[docIn])*1.0)
                self.PageRank[docOut] +=  d * sum
                temp =  round(self.PageRank[docOut],4)
                self.PageRank[docOut] = temp

                if temp >  self.max_pagerank:
                    self.max_pagerank = temp
                if temp <  self.min_pagerank:
                    self.min_pagerank = temp
        self.dumpPageRank()
    def dumpPageRank(self):
        file = open("PageRank.txt", 'w+')
        json.dump(self.PageRank, file)
        file.close()

        with open("pagerank_max_min.txt", "w") as outputstream:
            outputstream.write(str(self.max_pagerank) + "," + str(self.min_pagerank))
        outputstream.close()
        #print self.anchortext

        #priting some high frequecy word in anchor text for stopword
        highfreqword ={}
        for doc in self.anchortext:
            for word in self.anchortext[doc]:
                if word in highfreqword:
                    highfreqword[word] += 1
                else:
                    highfreqword[word] = 1
        highfreqword = sorted(highfreqword, key=lambda key: highfreqword[key], reverse=True)
        print highfreqword[:100]
        output = open('anchor.pkl', 'wb')
        pickle.dump(self.anchortext, output, -1)
        output.close()
        #json.dump(self.anchortext, file)





#os.remove("ReverseMapofDocs.txt")
#os.remove("PageRank.txt")
pageRank = PageRank()
pageRank.reverseMap()
pageRank.makeAdjacencyList()
pageRank.calculatePageRank()
