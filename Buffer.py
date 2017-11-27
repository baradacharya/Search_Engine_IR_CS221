import json

class Buffer:
    def __init__(self):
        self.buffer = {}
        self.doc_length_map = {}

    def dump(self):
        file = open("index.txt", 'w+')
        json.dump(self.buffer, file)
        file.close()

        file = open("tokenCount.txt", 'w+')
        file.write(str(len(self.buffer)))
        file.close()
        self.buffer.clear()
        print 'buffer cleared'

        file = open("document_length.txt", 'w+')
        json.dump(self.doc_length_map, file)
        file.close()
        print 'all files are dumped'
        self.doc_length_map.clear()
        print 'doc_length_map cleared'


    def writeInBuffer(self,entry,posting):

        if entry in self.buffer:
            self.buffer[entry].append((posting.docID,posting.list,posting.score))
        else:
            self.buffer[entry] = list()
            self.buffer[entry].append((posting.docID,posting.list,posting.score))
