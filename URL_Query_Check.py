import re
class URL_Query_Check:
    def __init__(self,url,query):
        self.url = url
        self.query = query
        self.stopWordList = set()
        self.populateStopWord()

    def populateStopWord(self):
        src = "StopWordsList.txt"
        file = open(src, "r")
        lines = file.readlines()
        for word in lines:
            splt = word.split("\n")
            self.stopWordList.add(splt[0])
        file.close()

    def URLprocesses(self):

        regex = "[^a-zA-Z0-9]"
        urlwordList = re.split(regex,self.url.lower())

        str_split = self.query.split(" ")
        res = ""
        querywordlist =list()
        #form like  Mchine learning ML
        for word in str_split:
            if word not in self.stopWordList:
                res += word[0]
                querywordlist.append(word)
        #print res.lower()
        #print querywordlist
        #print urlwordList
        score = 0
        #add for short form like Mchine learning ML
        if(res in urlwordList):
            score = score | 1
        #check foreach word in query whether present in url
        for word in querywordlist:
            if word in urlwordList:
                score = score | 1
        #print Flag
        return score

'''
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/"
query = "machine learning"
instance = URL_Query_Check(url,query)
instance.URLprocesses()
'''

