# scripts/scraping.py

import re
import requests
from bs4 import BeautifulSoup

def extract_urls_from_html(html_content):
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
        print(f'An error occurred while extracting URLs from HTML content: {e}')
        return []

# Additional functions for scraping and parsing HTML content
