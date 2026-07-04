"""
Simple scraper that fetches a product page using the requests library,
parses the product information, and stores it in the database.
"""

from modules import load_django
from pprint import pprint

import requests

from parser_app.models import Product
from modules.parsers import parse_html_product_page


HEADERS = {
    "accept-language": "en-US,en;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "referer": "https://www.google.com/",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/149.0.0.0 Safari/537.36"
    ),
}

PRODUCT_URL = (
    "https://brain.com.ua/ukr/"
    "Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"
)

# Download the product page.
response = requests.get(url=PRODUCT_URL, headers=HEADERS)
response.raise_for_status()

# Parse product information from the HTML.
parsed_product_data = parse_html_product_page(html=response.text)

# Save the parsed product if it does not already exist.
Product.objects.get_or_create(**parsed_product_data)

# Print parsed data for debugging purposes.
pprint(parsed_product_data, sort_dicts=False)
