# InsideTrading
InsideTrading is an application designed to automate the retrieval, processing, and analysis of insider trading information from emails and web pages.

The project uses credentials and token from Google API.

Please review and adjust the config/settings.py file before using the project.

## Features

- Connect to Gmail to retrieve relevant emails.
- Scrape web pages for insider trading information.
- Process and analyze the retrieved data.
- Save the processed data to CSV files.
- Send automated reports via email.
- ***coming soon - stock prediction based on CSV***

## Project Structure

```
InsideTrading/
│
├── config/
│   ├── __init__.py
│   ├── settings.py                # Configuration and settings
│
├── data/
│   ├── emails_data.csv
│   ├── emails_data_test.csv
│
├── scripts/
│   ├── __init__.py
│   ├── connect_to_gmail.py        # Gmail API connection and functions
│   ├── connect_to_maya.py         # Functions to interact with Maya
│   ├── csv_manipulations.py       # CSV handling and manipulation
│   ├── scraping.py                # Scraping functions
│
├── main.py                         # Main execution script
├── requirements.txt                
├── .gitignore                      
├── README.md                       
├── credentials.json                # Gmail API credentials (you need youe own)
├── token.json                      # Token file (you need youe own)
```

## Setup

### Prerequisites

- Python 3.7 or higher
- Google account with Gmail enabled
- ChromeDriver for Selenium

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/MIKIHERSHCOVITZ/InsideTrading.git
cd InsideTrading
```

2. **Set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required packages:**

```bash
pip install -r requirements.txt
```

## Gmail API Setup

**Enable the Gmail API:**

Go to the Gmail API page in the Google Cloud Console.

Click "Enable".

Create credentials (OAuth 2.0 Client IDs) and download the credentials.json file. Place it in the root directory of your project.


**Authenticate and create the token.json file:**

Run the following command to authenticate and create the token.json file:

```bash
python scripts/connect_to_gmail.py
```

## Running the Application

```bash
python main.py
```

## Usage
Data Retrieval: The application connects to Gmail to retrieve relevant emails based on predefined criteria.

Data Processing: Extracted data from emails and web pages is processed and analyzed.

CSV Handling: The processed data is saved to CSV files for further analysis or reporting.

Automated Reporting: Reports can be sent via email automatically.
