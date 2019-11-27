import PyPDF4
import re
import io
import os
import sys
import shutil

if (len(sys.argv) != 5 and len(sys.argv) != 4) or sys.argv[1] == "/?":
    print("usage: py pdfSplit.py /?")
    print("   To display cli instructions.")
    print("usage: py pdfSplit.py <path to folder> <path to archive folder> <path to output> <string to be present on first page of bill>")
    print("   To split a big PDF fill file as close to half based off of a string that should be unique to the first page of each bill.")
    print("   <path to folder> is a path to a folder that contains the PDF files to split.")
    print("   <path to archive folder> is the folder where PDF files that are split will be moved to.")
    print("   <path to output> is a path to a folder where split PDF files will be created.")
    print("   <string to be present on first page of bill> is a string value that will be used to identify the first page of any bill.  This text must exist on all bills and only on the first page of each.")
    print("usage: py pdfSplit.py /d <path to folder> <page number>")
    print("   To display the contents of a specific page number of each bill in the folder.  This can be useful to figure out the <string to be present on first page of bill>")
    print("   <path to folder> is a path to a folder that contains the PDF files to display")
    print("   <page number> is the page number of each PDF to display")
    sys.exit()

if len(sys.argv) == 4 and sys.argv[1] == "/d":
    inputFolder = sys.argv[2]
    filesInFolder = [f for f in os.listdir(inputFolder) if os.path.isfile(f)]
    pdfFiles = filter(lambda f: f.endswith(('.pdf','.PDF')), filesInFolder)
    for pdfFile in pdfFiles:
        print("Displaying page " + sys.argv[3] + " of file " + pdfFile)
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(int(sys.argv[3]))
            print(re.sub("\n", "", pageObj.extractText()))
    sys.exit()

inputFolder = sys.argv[1]
archiveFolder = sys.argv[2]
outputFolder = sys.argv[3]
searchString = sys.argv[4]

print ("supplied arguments:")
print ("inputFolder: " + inputFolder)
print ("archiveFolder " + archiveFolder)
print ("outputFolder " + outputFolder)
print ("searchString " + searchString)

# Create all folders if they don't exist yet
if os.path.exists(archiveFolder) == False:
    print("archive folder doesn't exist.  Creating...")
    os.mkdir(archiveFolder)
if os.path.exists(outputFolder) == False:
    print("output folder doesn't exist.  Creating...")
    os.mkdir(outputFolder)

# Find all PDF files in the input folder.
filesInFolder = [f for f in os.listdir(inputFolder) if os.path.isfile(f)]
pdfFiles = filter(lambda f: f.endswith(('.pdf','.PDF')), filesInFolder)
print ("Found " + str(len(filesInFolder)) + " PDF files:")

for pdfFile in pdfFiles:
    print("Splitting " + pdfFile)
    with open(pdfFile, 'rb') as pdfFileObj:
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)

        # Find the midpoint to split on without breaking a bill in half.
        numPages = pdfReader.getNumPages()
        print ("found " + str(numPages) + "bills")
        midPage = int(numPages / 2)
        print ("midpoint might be " + str(midPage))

        while True:
            pageObj = pdfReader.getPage(midPage)
            pages_text = re.sub("\n", "", pageObj.extractText())
            if re.match(r".*" + searchString + ".*", pages_text):
                print ("true midpoint found at " + str(midPage))
                break
            else:
                midPage = midPage + 1
                if midPage + 1 > numPages:
                    sys.exit("ERROR: string to split pages on not found in the last half of the document.  Please supply a different string and try again.")

        # Write first half into part 1.
        print("building up part 1...")
        pdfPart1Writer = PyPDF4.PdfFileWriter()
        for pageNumber in range(0, midPage):
            pdfPart1Writer.addPage(pdfReader.getPage(pageNumber))

        fullPathToFile1 = os.path.join(outputFolder, pdfFile.split('.')[0] + "_1.pdf")
        print ("Writing part 1 to " + fullPathToFile1)
        with open(fullPathToFile1, "wb") as outputFile:
            pdfPart1Writer.write(outputFile)

        # Write second half into part 2.
        print("building up part 2...")
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
        pdfPart2Writer = PyPDF4.PdfFileWriter()
        for pageNumber in range(midPage, numPages):
            pdfPart2Writer.addPage(pdfReader.getPage(pageNumber))

        fullPathToFile2 = os.path.join(outputFolder, pdfFile.split('.')[0] + "_2.pdf")
        print ("Writing part 2 to " + fullPathToFile2)
        with open(fullPathToFile2, "wb") as outputFile2:
            pdfPart2Writer.write(outputFile2)

    # Archive the source PDF.
    sourceFile = os.path.join(inputFolder, pdfFile)
    archiveFile = os.path.join(archiveFolder, pdfFile)
    shutil.move(sourceFile, archiveFile)