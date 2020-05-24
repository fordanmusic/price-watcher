# STILL TO DO
# integration tests!
# structure price_fetch object
# abstract links_list into file?
    # [prod_name, price_str, price_int, timestamp, url]
# can fetch_html be further abstracted?

# usecase:
# https://www.thomann.de/intl/yamaha_slb_300_silent_bass.htm
# <span class="primary">€ 3.890</span>
# <h1 itemprop="name">Yamaha SLB 300 Silent Bass</h1>

from datetime import datetime
import json
from extractdata import extract_data

WATCHLIST = "watch.list"
LOGROOT = "logs/"


def get_list(file):
    with open(file) as f:
        return f.read().splitlines()

def price_watch(url):
    product_name, product_price, currency = extract_data(url)
    timestamp = str(datetime.now())
    json_dict = { "Product name": product_name,
                  "Product price": product_price,
                  "Currency": currency,
                  "URL": url,
                  "Timestamp": timestamp }
    print(url)
    print(f"{product_name}: {product_price} {currency}")
    print()
    return json_dict

if __name__ == "__main__":
    date = str(datetime.now().date()) 
    logfile = LOGROOT + date + ".json"
    with open(logfile, 'a+') as f:
        for url in get_list(WATCHLIST):
            try:
                json.dump(price_watch(url), f)
                f.write('\n')            
            except RuntimeError as e:
                print(f"RuntimeError: {e}\n-- skipping {url}\n")