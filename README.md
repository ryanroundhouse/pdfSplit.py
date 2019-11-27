# pdfSplit.py
This script will split a PDF in half, but only on a page that contains a string that indicates the start of a new segment.

Instructions  

Deploy Script and Pre-requisites
Navigate to Python’s download page and download then install any version in the version 3 stream of python.

Install Python 3 on the server where this script will be executed.

Download the pdfSplit.py script file, and put it in a scripts folder on the customer’s machine.

pdfSplit.py
5 KB
Navigate to the scripts folder and run the following command to install the PDF component for python:

pip install PyPDF4


Execute script

Get Help
The script can be executed in the following manner to get help:

py pdfSplit.py /?
Which will display the cli help information:



Look up page contents
The script can be executed in the following manner:

py pdfSplit.py /d <path to folder> <page number>
For example:

py .\pdfSplit.py /d "c:/users/rg85036/desktop/pdf" 2
Which could provide a similar output to:


This could be useful if you know what is and is not a first page of a bill (page number-wise) and need help finding a specific string to provide when splitting the PDF.


Split PDF
The script can be executed in the following manner:

py pdfSplit.py <path to folder> <path to archive folder> <path to output> <string to be present on first page of bill>
For example:

py pdfSplit.py "C:/Users/rg85036/Desktop/pdf" "C:/Users/rg85036/Desktop/pdf/archive" "C:/Users/rg85036/Desktop/pdf/output" CustomerAccountNumber
The following pseudocode describes the script’s functionality:

FOR EACH pdf in <path to folder>
  GET midpoint in PDF collection containing the <search string>
  WRITE new pdf with pages 0-midpoint to <output folder>
  WRITE new pdf with pages midpoint-end to <output folder>
  MOVE pdf to <archive folder>
This script assumes there is a search string that will be repeated only in the first page of each new bill.  This is a requirement so that we can detect a the page that starts a new bill and no bills are cut in half to be displayed in another customers' bill.