import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from crewai.tools import BaseTool
from pydantic import Field
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar.readonly"
]

def get_google_services():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing Google Access Token...")
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError("Google Cloud credentials.json is missing! Please download it from GCP Console.")
            
            print("Starting Google OAuth Flow. A browser window should open...")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        gmail_service = build("gmail", "v1", credentials=creds)
        calendar_service = build("calendar", "v3", credentials=creds)
        return gmail_service, calendar_service
    except HttpError as error:
        print(f"An error occurred in getting Google services: {error}")
        return None, None

class GmailReadTool(BaseTool):
    name: str = "Read Unread Emails"
    description: str = "Fetches the latest unread emails from the user's Gmail inbox. Useful for summarize the daily emails."

    def _run(self) -> str:
        try:
            gmail_service, _ = get_google_services()
            if not gmail_service:
                return "Error: Could not authenticate with Google."

            # Call the Gmail API
            results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=5).execute()
            messages = results.get('messages', [])

            if not messages:
                return "You have no unread emails."
            
            email_summaries = []
            for message in messages:
                msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
                headers = msg['payload']['headers']
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                sender = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')
                snippet = msg.get('snippet', '')
                email_summaries.append(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n---")
                
            return "\n".join(email_summaries)

        except Exception as error:
            return f"An error occurred reading emails: {error}"


class CalendarReadTool(BaseTool):
    name: str = "Read Upcoming Events"
    description: str = "Fetches the upcoming events from the user's Google Calendar. Useful for planning the day."

    def _run(self) -> str:
        try:
            _, calendar_service = get_google_services()
            if not calendar_service:
                return "Error: Could not authenticate with Google."

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = calendar_service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                return "No upcoming events found in your calendar."

            event_summaries = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Untitled Event')
                event_summaries.append(f"Time: {start} | Event: {summary}")
                
            return "\n".join(event_summaries)

        except Exception as error:
            return f"An error occurred reading the calendar: {error}"
