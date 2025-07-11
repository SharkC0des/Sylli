import re
from datetime import datetime
from dateutil.parser import parse
import pymupdf

patterns = [
    r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})\b', # Goog
    r'\b\d{4}-\d{2}-\d{2}\b',
    r'\b\d{1,2}[\/\-\.\–]\d{1,2}[\/\-\.\–]\d{2,4}\b', # 5/3/2023
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?(?:,\s*)\d{4}(?:\s+\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))?\b',
    r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}(?:\s+\d{1,2}:\d{2}\s?(?:AM|PM|am|pm))?\b',
    r'\b\d{1,2}\s*[\/\-\.\–]\s*\d{1,2}\s*[\/\-\.\–]\s*\d{2,4}\b',
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?,\s*\d{4}(?:\s+\d{1,2}:\d{2}\s?(?:AM|PM))?\b'
            ]

time_start = []
time_end = []

def get_dates():
    with pymupdf.open(get_file) as pdf:
        for page in pdf:
            txt = page.get_text()
            date_format = set()
            for i in patterns:

                for j in re.findall(i, txt, re.IGNORECASE):
                    date_format.add(j.strip())

            for j in sorted(date_format):
                re_format = re.sub(r'(\d)(st|nd|rd|th)', r'\1', j, flags=re.IGNORECASE)
                re_format = re.sub(r'\s*([\/\-\.\–])\s*', r'\1', re_format)

                try:
                    dt_n_time = parse(re_format, fuzzy=False, dayfirst=False)
                    goog = dt_n_time.isoformat()
                except Exception:
                    goog = None
                time_start.append(goog)

        # def sameDate():
        #     to_end = []
        #     for idx, val in enumerate(time_start):
        #         same1 = datetime.strptime(time_start[idx-1][:10], '%Y-%m-%d')
        #         same2 = datetime.strptime(val[:10], '%Y-%m-%d')
        #         if same1 == same2:
        #             if time_start[idx-1] < val:
        #                 to_end.append(val)
        #                 mv = time_start.pop(idx)
        #                 time_end.append(mv)
        #
        # sameDate()





def more_format():

    with pymupdf.open(get_file) as pdf:
        for page in pdf:
            txt = page.get_text()
            year = datetime.now().year
            date_format = re.search(
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December)'
                r'\s+(\d{1,2})(?:st|nd|rd|th)?\s*(?:and|&)\s*(\d{1,2})(?:st|nd|rd|th)?',
                txt, re.IGNORECASE
            )

            for i in patterns:
                for j in re.findall(i, txt, re.I):
                    time_start.append(j)

            month, d1, d2 = date_format.groups()
            time = re.search(r'(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(AM|PM|am|pm)', txt)
            hr, minits, sec = time.groups()

            for k in (d1, d2):
                start_dt = parse(f"{month} {k}, {year} {hr} {sec}")
                end_dt = parse(f"{month} {k}, {year} {minits} {sec}")
                time_start.append(start_dt.isoformat())
                time_end.append(end_dt.isoformat())





def main():
    global get_file
    get_file = input("File name: ")
    get_dates()
    while True:

        if time_start:
            break
        if not time_start:
            more_format()
            break

    return time_start







