import re

RX_THOMANN_PRICE = '<span class="primary">(.*?)</span>'
RX_THOMANN_NAME = '<h1 itemprop="name">(.*?)</h1>'

def rx_find(pattern, content):
    found = re.search(pattern, content)
    if not found:
        raise RuntimeError(f"Not found")
    return found.group(1)

def extract_data(content, source):
    if source == "thomann":
        return extract_data_thomann(content)
    else:
        raise RuntimeError(f"Unknown source: {source}")


# functions for specific stores
def extract_data_thomann(content):
    name = rx_find(RX_THOMANN_NAME, content)
    curr, price = rx_find(RX_THOMANN_PRICE, content).split(" ")
    price = int(price.replace(".", ""))
    return name, price, curr




if __name__ == "__main__":
    pass