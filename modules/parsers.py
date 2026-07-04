"""
HTML parser for Brain product pages.

Extracts product information from a Brain product page and returns
it as a dictionary.
"""
import json
import re

from bs4 import BeautifulSoup, Tag


def _get_spec_value(specs_block: Tag | None, label: str) -> str | None:
    """Return the specification value for the given label."""
    try:
        label_element = specs_block.find("span", string=label)
        return label_element.find_next_sibling("span").get_text(strip=True)
    except AttributeError:
        return None


def parse_html_product_page(html: str) -> dict:
    """
    Parse a Brain product page and extract product information.

    Args:
        html: Raw HTML content of the product page.

    Returns:
        A dictionary containing the extracted product fields.

    Raises:
    ValueError:
        If the required product data cannot be extracted from the page.
    """
    soup = BeautifulSoup(html, "html.parser")

    specs_block = soup.find(name="div", class_="br-pr-chr")
    if specs_block is None:
        raise ValueError("Specifications block was not found.")

    product_data_script = soup.find(name="script", string=lambda t: t and "CURRENT_PRODUCT " in t)
    if product_data_script is None:
        raise ValueError("CURRENT_PRODUCT script was not found.")

    match = re.search(r"var CURRENT_PRODUCT = ({.*?});", product_data_script.get_text(strip=True), re.DOTALL)
    if match is None:
        raise ValueError("Unable to find CURRENT_PRODUCT JSON.")
    product_data_json = json.loads(match.group(1))

    product_review_photos_script = soup.find(name="script", string=lambda t: t and '"@type": "Product"' in t)
    if product_review_photos_script is None:
        raise ValueError("Product JSON-LD script was not found.")
    product_review_photos_json = json.loads(product_review_photos_script.get_text(strip=True))

    product = {
        "title": product_data_json.get("Name"),
        "vendor": product_data_json.get("VendorName"),
        "product_code": product_data_json.get("ProductCode"),
        "photos": product_review_photos_json.get("image"),
        "color": _get_spec_value(specs_block=specs_block, label="Колір"),
        "memory": _get_spec_value(specs_block=specs_block, label="Вбудована пам'ять"),
        "diagonal": _get_spec_value(specs_block=specs_block, label="Діагональ екрану"),
        "display_resolution": _get_spec_value(specs_block=specs_block, label="Роздільна здатність екрану"),
    }

    reviews_count = product_review_photos_json.get("aggregateRating", {}).get("reviewCount")
    product["reviews_count"] = str(reviews_count) if reviews_count is not None else None

    promo_price = product_data_json.get("OriginalRetailPrice")
    product["promo_price"] = str(promo_price) if promo_price is not None else None

    price = product_data_json.get("WithoutDiscountPrice")
    product["price"] = str(price) if price not in (None, 0, "0") else product["promo_price"]

    specifications = {}

    for spec_category in specs_block.find_all("div", recursive=False):
        category_name = spec_category.find("h3").get_text(strip=True)
        specifications[category_name] = {}

        specs = spec_category.find("div", recursive=False).find_all("div")

        for spec in specs:
            spans = spec.find_all("span", recursive=False)
            key = spans[0].get_text(separator=" ", strip=True)
            value = " ".join(spans[1].get_text().split())
            specifications[category_name][key] = value

    product["specifications"] = specifications

    return product
