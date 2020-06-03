import re
import requests

NAME_THOMANN = '<h1 itemprop="name">(.*?)</h1>'
PRICE_THOMANN = '<span class="primary">(.*?)</span>'
AVAIL_THOMANN = '<span class="rs-layover-trigger-text">(.*?)</span>'

NAME_KIWI = '<h1 class="heading-title">(.*?)</h1>'
PRICE_KIWI = '<span class="product-price">(.*?)</span>'
AVAIL_KIWI = '<span class="journal-stock instock">(.*?)<br ?/>'


def fetch_html(url):
    errmsg = "URL retrieval problem at"
    fetched = requests.get(url, timeout=10)
    if fetched.status_code != 200:
        raise RuntimeError(f"{errmsg} {url}: status {fetched.status_code}")
    if fetched.headers['Content-Type'].split(';')[0] != 'text/html':
        raise RuntimeError(
            f"{errmsg} {url}: content type wrong: {fetched.headers['Content-Type']}")
    if len(fetched.content) < 50:
        raise RuntimeError(
            f"{errmsg} {url}: filesize too small: {len(fetched.content)}")
    if len(fetched.content) > 1000000:
        raise RuntimeError(
            f"{errmsg} {url}: filesize too great: {len(fetched.content)}")
    return fetched.content.decode('utf-8')


def strip_html(line):
    line = re.sub('</?b>', '', line)
    line = re.sub('</?span(.*?)>', '', line)
    return line


def rx_find(pattern, content):
    found = re.search(pattern, content)
    if not found:
        raise RuntimeError(f"Not found: {pattern}")
    return strip_html(found.group(1))


def get_price(price_str):
    price_str = price_str.replace(".", "")
    price_str = price_str.replace(",", ".")
    return float(price_str)


def get_currency(symbol):
    if symbol == '\u20ac':
        return "EUR"
    else:
        return None


def extract_data_store(url, NAME_RX, PRICE_RX, AVAIL_RX):
    content = fetch_html(url)
    name = rx_find(NAME_RX, content)
    curr_sym, price = rx_find(PRICE_RX, content).split(" ")
    avail = rx_find(AVAIL_RX, content)
    price = get_price(price)
    curr = get_currency(curr_sym)
    return name, price, curr, avail


def determine_source(url):
    try:
        return re.match('https?://(www\.)?(.*?)\.', url).group(2)
    except RuntimeError:
        print(f"URL invalid: {url}")


def extract_data(url):
    source = determine_source(url)
    if source == "thomann":
        return extract_data_store(url, NAME_THOMANN, PRICE_THOMANN, AVAIL_THOMANN)
    if source == "kiwi-electronics":
        return extract_data_store(url, NAME_KIWI, PRICE_KIWI, AVAIL_KIWI)
    else:
        raise RuntimeError(f"Unknown source: {source}")


if __name__ == "__main__":
    pass
