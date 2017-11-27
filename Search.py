import re
import json
import lxml
from lxml import html
from URL_Query_Check  import URL_Query_Check
from nltk.stem.porter import *

class Search:
    def __init__(self,tf_Idffile,doc_len_file,pagerankfile):
        self.query = ""
        self.DocUrl = {}
        self.cos_result = []
        self.tf_idf_scores = {}
        self.url_scores = {}
        print ("doc-url loading")
        with open("D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW/bookkeeping.json") as file:
            self.DocUrl = json.load(file)

        print ("tf-idf loading .....")
        with open(tf_Idffile) as file:
            self.tf_idf = json.load(file)
        file.close()
        print ("tf-idf loaded")
        print ("pagerank loading .....")
        with open(pagerankfile) as file:
            self.pagerank = json.load(file)
        file.close()
        print ("pagerank loaded .....")
        with open(doc_len_file) as file:
            self.doc_len_map = json.load(file)
        file.close()

        with open("TF_IDF_max_min.txt", "r") as Inputstream:
            for line in Inputstream:
                    str_split = line.split(",")
                    self.max_tf_idf = float(str_split[0])
                    self.min_tf_idf = float(str_split[1])
        with open("pagerank_max_min.txt", "r") as Inputstream:
            for line in Inputstream:
                    str_split = line.split(",")
                    self.max_pagerank = float(str_split[0])
                    self.min_pagerank = float(str_split[1])
        print ("all files loaded")

        self.src = "D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW/"

    def inputQuery(self):
        self.query = raw_input("Query enter kar: ")
        if self.query == "quit":
            return 0
        self.query = self.query.lower()
        return 1

    def search(self,top = 20,tfidf_param =1.2, pagerank_para =0.7, urlpara = 0.075):
        stemmer = PorterStemmer()
        regex = "[^a-zA-Z0-9]"
        wordList = re.split(regex,self.query)
        scores = {}
        cos_score = {}
        for word in wordList:
            if word == "":
                continue
            '''if self.stopWord(word):
                continue'''
            key = str()
            try:
                key = stemmer.stem(word)
            except IndexError:
                key = word
            docs = self.tf_idf[key]
            for docID in docs:
                if docID not in scores:
                    scores[docID] = 0
                    cos_score[docID] = 0
                #cal normalization doc score
                normalize_doc_score = float(docs[docID])/self.doc_len_map[docID]
                cos_score[docID] += normalize_doc_score
                #adding normalization to shift into 0-1 range both scoores
                tf_idf_score = float((docs[docID]- self.min_tf_idf))/(self.max_tf_idf-self.min_tf_idf)
                self.tf_idf_scores[docID] = round(tf_idf_score,4)
                pagerank_score = float((self.pagerank[docID]-self.min_pagerank))/(self.max_pagerank-self.min_pagerank)
                scores[docID] += tfidf_param * tf_idf_score + pagerank_para * pagerank_score

                self.url_scores[docID] = 0
                #add some weightage to url
                if  docID in self.DocUrl:
                    url= self.DocUrl[docID]
                    instance = URL_Query_Check(url, self.query)
                    #if(instance.URLprocesses() == 1):
                    url_score = instance.URLprocesses()
                    scores[docID] += urlpara * url_score
                    self.url_scores[docID] = urlpara * url_score


        sorted_scores = sorted(scores, key=lambda key: scores[key],reverse=True)
        cosine_scores = sorted(cos_score, key=lambda key: cos_score[key], reverse=True)
        result = []
        result_url_set = set()
        i = 0
        #use set
        for docID in sorted_scores:
            if docID in self.DocUrl:
                if self.DocUrl[docID] not in result_url_set:
                    result_url_set.add(self.DocUrl[docID])
                    result.append(docID)
                    print docID,self.DocUrl[docID],self.tf_idf_scores[docID],self.pagerank[docID], self.url_scores[docID],scores[docID]
                    i+=1
                    if i == top:
                        break
                    #print result
        #return result
        #print ("cosine similarity results")
        i = 0
        for docID in cosine_scores:
            self.cos_result.append(docID)
            i += 1
            if i == top:
                break
        #print self.cos_result
        return result

    def getSnippet(self,elements,maxLength = 2):
        pageData = elements.text_content()
        sentences = re.split("[\n\\.\\t]",pageData)
        tokens = re.split(" ",self.query)
        result = ""
        length = 0
        for sen in sentences:
            sen.strip()
            if sen == "":
                continue
            for token in tokens:
                token.strip()
                if token == "":
                    continue
                if token in sen.lower():
                    result = result + sen + "..."
                    length += 1
                    break
            if length == maxLength:
                result.strip()
                print result
                return result
        result.strip()
        print result
        return result


    def retrieveDocuments(self,result):
        '''
        with open("D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW/bookkeeping.json") as file:
            data = json.load(file)
        '''
        for docID in result:

            #print self.DocUrl[docID]
            file = open(self.src + docID,'r')
            PageData = file.read()
            try:
                elements = lxml.html.fromstring(PageData);
            except:
                print "Invalid File"
                continue
            ele = elements.xpath("//title")
            if not ele:
                print "Not a HTML file"
            else:
                #print ele[0].text_content()
                #self.getSnippet(elements,3)
                print "\n"
            '''
            print ("cosine results")
            for docID in self.cos_result:

                print data[docID]

                file = open(self.src + docID, 'r')
                PageData = file.read()
                try:
                    elements = lxml.html.fromstring(PageData);
                except:
                    print "Invalid File"
                    continue
                ele = elements.xpath("//title")
                if not ele:
                    print "Nai milra re title"
                else:
                    print ele[0].text_content()
                    #self.getSnippet(elements, 3)
                    print "\n"
            '''

search = Search("TF_IDF.txt","document_length.txt","PageRank.txt")
while(1):
    ans = search.inputQuery()
    if(ans == 0):
        break
    search.retrieveDocuments(search.search())
