import re
from dateutil import parser
import pdfplumber
from date_patterns import time_patterns
from date_patterns import date_patterns

class Func:

    def __init__(self):
        self.end = None
        self.start = None
        self.combined_pattern = ''
        self.time = ''
        self.date = ''
        self.dates = []
        self.date_time = []
        self.goog_format = []


    def openFile(self):
        get_file = input("File name: ")
        with pdfplumber.open(get_file) as pdf:
            for page in pdf.pages:
                txt = page.extract_text()
                self.date = r'\b(?:' + '|'.join(date_patterns)
                self.time = r')\b(?:\s+' + '|'.join(time_patterns) + r')?'
                self.combined_pattern = '|'.join(date_patterns)

                date_only = self.combined_pattern
                date_n_time = self.date + self.time
                self.dates = re.findall(date_only, txt)
                self.date_time = re.findall(date_n_time, txt)
                print(self.dates)
        return self.date_time

    def date_start(self):
        self.start = None
        print(self.date_time, '3434')
        for idx, i in enumerate(self.date_time):
            for jdx, j in enumerate(self.date_time):
                if self.dates[idx] == self.dates[jdx] and i < j:
                    self.start = i
                elif self.dates:
                    self.start = i
        convert = parser.parse(self.start)
        self.start = convert.isoformat()
        print(self.start)
        return self.start

    def date_end(self):
        self.end = None
        print(self.date_time, 'edt')
        for idx, i in enumerate(self.date_time):
            for jdx, j in enumerate(self.date_time):
                # If dates are the same, Compare Time
                if self.dates[idx] == self.dates[jdx] and i < j:
                    self.end = j # J = Later date and time
                elif self.dates:
                    self.end = j
        convert = parser.parse(self.end)
        self.end = convert.isoformat()
        print(self.end)
        return self.end

if __name__ == '__main__':
    main = Func()
    main.openFile()
    main.date_start()
    main.date_end()

