import json


def loadURL(filepath) :
    URL = set()
    with open("D:/UCI/CS221_IR/HW3/IR_projecct3/WEBPAGES_RAW/bookkeeping.json") as file:
        DocUrl = json.load(file)
    UrlDoc = {}
    for entry in DocUrl:
        UrlDoc[DocUrl[entry]] = entry
    with open(filepath) as Inputstream:
        for line in Inputstream :
            url = line.split("\n")[0]
            if url in UrlDoc:
                URL.add(url)
    print URL

    print len(URL)
    return URL
loadURL("google_original.txt")
