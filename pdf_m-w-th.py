# Feed from mondays, wednesdays, and thursdays
# Wait for Sales Team to generate PDF in Quarterly folder
# Extract Sector, Geography, Ownership %, and Total Value

# import pdfquery

# pdf = pdfquery.PDFQuery("mwth_2022Q2ex.pdf")
# pdf.load()

# pdf.tree.write('mwth_2022Q2ex.xml', pretty_print=True)



from pdfminer.layout import LAParams
from pdfminer.converter import PDFResourceManager
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.converter import TextConverter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdfminer.layout import LTTextBoxHorizontal

document = open('mwth_2022Q2.pdf', 'rb')
#Create resource manager
rsrcmgr = PDFResourceManager()
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.get_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    for element in layout:
        if isinstance(element, LTTextBoxHorizontal):
            print(element.bbox)


# update consisten coordinates for page summary