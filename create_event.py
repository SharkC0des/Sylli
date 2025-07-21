import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime
import date_patterns as dp
from desc import Descriptions
import desc as de

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_creds():
    creds = None

    if os.path.exists(r"CREDENTIALS\token.json"):
        #os.remove("CREDENTIALS/token.json")
        creds = Credentials.from_authorized_user_file(r"CREDENTIALS\token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(r"CREDENTIALS/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0, prompt='consent')

        with open(r"CREDENTIALS\token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def create_event(service):
    try:
        start_ = dp.time_start
        start_.sort(reverse=True)
        end_ = dp.time_end
        created_date = []
        i = 0
        frm_desc = de.Descriptions()
        frm_desc.main()
        desc_dates = de.dates
        rev_dates = sorted(desc_dates.items(), key=lambda x: x[0], reverse=True)
        final_date_desc = dict(rev_dates)


        while i <= len(start_) - 1:
            for k, val in final_date_desc.items():
                event = {
                    'summary': '',
                    'location': '',
                    'description': 'A chance to hear more about Google\'s developer products.',
                    'start': {
                        'dateTime': start_[i],
                        'timeZone': 'America/New_York',
                    },

                    'end': {
                        'dateTime': start_[i],
                        'timeZone': 'America/New_York',
                    },
                    'recurrence': [
                        'RRULE:FREQ=DAILY;COUNT=1'
                    ],
                    # 'attendees': [
                    #     {'email': 'lpage@example.com'},
                    #     {'email': 'sbrin@example.com'},
                    # ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }
                # to_end = []
                # for idx, val in enumerate(start_):
                #     same1 = datetime.strptime(start_[idx - 1][:10], '%Y-%m-%d')
                #     same2 = datetime.strptime(val[:10], '%Y-%m-%d')
                #     if same1 == same2:
                #         if same1[idx - 1] < val:
                #             to_end.append(val)
                #             mv = start_.pop(idx)
                #             event.update(end=mv)
                if len(start_) != 1:

                    same1 = datetime.strptime(start_[i][:10], '%Y-%m-%d')
                    same2 = datetime.strptime(start_[i + 1][:10], '%Y-%m-%d')
                    if same1 != same2:
                        if start_[i] not in created_date:
                            created_date.append(start_[i])

                            x = start_[i]
                            l = k
                            if x == l:
                                event['summary'] = final_date_desc[k]['summary']
                                event['description'] = final_date_desc[k]['description']

                            start_.pop(i)
                    created_event = service.events().insert(calendarId="primary", body=event).execute()
                    print(f"Event Created: {created_event.get('htmlLink')}")

                else:
                    if start_[i] not in created_date:
                        created_date.append(start_[i])
                        mv = start_.pop(i)
                        if len(start_) == 1:
                            event['start']['dateTime'] = start_[i]
                            event['end']['dateTime'] = mv
                            start_.pop(i)
                        else:
                            event['start']['dateTime'] = start_[i]
                            event['end']['dateTime'] = mv
                            start_.pop(i)

                        for k, val in final_date_desc.items():
                            if k == start_[i]:
                                l = k
                                event['summary'] = final_date_desc['summary']
                                event['description'] = final_date_desc['description']

                        created_event = service.events().insert(calendarId="primary", body=event).execute()
                        print(f"Event Created: {created_event.get('htmlLink')}")

                    if not start_:
                        break

                    else:
                        created_event = service.events().insert(calendarId="primary", body=event).execute()
                        print(f"Event Created: {created_event.get('htmlLink')}")
                        start_.pop(i)

    except HttpError as error:
        print(f"An error as occurred {error}")


def main():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    des = Descriptions()
    des.main()

    create_event(service)


if __name__ == '__main__':
    main()
