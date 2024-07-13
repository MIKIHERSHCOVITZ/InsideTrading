import time
from scripts.connect_to_gmail import get_mails, send_csv_to_mail, create_service
from scripts.connect_to_maya import use_selenium_for_url, retrieve_text
from scripts.csv_manipulations import write_to_csv
from scripts.scraping import extract_urls_from_html, pars_html, get_current_price
from functools import wraps


def gmail_service_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        service = create_service()
        return func(service, *args, **kwargs)

    return wrapper


@gmail_service_decorator
def process_mail(service, mail):
    try:
        all_urls = extract_urls_from_html(mail)
        maya_url = next(url for url in all_urls if "reports/details" in url)
        print(maya_url)

        links_from_maya_page = use_selenium_for_url(maya_url)
        link_to_html = next(link for link in links_from_maya_page if ".htm" in link)
        print(link_to_html)

        maya_html_page = retrieve_text(link_to_html)
        print(maya_html_page)

        return pars_html(maya_html_page)
    except Exception as ex:
        print(ex)
        return []


@gmail_service_decorator
def main(service):
    try:
        objects_for_csv = []
        mails = get_mails(service, unread=False, num_of_msg=600, num_of_days=None)

        for mail in mails:
            objects_for_csv.extend(process_mail(service, mail))
            time.sleep(5)

        clean_data = [json for json in objects_for_csv if json['שער עסקה'] != "0"]
        clean_data = get_current_price(clean_data)

        filename = 'emails_data.csv'
        if clean_data:
            write_to_csv(filename, clean_data)

        send_csv_to_mail(filename, clean_data)
        print("finished process successfully")
    except Exception as ex:
        print(ex)
        time.sleep(10)


if __name__ == '__main__':
    main()
