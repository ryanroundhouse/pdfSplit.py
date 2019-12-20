import re

def displayHelp():
    print("usage: py pdfSplit.py /?")
    print("   To display cli instructions.")
    print("usage: py pdfSplit.py <path to folder> <path to archive folder> <path to output> <string to be present on first page of bill>")
    print("   To split a big PDF fill file as close to half based off of a string that should be unique to the first page of each bill.")
    print("   <path to folder> is a path to a folder that contains the PDF files to split.")
    print("   <path to archive folder> is the folder where PDF files that are split will be moved to.")
    print("   <path to output> is a path to a folder where split PDF files will be created.")
    print("   <string to be present on first page of bill> is a string value that will be used to identify the first page of any bill.  This text must exist on all bills and only on the first page of each.")
    print("usage: py pdfSplit.py /d <path to pdf> <page number>")
    print("   To display the contents of a specific page number of each bill in the folder.  This can be useful to figure out the <string to be present on first page of bill>")
    print("   <path to pdf> is a path to the PDF to display")
    print("   <page number> is the page number of each PDF to display")

def findBillBreaks(pdfReader, sizePerChunk, searchString):
    """ Returns an array of all pages upon which you should break the PDF so that it doesn't split any bills. """
    if (sizePerChunk <= 0):
        raise Exception("You must specify a chunk size of 1 page or more.")
    chunkList = []
    numPages = pdfReader.getNumPages()
    nextPageToChunkOn = sizePerChunk

    while True:
        if nextPageToChunkOn >= numPages:
            break
        else:
            nextPageToChunkOn = findNextPageWithSearchString(pdfReader, searchString, nextPageToChunkOn, numPages + 1)
            chunkList.append(nextPageToChunkOn)
            nextPageToChunkOn += sizePerChunk
    return chunkList

def findNextPageWithSearchString(pdfReader, searchString, pageNum, numPages):
    """ Find the next page after the specified page that contains the searchString. """
    while True:
        if doesPageContainSearchString(pdfReader, searchString, pageNum):
            break
        else:
            pageNum += 1
        if pageNum >= numPages:
            break
    return pageNum

def doesPageContainSearchString(pdfReader, searchString, pageNum):
    """ Returns true if the specified page contains the searchString. """
    page_text = getContentsOfPageFromPDF(pdfReader, pageNum)
    return re.match(r".*" + searchString + ".*", page_text)

def getContentsOfPageFromPDF(pdfReader, pageNum):
    """ Returns the content of a specific page in a PDF. """
    pageObj = pdfReader.getPage(pageNum)
    return re.sub("\n", "", pageObj.extractText())