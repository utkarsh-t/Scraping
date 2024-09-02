Scraping Tool
A Python-based scraping tool using FastAPI for automating the extraction of product information from Dental Stall. This tool allows you to scrape product names, prices, and images and supports configurable settings for limiting pages and using proxies.

Features
Scrape Product Information: Extract product title, price, and image from each page.
Configurable Settings:
Limit the number of pages to scrape.
Use a proxy for scraping.
Data Storage: Save scraped data as JSON files on local storage.
Notification: Print scraping status to the console.
Retry Mechanism: Handle request failures with retry logic.
Caching: Avoid updating unchanged product data.
Requirements
Python 3.8+
FastAPI
Requests
BeautifulSoup4
Redis (for caching)
Install dependencies:


pip install -r requirements.txt
Configuration
Create a .env file with the following content:

env

STATIC_TOKEN=your_static_token_here
DB_PATH=data.json
Usage
Run the FastAPI Application:


uvicorn app.main:app --reload
Scrape Data:

Send a POST request to /scrape with a JSON body:

json
//Example of curl request

curl -X POST "http://127.0.0.1:8000/scrape" -H "Content-Type: application/json" -H "Authorization: Bearer current_static_token_For_Scraping" -d '{
    "pages_limit": 3,
    "proxy": "http://your-proxy-here"
}'

Include the Authorization header with the static token.

File Structure
app/ - Contains FastAPI app, scraper logic, and utility functions.
cache/ - Manages caching with Redis.
db/ - Handles local JSON data storage.
requirements.txt - Project dependencies.