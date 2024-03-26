import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta

from listing import Listing


def scrape_ebay_macbooks():
    global title, price, category
    url = "https://www.ebay.com/sch/i.html?_nkw=macbook&_sop=12&_ipg=100"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all("div", class_="s-item__info")

        for listing in listings:
            title_element = listing.find("div", class_="s-item__title")
            if title_element:
                title = title_element.text
            else:
                title = "Title not available"

            price_element = listing.find("span", class_="s-item__price")
            if price_element:
                price = price_element.text
            else:
                price = "Price not available"

            category_element = listing.find("div", class_="s-item__subtitle")
            if category_element:
                category = category_element.text
            else:
                category = "Category not available"
            new_listing = Listing(title, price, category)
            new_listing.print_all_details()
            new_listing.save_to_database()
        else:
            print("Failed to fetch page.")


def store_in_database(list2):
    conn = sqlite3.connect('ebay_macbooks.db')
    c = conn.cursor()
    for list1 in list2:
        c.execute('''CREATE TABLE IF NOT EXISTS listings
                 (id INTEGER PRIMARY KEY, title TEXT, price TEXT, category TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        c.execute("INSERT INTO listings (title, price, category) VALUES (?, ?, ?)", (list1.title, list1.price, list1.category))
        conn.commit()
        conn.close()


def main():
    scrape_ebay_macbooks()


if __name__ == "__main__":
    main()
