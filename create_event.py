import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from main import Func

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
        f = Func()
        file = f.openFile()
        start = f.date_start()
        end = f.date_end()
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': start,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end,
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

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Event Created: {created_event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error as occurred {error}")


def main():
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    create_event(service)

if __name__ == '__main__':
    main()