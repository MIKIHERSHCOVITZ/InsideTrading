import re
import requests
from bs4 import BeautifulSoup

def extract_urls_from_html(html_content):
    """
    Extract all URLs from HTML content.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        url_tags = soup.find_all('a', href=True)
        urls = [tag['href'] for tag in url_tags]

        text_content = soup.get_text()
        text_urls = re.findall(r'https?://\S+', text_content)

        all_urls = list(set(urls + text_urls))
        all_urls = [requests.head(url).headers.get("Location", "") for url in all_urls]
        return all_urls
    except Exception as e:
        print('An error occurred while extracting URLs from HTML content:', e)
        return []

def get_href_attributes(html_content):
    """
    Extract all href attributes from HTML content.
    """
    href_attributes = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            href_attributes.append(a_tag['href'])
        return href_attributes
    except Exception as e:
        print('An error occurred while extracting href attributes from HTML content:', e)
        return []

def find_buttons(html_content):
    """
    Find all button texts in the HTML content.
    """
    buttons = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        for button_tag in soup.find_all('button'):
            buttons.append(button_tag.text.strip())
        return buttons
    except Exception as e:
        print('An error occurred while finding buttons on the HTML page:', e)
        return []

def find_feed_item_buttons(html_content):
    """
    Find all elements with class="feedItemButton" in the HTML content.
    """
    feed_item_buttons = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        feed_item_buttons = soup.find_all(class_="feedItemButton")
        return feed_item_buttons
    except Exception as e:
        print('An error occurred while finding elements with class="feedItemButton" on the HTML page:', e)
        return feed_item_buttons

def pars_html(html_file):
    """
    Parse the HTML content to extract relevant information.
    """
    num_list = [str(num) for num in range(10)]
    date = None
    lst = html_file.split("\n")
    objects_for_csv = []
    specific_obj = {}

    for row in lst:
        if "שם תאגיד/שם משפחה ושם פרטי של המחזיק:" in row:
            data = row.split(": ")
            corp_name = data[-1]
            specific_obj["שם מלא"] = corp_name
        if "תאריך השינוי:" in row and not date:
            data = row.split(" ")
            date = data[-1]
            specific_obj["תאריך"] = date
        if "שער העסקה:" in row:
            data = row.split(" ")
            value_per_share = data[2]
            specific_obj["שער עסקה"] = value_per_share
        if "שינוי בכמות" in row:
            data = row.split(" ")
            specific_obj["סוג עסקה"] = "קניה" if data[-1] == "+" else "מכירה"
            shares_in_transaction = data[-2]
            specific_obj["שינוי בכמות"] = shares_in_transaction
        if "יתרה (בכמות ניירות ערך) בדיווח האחרון:" in row:
            last_report_shares = "error"
            data = row.split(" ")
            for word in data:
                if word != "" and word[0] in num_list:
                    last_report_shares = word
                    break
            specific_obj["יתרה בדוח אחרון"] = last_report_shares
        if "יתרה נוכחית (בכמות ניירות ערך):" in row:
            current_report_shares = "error"
            data = row.split(" ")
            for word in data:
                if word != "" and word[0] in num_list:
                    current_report_shares = word
                    break
            specific_obj["יתרה בדוח נוכחי"] = current_report_shares
        if "מספר נייר ערך בבורסה:" in row:
            data = row.split(": ")
            share_number = data[-1]
            specific_obj["מספר נייר"] = share_number
        if "שם וסוג נייר הערך:" in row:
            data = row.split(": ")
            share_name = data[-1]
            specific_obj["שם נייר"] = share_name
        if len(specific_obj) == 9:
            if specific_obj["שער עסקה"][0] in num_list:
                cost_of_transaction = specific_obj["שער עסקה"]
                cost_of_transaction = float(cost_of_transaction.replace(",", '')) / 100
                change_amount = specific_obj["שינוי בכמות"]
                change_amount = float(change_amount.replace(",", ''))
                specific_obj["סכום עסקה"] = cost_of_transaction * change_amount
            else:
                specific_obj["סכום עסקה"] = "לא ידוע"
            objects_for_csv.append(specific_obj)
            specific_obj = {}
    return objects_for_csv

def get_current_price(new_json_list):
    """
    Get the current price of stocks from TheMarker finance.
    """
    for json_obj in new_json_list:
        try:
            paper_number = json_obj["מספר נייר"]
            url = f'https://finance.themarker.com/stock/{paper_number}'
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                json_obj['מחיר מניה בעת קריאת המייל'] = pars_html_marker(html_content)
        except Exception as ex:
            json_obj['מחיר מניה בעת קריאת המייל'] = ""
            print(ex)
            continue
    return new_json_list

def pars_html_marker(html_content):
    """
    Parse the HTML content from TheMarker to get the stock price.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    span_shaar = soup.find('span', text='שער')
    if span_shaar:
        next_span = span_shaar.find_next_sibling('span')
        if next_span:
            return next_span.text
    return None
