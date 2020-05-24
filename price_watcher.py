# STILL TO DO
# integration tests!
# structure price_fetch object
# abstract links_list into file?
    # [prod_name, price_str, price_int, fetch_date, url]
# can fetch_html be further abstracted?

# usecase:
# https://www.thomann.de/intl/yamaha_slb_300_silent_bass.htm
# <span class="primary">€ 3.890</span>
# <h1 itemprop="name">Yamaha SLB 300 Silent Bass</h1>

import requests
import datetime
from extractdata import extract_data

WATCHLIST = "watch.list"

def get_list(file):
    with open(file) as f:
        return f.read().splitlines()

def determine_source(url):
    return url.split(".")[1]

def get_data(url):
    content = fetch_html(url)
    source = determine_source(url)
    return extract_data(content, source)

def fetch_html(url):
    errmsg = "URL retrieval problem at"
    fetched = requests.get(url)
    if fetched.status_code != 200:
        raise RuntimeError(f"{errmsg} {url}: status {fetched.status_code}")
    if len(fetched.content) < 50:
        raise RuntimeError(f"{errmsg} {url}: filesize too small: {len(fetched.content)}")
    if len(fetched.content) > 1000000:
        raise RuntimeError(f"{errmsg} {url}: filesize too great: {len(fetched.content)}")
    return fetched.content.decode('utf-8')

def price_watch(url):
    product_name, product_price, price_currency = get_data(url)
    fetch_date = datetime.datetime.now()
    print(f"{product_name}\n{price_currency} {product_price}\n{fetch_date}\n{url}\n")

if __name__ == "__main__":
    for url in get_list(WATCHLIST):
        try:
            price_watch(url)            
        except RuntimeError as e:
            print(f"RuntimeError: {e}\n-- skipping {url}\n")