import base64
import os
import datetime as dt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from google.oauth2.credentials import Credentials
def sendMail(email:str):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())



    #creds = Credentials.from_authorized_user_file(filename = 'token.json', scopes = SCOPES)

    msg = MIMEMultipart()
    msg['to'] = email # The recipient's email address
    msg['subject'] = 'Attendance data'
    today = dt.datetime.now().strftime('%d-%B-%Y')
    msg.attach(MIMEText('Attendance record for {}'.format(today)))

    with open('data.csv', 'rb') as f:
        attach = MIMEApplication(f.read(),_subtype="csv")
        attach.add_header('Content-Disposition','attachment',filename=os.path.basename('data.csv'))
        msg.attach(attach)

    service = build('gmail', 'v1', credentials=creds)
    message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    try:
        send_message = (service.users().messages().send(userId="me", body=message).execute())
        print(F'sent message to {msg["to"]} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    os.remove('data.csv')


