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
import re
import datetime

WATCHLIST = "watch.list"

# links_list = (
#     "https://www.thomann.de/intl/yamaha_slb_300_silent_bass.htm",
#     "https://www.thomann.de/intl/aer_bottom_line_amp_one.htm",
#     "https://www.thomann.de/intl/moog_one_16.htm",
# )

RX_THOMANN_PRICE = '<span class="primary">(.*?)</span>'
RX_THOMANN_NAME = '<h1 itemprop="name">(.*?)</h1>'


def get_list(file):
    with open(file) as f:
        return f.read().splitlines()

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

def rx_find(pattern, content):
    found = re.search(pattern, content)
    if not found:
        raise RuntimeError(f"Not found")
    return found.group(1)

def determine_source(url):
    return url.split(".")[1]

def extract_data(content, source):
    if source == "thomann":
        return extract_data_thomann(content)

def extract_data_thomann(content):
    name = rx_find(RX_THOMANN_NAME, content)
    curr, price = rx_find(RX_THOMANN_PRICE, content).split(" ")
    price = int(price.replace(".", ""))
    return name, price, curr

def fetch_data(url):
    content = fetch_html(url)
    source = determine_source(url)
    return extract_data(content, source)

def price_watch(url):
    product_name, product_price, price_currency = fetch_data(url)
    fetch_date = datetime.datetime.now()
    print(f"{product_name}\n{price_currency} {product_price}\n{fetch_date}\n{url}\n")


if __name__ == "__main__":
    for url in get_list(WATCHLIST):
        try:
            price_watch(url)            
        except RuntimeError as e:
            print(f"RuntimeError: {e} -- skipping {url}\n")