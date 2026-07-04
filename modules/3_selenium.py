"""
Simple scraper that uses Selenium to search for a product,
open its page, parse the product information, and store it
in the database.
"""

import load_django

from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser_app.models import Product
from modules.parsers import parse_html_product_page


BASE_URL = "https://brain.com.ua/"
SEARCH_QUERY = "Apple iPhone 15 128GB Black"

SEARCH_INPUT_XPATH = '//div[@class="header-bottom"]//input[@type="search"]'
SEARCH_RESULT_XPATH = '//div[@class="qsr-products-list"]/a'
EXPECTED_ELEMENT_XPATH = '//div[@class="br-wrap-block wrap-block-product"]'


with webdriver.Chrome() as driver:
    wait = WebDriverWait(driver, 20)

    # Open the website.
    driver.get(BASE_URL)

    # Search for the product.
    search_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, SEARCH_INPUT_XPATH))
    )
    search_input.send_keys(SEARCH_QUERY)

    # Open the first search result.
    wait.until(
        EC.element_to_be_clickable((By.XPATH, SEARCH_RESULT_XPATH))
    ).click()

    # Wait until the product page is fully loaded.
    wait.until(
        EC.visibility_of_element_located((By.XPATH, EXPECTED_ELEMENT_XPATH))
    )

    # Retrieve the page HTML for parsing.
    html = driver.page_source

# Parse product information from the HTML.
parsed_product_data = parse_html_product_page(html)

# Save the parsed product if it does not already exist.
Product.objects.get_or_create(**parsed_product_data)

# Print parsed data for debugging purposes.
pprint(parsed_product_data, sort_dicts=False)
