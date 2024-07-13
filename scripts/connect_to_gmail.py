import os
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64

from config.settings import SENDER_EMAIL, RECEIVER_EMAILS, TOKEN_PATH, CREDENTIALS_PATH, GMAIL_SCOPES


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
    print("num of messages:", len(relevant_messages))
    for msg in relevant_messages:
        print(f"relevant_message is {msg}")
        mark_email_as_read(service, 'me', msg['id'])
        message, sender_email = get_message_details(service, 'me', msg['id'])
        print(f"sender_email is {sender_email}")
        if not sender_email or ("MAYA1" not in sender_email and "מאיה" not in sender_email):
            continue
        message_content = get_message_content(message)
        if message_content:
            all_mails.append(message_content)
    return all_mails

def list_messages(service, user_id='me'):
    try:
        query = 'is:unread -in:sent'
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except Exception as e:
        print('An error occurred:', e)
        return []

def get_message_details(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        sender_email = None
        headers = message.get('payload', {}).get('headers', [])
        for header in headers:
            if header.get('name') == 'From':
                sender_email = header.get('value')
                break
        return message, sender_email
    except Exception as e:
        print('An error occurred:', e)
        return None, None

def get_message_content(message):
    try:
        msg_str = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'].encode('ASCII')).decode('utf-8')
        return msg_str
    except Exception as e:
        print('An error occurred while extracting message content:', e)
        return None

def list_last_n_messages(service, user_id='me', n=3):
    try:
        query = '-in:sent'
        response = service.users().messages().list(userId=user_id, q=query, maxResults=n).execute()
        messages = response.get('messages', [])
        messages.reverse()
        return messages
    except Exception as e:
        print('An error occurred:', e)
        return []

def mark_email_as_read(service, user_id, msg_id):
    try:
        modified_message = service.users().messages().modify(userId=user_id, id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        print("Email marked as read:", modified_message)
    except Exception as e:
        print(f'Failed to send message: {e}')
        if hasattr(e, 'resp'):
            print(f'Status code: {e.resp.status}, Response: {e.resp.reason}')

def get_emails_from_last_n_days(service, n):
    try:
        date_n_days_ago = datetime.now() - timedelta(days=n)
        formatted_date = date_n_days_ago.strftime("%Y/%m/%d")
        query = f"after:{formatted_date} -in:sent"
        response = service.users().messages().list(userId='me', q=query).execute()
        messages = response.get('messages', [])
        return messages
    except Exception as e:
        print('An error occurred while retrieving emails:', e)
        return []

def send_email_with_attachment(service, sender_email, receiver_email, subject, message_text, file_path):
    try:
        message = create_message_with_attachment(sender_email, receiver_email, subject, message_text, file_path)
        send_message(service, sender_email, message)
        print("Email with attachment sent successfully.")
    except Exception as e:
        print('An error occurred while sending email with attachment:', e)

def create_message_with_attachment(sender_email, receiver_email, subject, message_text, file_path):
    message = MIMEMultipart()
    message['to'] = receiver_email
    message['from'] = sender_email
    message['subject'] = subject
    message.attach(MIMEText(message_text, 'plain'))
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
    message.attach(part)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: {}'.format(message['id']))
    except Exception as e:
        print('An error occurred:', e)

def create_simple_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_simple_email(service, sender_email, receiver_email, subject, message_text):
    message = create_simple_message(sender_email, receiver_email, subject, message_text)
    send_message(service, sender_email, message)

def send_csv_to_mail(filename, clean_data):
    service = create_service()
    sender_email = SENDER_EMAIL
    receiver_emails = RECEIVER_EMAILS
    subject = 'weekly update on inside trading'
    message_text = f'Please find the attached CSV file. \n Number of rows added is {len(clean_data)}' if clean_data else 'No new update on inside trading'
    for receiver_email in receiver_emails:
        try:
            if clean_data:
                send_email_with_attachment(service, sender_email, receiver_email, subject, message_text, filename)
            else:
                send_simple_email(service, sender_email, receiver_email, subject, message_text)
        except Exception as e:
            print(f'Failed to send message: {e}')
            if hasattr(e, 'resp'):
                print(f'Status code: {e.resp.status}, Response: {e.resp.reason}')
