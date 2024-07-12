# scripts/connect_to_maya.py

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from config.settings import CHROME_DRIVER_PATH

def make_get_request(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"GET request to {url} failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred while making the GET request to {url}: {e}")

def use_selenium_for_url(url):
    all_links = []
    service = Service(CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(5)
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href:
                all_links.append(href)
    finally:
        driver.quit()
        return all_links

# Additional functions to retrieve text from a URL using Selenium
