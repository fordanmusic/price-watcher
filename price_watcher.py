#!/usr/bin/env python3

import json
import os
from pathlib import Path
from datetime import datetime
from extract_data import extract_data

ROOT = str(Path(os.path.abspath(os.path.realpath(__file__))).parent)
WATCHLIST = ROOT + "/watch.list"
LOGROOT = ROOT + "/logs/"


def get_list(file):
    with open(file) as f:
        return [line for line in f.read().splitlines()
                if line and not line.startswith('#')]


def price_watch(url):
    product_name, product_price, currency, avail = extract_data(url)
    timestamp = str(datetime.now())
    json_dict = {"Product name": product_name,
                 "Product price": product_price,
                 "Currency": currency,
                 "Availability": avail,
                 "URL": url,
                 "Timestamp": timestamp}
    print(f"{product_name:50}{product_price:8} {currency:5}({avail})")
    return json_dict


if __name__ == "__main__":
    date = str(datetime.now().date())
    logfile = LOGROOT + "pw-" + date + ".json"
    with open(logfile, 'a+') as f:
        for url in get_list(WATCHLIST):
            try:
                json.dump(price_watch(url), f)
                f.write('\n')
            except RuntimeError as e:
                print(f"RuntimeError: {e}\n-- skipping {url}\n")
