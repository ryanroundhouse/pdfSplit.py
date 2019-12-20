import unittest
import pdfTools
import PyPDF4

class TestPdfTools(unittest.TestCase): 
    def test_SingleBillReturnsEmptyArray(self):
        # Test that when passed a file with a single page, it should return empty array
        pdfFile = "./samples/OneBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            self.assertEqual(pdfTools.findBillBreaks(pdfReader, 1, "First Page"), [])

    def test_ChunkBiggerThanFileReturnsEmptyArray(self):
        # Test that 5 single page bills should return empty array when the chunk is larger than the number of pages
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            self.assertEqual(pdfTools.findBillBreaks(pdfReader, 10, "First Page"), [])
    
    def test_ErrorDisplayedIfNegativeChunkSize(self):
        # Test we receive an exception if invalid chunk size is specified
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            with self.assertRaises(Exception):
                pdfTools.findBillBreaks(pdfReader, -1, "First Page")

    def test_GetPageContent(self):
        # Test getting the page contents
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj) 
            self.assertEqual(pdfTools.getContentsOfPageFromPDF(pdfReader, 0), "First Page (Page 1)   ")

    def test_GetPageContentErrorIfNotPositivePage(self):
        # Test we receive an exception when getting page content and invalid chunk size is specified
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            with self.assertRaises(Exception):
                pdfTools.findBillBreaks(pdfReader, -1, "First Page")

    def test_NotAlwaysMultipageBill2Chunk(self):
        # Test that the multipage bill file with size 2 chunks returns [2, 5]
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            self.assertEqual(pdfTools.findBillBreaks(pdfReader, 2, "First Page"), [2, 5])

    def test_NotAlwaysMultipageBill3Chunk(self):
        # Test that the multipage bill file with size 3 chunks returns [5]
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            self.assertEqual(pdfTools.findBillBreaks(pdfReader, 3, "First Page"), [5])

    def test_NotAlwaysMultipageBill1Chunk(self):
        # Test that the multipage bill file with size 1 chunks returns [1, 2, 5]
        pdfFile = "./samples/NotAlwaysMultipageBill.pdf"
        with open(pdfFile, 'rb') as pdfFileObj:
            pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
            self.assertEqual(pdfTools.findBillBreaks(pdfReader, 1, "First Page"), [1, 2, 5])