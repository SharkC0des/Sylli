import re
from dateutil import parser
#import pdfplumber
import pymupdf
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
        self.append_dates = []
        self.append_date_n_time = []
        get_file = input("File name: ")
        with pymupdf.open(get_file) as pdf:
            for page in pdf:
                txt = page.get_text()
                self.date = r'\b(?:' + '|'.join(date_patterns)
                self.time = r')\b(?:\s+' + '|'.join(time_patterns) + r')?'
                self.combined_pattern = '|'.join(date_patterns)

                date_only = self.combined_pattern
                date_n_time = self.date + self.time
                self.dates = re.findall(date_only, txt)
                self.date_time = re.findall(date_n_time, txt)

                for i in self.date_time:
                    convert = parser.parse(i)
                    i = convert.isoformat()
                    self.append_date_n_time.append(i)

                for i in self.dates:
                    self.append_dates.append(i)

        return self.date_time

    def date_start(self):
        self.start = None
        frst = self.append_date_n_time[0]
        for i in range(len(self.append_dates) - 1):
            if self.append_dates[i] == self.append_dates[i+1]:
                if self.append_date_n_time[i] < self.append_date_n_time[i+1]:
                    self.start = self.append_date_n_time[i]

            else:
                for j in self.append_date_n_time:
                    if j < frst:
                        frst = j
                        self.start = j
                    else:
                        self.start = frst
        return self.start

    def date_end(self):
        self.end = None
        frst = self.append_date_n_time[0]
        for i in range(len(self.append_dates) - 1):
            if self.append_dates[i] == self.append_dates[i + 1]:
                if self.append_date_n_time[i] < self.append_date_n_time[i + 1]:
                    self.end = self.append_date_n_time[i]
            else:
                for j in self.append_date_n_time:
                    if j > frst:
                        frst = j
                        self.end = j
                    else:
                        self.end = frst
        return self.end


def main_func():
    main = Func()
    main.openFile()



