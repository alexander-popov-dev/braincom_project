"""
Simple scraper that uses Playwright to search for a product,
open its page, parse the product information, and store it
in the database.
"""

import load_django

from pprint import pprint

from playwright.sync_api import sync_playwright

from parser_app.models import Product
from modules.parsers import parse_html_product_page


BASE_URL = "https://brain.com.ua/"
SEARCH_QUERY = "Apple iPhone 15 128GB Black"

SEARCH_INPUT_XPATH = '//div[@class="header-bottom"]//input[@type="search"]'
SEARCH_RESULT_XPATH = '//div[@class="qsr-products-list"]/a'
EXPECTED_ELEMENT_XPATH = '//div[@class="br-wrap-block wrap-block-product"]'


with sync_playwright() as playwright:
    driver = playwright.chromium.launch(headless=False)
    page = driver.new_page()

    # Open the website.
    page.goto(url=BASE_URL, wait_until="load")

    # Search for the product.
    search_input = page.locator(SEARCH_INPUT_XPATH)
    search_input.type(text=SEARCH_QUERY, delay=0.5)

    # Open the first search result.
    page.locator(SEARCH_RESULT_XPATH).first.click()

    # Wait until the product page is fully loaded.
    page.locator(EXPECTED_ELEMENT_XPATH).wait_for(state="visible")

    # Retrieve the page HTML for parsing.
    html = page.content()

# Parse product information from the HTML.
parsed_product_data = parse_html_product_page(html=html)

# Save the parsed product if it does not already exist.
Product.objects.get_or_create(**parsed_product_data)

# Print parsed data for debugging purposes.
pprint(parsed_product_data, sort_dicts=False)
