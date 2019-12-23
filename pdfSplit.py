import PyPDF4
import re
import io
import os
import sys
import shutil
import pdfTools

if (len(sys.argv) != 6 and len(sys.argv) != 4) or sys.argv[1] == "/?":
    pdfTools.displayHelp()
    sys.exit()

if len(sys.argv) == 4 and sys.argv[1] == "/d":
    inputFile = sys.argv[2]
    pageNumber = int(sys.argv[3])
    if os.path.exists(inputFile) and os.path.isfile(inputFile):
        print("Displaying page " + str(pageNumber) + " of " + inputFile)
        with open(inputFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            if pageNumber >= pdfReader.getNumPages():
                print("Specified page number is larger than the number of pages in the document (Zero-indexed).")
                sys.exit(-1)
            print(pdfTools.getContentsOfPageFromPDF(pdfReader, pageNumber))
    else:
        print("file does not exist.")
        sys.exit(-1)
    sys.exit()

inputFolder = sys.argv[1]
archiveFolder = sys.argv[2]
outputFolder = sys.argv[3]
searchString = sys.argv[4]
idealPagesPerFile = int(sys.argv[5])

print ("supplied arguments:")
print ("inputFolder: " + inputFolder)
print ("archiveFolder " + archiveFolder)
print ("outputFolder " + outputFolder)
print ("searchString " + searchString)
print ("idealPagesPerFile " + str(idealPagesPerFile))

# Create all folders if they don't exist yet
if os.path.exists(archiveFolder) == False:
    print("archive folder doesn't exist.  Creating...")
    os.mkdir(archiveFolder)
if os.path.exists(outputFolder) == False:
    print("output folder doesn't exist.  Creating...")
    os.mkdir(outputFolder)

# Find all PDF files in the input folder.
absoluteFolder = os.path.abspath(inputFolder)
print("checking for bills in folder " + absoluteFolder)
filesInFolder = [f for f in os.listdir(absoluteFolder) if os.path.isfile(os.path.join(absoluteFolder,f))]
for fi in filesInFolder:
    print("found bill named " + fi)
pdfFiles = filter(lambda f: f.endswith(('.pdf','.PDF')), filesInFolder)
pdfFileList = []
for pdfFile in pdfFiles:
    pdfFileList.append(pdfFile)
print ("Found " + str(len(pdfFileList)) + " PDF files:")

for pdfFile in pdfFileList:
    print("Splitting " + pdfFile)
    with open(os.path.join(absoluteFolder, pdfFile), 'rb') as pdfFileObj:
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
        pageSplits = pdfTools.findBillBreaks(pdfReader, idealPagesPerFile, searchString)

        splitIndex = 0
        nextSplit = 0
        if len(pageSplits) > 0:
            while True:
                if (splitIndex >= len(pageSplits)):
                    pageToStopSplit = pdfReader.getNumPages()
                    #splitIndex += 1
                else:
                    pageToStopSplit = pageSplits[splitIndex]
                print("building up part " + str(splitIndex + 1) + "...")
                pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
                pdfWriter = PyPDF4.PdfFileWriter()
                for pageNumber in range(nextSplit, pageToStopSplit):
                    pdfWriter.addPage(pdfReader.getPage(pageNumber))
                fullPathToFile = os.path.join(outputFolder, pdfFile.split('.')[0] + "_" + str(splitIndex + 1) + ".pdf")
                print("writing chunk " + str(splitIndex) + " to " + fullPathToFile)
                with open(fullPathToFile, "wb") as outputFile:
                    pdfWriter.write(outputFile)
                if (splitIndex >= len(pageSplits)):
                    break
                nextSplit = pageSplits[splitIndex]
                splitIndex += 1
        else:
            print("no breaks to split on no search string found.")
            sourceFile = os.path.join(inputFolder, pdfFile)
            outputFile = os.path.join(outputFolder, pdfFile)
            print("copying " + sourceFile + " to " + outputFile)
            shutil.copy(sourceFile, outputFile)

    # Archive the source PDF.
    sourceFile = os.path.join(inputFolder, pdfFile)
    archiveFile = os.path.join(archiveFolder, pdfFile)
    print("archiving " + sourceFile + " to " + archiveFile)
    shutil.move(sourceFile, archiveFile)