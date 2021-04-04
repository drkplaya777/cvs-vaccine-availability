"""Sends emails via Gmail(BARS)"""
import os
import pprint
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from apiclient import errors


from app.utils.functions import get_project_root


SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.compose"]


def get_gmail_service():
    """Opens a connection to the Gmail Api

    Returns:
        A Resource object with methods for interacting with the gmail service.
    """
    token = load_token()
    token = login_user(token)

    service = build('gmail', 'v1', credentials=token)

    return service


def load_token() -> Credentials:
    """Loads a user's access token

    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    token_file_path = get_token_file_path()
    credentials = None

    if os.path.exists(token_file_path):
        credentials = Credentials.from_authorized_user_file(token_file_path,
                                                            SCOPES)

    return credentials


def get_token_file_path() -> str:
    """Loads a users access token file. """
    project_root = get_project_root()
    token_file_path = os.path.join(project_root, 'token.json')

    return token_file_path


def login_user(credentials: Credentials = None) -> Credentials:
    """Logs a user into their Google account

    This functions doubles a validation of credentials too. Tokens are a MUST
    when interacting with Google's APIs, therefore this function ensures we
    always have a token.
    """
    credentials_file_path = get_credentials_file_path()

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES)
            credentials = flow.run_local_server(port=0)

            save_token(credentials)

            return credentials
    return credentials


def get_credentials_file_path() -> str:
    """Loads a users credentials file from a JSON file.

    We need this credentials file to open a connection to any Google API.
    Therefore, this function is a MUST as it loads the JSON configuration file
    from any location on a server.
    """
    credentials_file_path = os.environ['gmail_credentials_file_path']

    return credentials_file_path


def save_token(credentials: Credentials) -> None:
    """Saves a Gmail JSON token to the file system

    Save the credentials for the next run of the application.
    """
    token_file_path = get_token_file_path()

    with open(token_file_path, 'w') as token:
        token.write(credentials.to_json())


def create_email(
        from_address: str, to_address: str, subject: str, email_body: str
):
    """Create a message for an email.
      Args:
        from_address: Email address of the sender.
        to_address: Email address of the receiver.
        subject: The subject of the email message.
        email_body: The text of the email message.
      Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    msg = MIMEText(email_body, "html")
    msg['subject'] = subject
    msg['to'] = to_address

    message.attach(msg)
    message_body = msg.as_bytes()
    encoded_message = base64.urlsafe_b64encode(message_body)

    electronic_mail = {'raw': encoded_message.decode()}

    return electronic_mail


def send_email(gmail_service, user_id: str, email_body: str):
    """Send an email message.
      Args:
          gmail_service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me" can be used to
          indicate the authenticated user.
          email_body: Message to be sent.

      Returns:
        Sent Message.
    """
    try:
        message = (gmail_service
                   .users()
                   .messages()
                   .send(userId=user_id, body=email_body)
                   .execute())
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    else:
        print('Message Id: %s' % message['id'])

        return message


def get_email(email_address: str, email_id: str, gmail_service) -> dict:
    """Retrieves an email from a gmail Inbox using its message id"""
    txt = (gmail_service
           .users()
           .messages()
           .get(userId=email_address, id=email_id)
           .execute())

    return txt


def get_email_subject(email_message) -> str:
    """Parses out the email subject from an email message"""
    sent_email_payload = email_message['payload']
    sent_email_headers = sent_email_payload['headers']
    sent_email_subject = None

    for header in sent_email_headers:
        if header['name'].upper() == 'SUBJECT':
            sent_email_subject = header['value']

    return sent_email_subject
