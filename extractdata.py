import re
import requests

RX_THOMANN_PRICE = '<span class="primary">(.*?)</span>'
RX_THOMANN_NAME = '<h1 itemprop="name">(.*?)</h1>'



def determine_source(url):
    return url.split(".")[1]

def extract_data(url):
    source = determine_source(url)
    if source == "thomann":
        return extract_data_thomann(url)
    else:
        raise RuntimeError(f"Unknown source: {source}")



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


##
## functions for specific stores
##
def extract_data_thomann(url):
    content = fetch_html(url)
    name = rx_find(RX_THOMANN_NAME, content)
    curr, price = rx_find(RX_THOMANN_PRICE, content).split(" ")
    price = int(price.replace(".", ""))
    return name, price, curr




if __name__ == "__main__":
    pass