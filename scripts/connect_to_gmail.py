# scripts/connect_to_gmail.py

import os
import base64
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.settings import GMAIL_SCOPES, CREDENTIALS_PATH, TOKEN_PATH, SENDER_EMAIL, RECEIVER_EMAILS

def create_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, GMAIL_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_mails(service, unread=False, num_of_msg=None, num_of_days=None):
    all_mails = []
    if unread:
        relevant_messages = list_messages(service)
    elif num_of_msg:
        relevant_messages = list_last_n_messages(service, n=num_of_msg)
    else:
        relevant_messages = get_emails_from_last_n_days(service, n=num_of_days)
    for msg in relevant_messages:
        mark_email_as_read(service, 'me', msg['id'])
        message, sender_email = get_message_details(service, 'me', msg['id'])
        if not sender_email or ("MAYA1" not in sender_email and "מאיה" not in sender_email):
            continue
        message_content = get_message_content(message)
        if message_content:
            all_mails.append(message_content)
    return all_mails

# Additional functions for send email, list messages, get message details, get message content, mark email as read, and get emails from last n days
