import re
from dateutil import parser
#import pdfplumber
import pymupdf

import date_patterns


class Func:

    def __init__(self):
        self.get_file = None
        self.end = None
        self.start = None
        self.combined_pattern = ''
        self.time = ''
        self.date = ''
        self.dates = []
        self.date_time = []
        self.goog_format = []
        self.append_dates = []
        self.get_file = input("File name: ")
        self.append_date_n_time = []


def main_func():
    date_patterns.get_dates()


if __name__ == '__main__':
    main_func()
