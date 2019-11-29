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

# Get Help
The script can be executed in the following manner to display help information:

```powershell
py pdfSplit.py /?
```

# Look up page contents
The script can be executed in the following manner in order to see the content of a specific page for all PDFs in the folder.  This should be used to figure out a search string that indicates the first page of each segment of the PDF.

```powershell
py pdfSplit.py /d <path to folder> <page number>
```

For example:
```powershell
py .\pdfSplit.py /d "c:/users/username/desktop/pdf" 2
```

# Split PDF
The script can be executed in the following manner:

```powershell
py pdfSplit.py <path to folder> <path to archive folder> <path to output> <string to be present on first page of bill>
```

For example:
```powershell
py pdfSplit.py "C:/Users/username/Desktop/pdf" "C:/Users/username/Desktop/pdf/archive" "C:/Users/username/Desktop/pdf/output" CustomerAccountNumber
```
## The following pseudocode describes the script’s functionality:

```pseudocode
FOR EACH pdf in <path to folder>
  GET midpoint in PDF collection containing the <search string>
  WRITE new pdf with pages 0-midpoint to <output folder>
  WRITE new pdf with pages midpoint-end to <output folder>
  MOVE pdf to <archive folder>
```

This script assumes there is a search string that will be repeated only in the first page of each new bill.  This is a requirement so that we can detect a the page that starts a new bill and no bills are cut in half to be displayed in another customers' bill.
