# STILL TO DO
# integration tests!
# structure price_fetch object
# abstract links_list into file?
    # [prod_name, price_str, price_int, fetch_date]
# can fetch_html be further abstracted?

# usecase:
# https://www.thomann.de/intl/yamaha_slb_300_silent_bass.htm
# <span class="primary">€ 3.890</span>
# <h1 itemprop="name">Yamaha SLB 300 Silent Bass</h1>

import requests
import re
import datetime

links_list = (
    "https://www.thomann.de/intl/yamaha_slb_300_silent_bass.htm",
    "https://www.thomann.de/intl/aer_bottom_line_amp_one.htm",
    "https://www.thomann.de/intl/moog_one_16.htm"
)

RX_THOMANN_PRICE = '<span class="primary">(.*?)</span>'
RX_THOMANN_NAME = '<h1 itemprop="name">(.*?)</h1>'


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

def price_watch_thomann(url):
    content = fetch_html(url)
    name = rx_find(RX_THOMANN_NAME, content)
    price = rx_find(RX_THOMANN_PRICE, content)
    date = datetime.datetime.now()
    print(f"{name}\n{price}\n{date}\n{url}\n")

if __name__ == "__main__":
    for url in links_list:
        try:
            price_watch_thomann(url)            
        except RuntimeError as e:
            print(f"RuntimeError: {e} -- skipping {url}\n")