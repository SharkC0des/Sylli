import re
import datetime
import pdfplumber
from dateutil import parser
from date_patterns import date_patterns
def openFile():
    get_file = input("File name: ")
    with pdfplumber.open(get_file) as pdf:
        page = pdf.pages[0]
        txt = page.extract_text()

        combined_pattern = '|'.join(date_patterns)
        date = re.findall(combined_pattern, txt)
        print(date)



if __name__ == '__main__':
    openFile()