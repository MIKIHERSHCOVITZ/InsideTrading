# main.py

from scripts.connect_to_gmail import create_service, get_mails
from scripts.connect_to_maya import make_get_request, use_selenium_for_url
from scripts.scraping import extract_urls_from_html
from scripts.csv_manipulations import write_to_csv

def main():
    service = create_service()
    mails = get_mails(service, unread=True)
    all_data = []
    for mail in mails:
        data = extract_urls_from_html(mail)
        all_data.extend(data)
    write_to_csv('data/emails_data.csv', all_data)

if __name__ == "__main__":
    main()
