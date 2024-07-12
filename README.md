# InsideTrading
InsideTrading is an application designed to automate the retrieval, processing, and analysis of insider trading information from emails and web pages.


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
├── requirements.txt                # Project dependencies
├── .gitignore                      # Files to ignore in Git
├── README.md                       # Project description and instructions
├── credentials.json                # Gmail API credentials (you need youe own)
├── token.json                      # Token file (you need youe own)
```