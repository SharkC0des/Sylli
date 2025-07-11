import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import date_patterns as dp

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_creds():
    creds = None

    if os.path.exists(r"CREDENTIALS\token.json"):
        creds = Credentials.from_authorized_user_file(r"CREDENTIALS\token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(r"CREDENTIALS/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

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
        while i <= len(start_) -1:
            to_end = []
            event = {
                'summary': 'Google I/O 2015',
                'location': '800 Howard St., San Francisco, CA 94103',
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
                same2 = datetime.strptime(start_[i+1][:10], '%Y-%m-%d')
                if same1 != same2:
                    if start_[i] not in created_date:
                        created_date.append(start_[i])
                        created_event = service.events().insert(calendarId="primary", body=event).execute()
                        print(f"Event Created: {created_event.get('htmlLink')}")
                        start_.pop(i)


                else:
                    if start_[i] > start_[i+1]:
                        to_end.append(start_[i])
                        if start_[i] not in created_date:
                            created_date.append(start_[i])
                            created_date.append(start_[i+1])
                            mv = start_.pop(i)
                            event['start']['dateTime'] = start_[i]
                            event['end']['dateTime'] = mv
                            start_.pop(i)
                            start_.pop(i+1)
                            created_event = service.events().insert(calendarId="primary", body=event).execute()
                            print(f"Event Created: {created_event.get('htmlLink')}")

            else:
                created_event = service.events().insert(calendarId="primary", body=event).execute()
                print(f"Event Created: {created_event.get('htmlLink')}")
                start_.pop(i)






    except HttpError as error:
        print(f"An error as occurred {error}")


def main():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    dp.main()
    create_event(service)
