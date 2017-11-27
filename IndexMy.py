import os
import lxml
from Buffer import Buffer
from Tokenizer import Tokenizer
from lxml import html
from TF_IDF import Score
import pickle
class PostingObj:
    def __init__(self, doc, list,score):
        self.docID = doc
        self.list = list
        self.score = score

def LoadanchorText(filepath):
    anchortext = {}
    pkl_file = open('anchor.pkl', 'rb')
    anchortext = pickle.load(pkl_file)
    return anchortext

tagDict = {"title":150,"h1":20,"h2":20,"h3":20,"h4":20,"h5":20,"h6":20,"h7":20,"strong":5,"b":3,"i":3,"u":3}


src = "D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW"

folder = os.listdir(src)
buffer = Buffer()
totalDocs = 0
tokenizer = Tokenizer()
blockedList = ['script']
anchorpath = "anchor.txt"
anchortext = LoadanchorText(anchorpath)
for directory in folder:
    currDir = src + "/" + directory
    if not os.path.isdir(currDir):
        continue
    files = os.listdir(currDir)
    lines = list()
    for file in files:
        # print file
        currFile = currDir + "/" + file
        #skip for directory
        if not os.path.isfile(currFile):
            continue
        input = open(currFile, "r")
        data = input.read()
        try:
            elements = lxml.html.fromstring(data);
        except:
            print "Invalid File"
            continue
        #line will store token of full document
        lines = list()
        for ele in elements.xpath("//*"):
            #except for the blocked lit parse others
            if ele.tag in blockedList:
                continue
            elementText = str()
            #handle invalid coding
            try:
                elementText = str(ele.text)
            except UnicodeEncodeError:
                elementText = ele.text.encode('utf-8')
            elementText = elementText.strip()

            if elementText == "None" or elementText == "":
                continue

            lines.append(elementText)

        # input.close()
        print "File done...", file
        totalDocs += 1
        #pass the entire document for tokenization dict[word] = offset position in document
        map = tokenizer.getWordMap(lines)
        '''
        Created a score map using tags in the the tagdict at the end of this for loop we get a dict that contains final
        score corresponding to the word for this document.
        '''
        scoreMap = {}
        for word in map:
            scoreMap[word] = len(map[word])

        # parsing it for different important tags
        for tag in tagDict:
            for ele in elements.xpath("//" + tag):
                elementText = str()
                try:
                    elementText = str(ele.text_content())
                except UnicodeEncodeError:
                    elementText = ele.text_content().encode('utf-8')
                if elementText == "None" or elementText == "":
                    continue
                scoreMap = tokenizer.tagWiseScore(tagDict[tag],elementText,scoreMap)

        #parse for anchor text add coresponding score to word-docuent score
        anchor_score = 100
        docname = directory + '/' + file
        if docname in anchortext:
            for list1 in anchortext[docname]:
                scoreMap = tokenizer.anchorScore(anchor_score, list1, scoreMap)


        for entry in map:
            #store as word : postingobj , where postingobj : docname, dict[word],tf_idf
            buffer.writeInBuffer(entry, PostingObj(docname, map[entry],scoreMap[entry]))
            buffer.doc_length_map[docname] = tokenizer.doc_length

    print "Folder done...", directory



#buffer.printBuffer()
'''
os.remove("index.txt")
os.remove("TF_IDF.txt")
os.remove("tokenCount.txt")
os.remove("document_length.txt")
'''
score = Score()
score.createTFIDF(totalDocs,buffer.buffer)
buffer.dump()



print("finished")

