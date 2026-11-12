"""
production:
-beatifulsoup4
_requests
_schedule

dev:
-pytest
-black

webscraper_project/
|--scraper.py
|-- tests/
    |- test_scraper.py

Your Tasks:
1. Set up a virtual environment for the project using uv.
2. Create separate dependency files for production(base) and development.
3. GEnerate locked requirements.txt files for both environments.
4. Write down the commands to sync the development environment so you can run the tests.

 """

import requests
from bs4 import BeautifulSoup


def scrape_title(url):
    """Scrapes the title from a fiven URL"""
    try:
        response=requests.get(url,timeout=5)
        response.raise_for_status() # RAises an HTTPError for bad responses
        soup=BeautifulSoup(response.text,"html.parser")
        return soup.title.string
    except requests.RequestException as e:
        return f"Error: {e}"

