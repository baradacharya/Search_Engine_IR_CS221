import json
import math
class Memory:
    def __init__(self):
        self.buffer = {}
        self.total_Document_number = 0
        self.tf_idf = {}

    def printBuffer(self):
        for k in self.buffer:
            print k,self.buffer[k]

    def dump(self):
        self.file = open("index.txt", 'w+')
        json.dump(self.buffer, self.file)
        self.file.close()
        print "No of unique Word : " + str(len(self.buffer))
    def Score_tf_idf(self):
        print "total_doc : " + str(self.total_Document_number)
        for entry in self.buffer:

            idf = len(self.buffer[entry])
            #print entry,idf
            temp = {}
            for posting in self.buffer[entry]:
                tf = len(posting[1])
                tf_idf_score = math.log10(1 + tf) * math.log10(float(self.total_Document_number)/idf)
                #print entry,posting[0],tf,self.total_Document_number,idf,tf_idf_score
                temp[posting[0]] = round(tf_idf_score, 4 )
            self.tf_idf[entry] = temp
    def writeInBuffer(self,entry,posting):
        if entry in self.buffer:
            self.buffer[entry].append((posting.docID,posting.list))
        else:
            self.buffer[entry] = list()
            self.buffer[entry].append((posting.docID,posting.list))
    def dumpScore(self):
        file = open("TF_IDF.txt", 'w+')
        json.dump(self.tf_idf, file)
        file.close()

