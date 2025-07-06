import re

import pdfplumber

from date_patterns import date_patterns
def openFile():
    get_file = input("File name: ")
    with pdfplumber.open(get_file) as pdf:
        page = pdf.pages[0]
        txt = page.extract_text()

        combined_pattern = '|'.join(date_patterns)
        dates = re.findall(combined_pattern, txt)
        print(dates)
#dd


if __name__ == '__main__':
    openFile()