import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from config.settings import CHROME_DRIVER_PATH


def make_get_request(url):
    """
    Make a GET request to a URL.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("GET request to", url, "was successful!")
            return response.text
        else:
            print("GET request to", url, "failed with status code", response.status_code)
    except Exception as e:
        print('An error occurred while making the GET request to', url, ':', e)
        return None


def use_selenium_for_url(url):
    """
    Use Selenium to extract all href links from a URL.
    """
    all_links = []

    # Specify the path to chromedriver.exe from an environment variable
    chromedriver_path = CHROME_DRIVER_PATH

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment if you need headless mode

    # Set up the driver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    try:
        # Navigate to the page
        driver.get(url)

        # Wait for the dynamic content to load
        time.sleep(5)  # Adjust this delay as necessary

        # Find the link by its partial href or another attribute that identifies it
        links = driver.find_elements(By.TAG_NAME, "a")

        # Print the href attribute of each link
        for link in links:
            href = link.get_attribute("href")
            if href:  # Skip any <a> elements without an href attribute
                all_links.append(href)
    finally:
        # Clean up by closing the browser window
        print("Finish")
        driver.quit()
        return all_links


def retrieve_text(url):
    """
    Use Selenium to retrieve all text from a URL.
    """
    # Specify the path to chromedriver.exe from an environment variable
    chromedriver_path = CHROME_DRIVER_PATH

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment if you need headless mode

    # Set up the driver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    try:
        # Navigate to the page
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)  # Adjust the sleep time if necessary

        # Find the <body> element and get its entire text content
        body_text = driver.find_element(By.TAG_NAME, "body").text

        # Print the text content
        return body_text
    finally:
        # Clean up: close the browser window
        driver.quit()
