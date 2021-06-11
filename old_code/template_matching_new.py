import PyPDF2
import re

# creating a pdf file object
pdfFileObj = open('J1534.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# creating a page object
pageObj = pdfReader.getPage(0)

# extracting text from page
read = pageObj.extractText()

regex2 = re.compile(r'TOTAL|Alaska')
e = regex2.findall(read)
print(e)
