# STILL TO DO
# integration tests!
# error log
# make paths relative to where file is located
# on pi: crontab mailto
# on pi: git

# 'import' changes made on pi


from datetime import datetime
import json
from extractdata import extract_data

WATCHLIST = "watch.list"
LOGROOT = "logs/"


def get_list(file):
    with open(file) as f:
        return [line for line in f.read().splitlines() if line]
    
def price_watch(url):
    product_name, product_price, currency = extract_data(url)
    timestamp = str(datetime.now())
    json_dict = { "Product name": product_name,
                  "Product price": product_price,
                  "Currency": currency,
                  "URL": url,
                  "Timestamp": timestamp }
    print(f"Fetched: {url}\n{product_name}: {product_price} {currency}\n")
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
