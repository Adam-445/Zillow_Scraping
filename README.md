# Zillow Listings Scraper & Google Forms Automator

A Python script that scrapes property listings from a stable Zillow clone website and automatically submits them to a Google Form.

> Uses a custom Zillow clone page to ensure consistent scraping results.
> 

---

## Key Features

- Web Scraping: Extracts property links, prices, and addresses using BeautifulSoup
- Form Automation: Auto-fills Google Forms with scraped data using Selenium
- Stable Testing: Targets a custom Zillow clone page to avoid breaking changes

## Tech Stack

- Scraping: BeautifulSoup, Requests
- Automation: Selenium WebDriver
- Environment: Python 3, ChromeDriver

## How It Works

1. Scrapes listing data from the stable Zillow clone page
2. Cleans and structures the data (price normalization, address formatting)
3. Automatically submits each listing to a Google Form
4. Results populate a Google Sheet for easy analysis

## Setup

1. Install requirements:

```bash
pip install beautifulsoup4 requests selenium

```

1. Download ChromeDriver matching your Chrome version
2. Run the script:

```bash
python main.py

```

---

### Notes

- The script targets a custom Zillow clone ([appbrewery.github.io/Zillow-Clone/](http://appbrewery.github.io/Zillow-Clone/)) to ensure reliability
- Google Form selectors may need updating if the form structure changes
- Built as part of the 100 Days of Python course.
- Includes error handling for individual listing processing
