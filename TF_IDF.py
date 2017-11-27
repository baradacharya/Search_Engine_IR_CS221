import json
import math
from Buffer import Buffer
'''
posting(docID, list, score)

'''

class Score:
    def __init__(self):
        self.tf_idf = {}
        self.max_tf_idf = 0
        self.min_tf_idf = 100000

    def createTFIDF(self,totalDocs,data):
        '''
        with open("index.txt") as file:
            data = json.load(file)
        '''
        for wordID in data:
            dft = len(data[wordID])
            idf = math.log(float(totalDocs) / dft)
            temp = {}
            for posting in data[wordID]:
                tf = posting[2] #tf score
                tf_idf_score = round((1 + math.log(tf)) * idf,4)
                temp[posting[0]] = tf_idf_score
                #storig highest lowest value for narmalization
                if tf_idf_score >  self.max_tf_idf:
                    self.max_tf_idf = tf_idf_score
                if tf_idf_score <  self.min_tf_idf:
                    self.min_tf_idf = tf_idf_score
            self.tf_idf[wordID] = temp
        #file.close()
        self.dumpData()

    def dumpData(self):
        file = open("TF_IDF.txt", 'w+')
        json.dump(self.tf_idf, file)
        file.close()
        with open("TF_IDF_max_min.txt", "w") as outputstream:
            outputstream.write(str(self.max_tf_idf) + "," + str(self.min_tf_idf))
        outputstream.close()
