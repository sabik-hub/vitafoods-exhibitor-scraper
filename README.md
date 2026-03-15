# Vitafoods Exhibitor Scraper

Python web scraper that collects exhibitor information from the Vitafoods event directory.

## Features

- Automatic pagination handling
- Selenium automation
- HTML parsing with BeautifulSoup
- Data export to Excel

## Extracted Data

The scraper collects:

- Company Name
- Stand
- Hall
- Country
- Description
- Profile Link

## Installation

Clone the repository

```
git clone https://github.com/sabik-hub/vitafoods-exhibitor-scraper.git
```

Install dependencies

```
pip install -r requirements.txt
```

Run the scraper

```
python scraper.py
```

## Output

The scraper generates:

```
vitafoods_exhibitors.xlsx
```

## Screenshot

!(screenshots/scraper_result.png)
