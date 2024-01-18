import sys
import requests
import ast
from bs4 import BeautifulSoup

# Methods
def get_price_methods_dynamic(shop,url):
    return getattr(sys.modules[__name__], "get_price_from_%s" % shop)(url)

def get_price_from_dateks(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", {"class": "avail warn"}):
        price = '-'
    else:
        price = soup.find("div", {"class": "price"}).getText().replace('€', '').strip()
    return price.replace('\xa0', '')

# def get_price_from_220(url):
#     html = requests.get(url).content
#     soup = BeautifulSoup(html, 'html.parser')
#     if soup.find("div", {"class": "product-price fl notranslate"}):
#         price = soup.find("div", {"class": "c-price h-price--xx-large h-price--new"}).find('meta')['content'].strip()
#     else:
#         price = '-'
#     return price.replace(",", ".")


def get_price_from_m79(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", {"class": "price"}) and not soup.find("div", {"class": "pages"}):
        price = soup.find("div", {"class": "price"}).find('b').getText().strip()
    else:
        price = '-'
    return price.replace(",", ".")


def get_price_from_1a(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    if soup.find("span", {"class": "product-price-details__price-number"}):
        price = soup.find("span", {"class": "product-price-details__price-number"}).getText().replace('€',
                                                                                                      '').strip().replace(
            ".", "")
    elif soup.find("span", {"class": "price"}):
        price = soup.find("span", {"class": "price"}).find('span').getText().strip().replace(".", "")
    else:
        price = '-'
    return price.replace(",", ".")


def get_price_from_rdveikals(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", {"class": "price price--larger"}):
        price = soup.find("span", {"class": "price price--larger"})['content'].strip()
    else:
        price = '-'
    return price.replace(",", ".")


# def get_price_from_amazon(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0',
#         'From': 'personal@domain.com'
#     }
#     html = requests.get(url, headers=headers)
#     soup = BeautifulSoup(html.content, "html.parser")

#     if soup.find("div", {"id": "rightCol"}).find("span", {"class": "a-price"}):
#         base_price = soup.find("div", {"id": "apex_desktop"}).find("span", {"class": "a-price"}).find("span", {
#             "class": "a-price-whole"}).getText().replace(',', '').replace('.', '').strip()
#         decimal_price = soup.find("div", {"id": "apex_desktop"}).find("span", {"class": "a-price"}).find("span", {
#             "class": "a-price-fraction"}).getText().replace(',', '').strip()
#         price = f"{base_price},{decimal_price}"
#         print(price)

#         if soup.find("div", {"id": "mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"}):
#             return str(format(float(price.replace(",", ".")) + float(
#                 soup.find("div", {"id": "mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"})
#                     .find('span')['data-csa-c-delivery-price']
#                     .replace('€', '')
#                     .replace(",", ".")
#                     .strip()), '.2f')).replace(".", ",")
#     else:
#         price = '-'

#     return price.replace(".", ",")


# def get_price_from_capital(url):
#     html = requests.get(url).content
#     soup = BeautifulSoup(html, 'html.parser')
#     prices = [i['data-product_data'] for i in soup.find_all('div', {"class": "row search_row"})]

#     final_prices = []
#     for price in prices:
#         final_prices.append(ast.literal_eval(price).get('price').strip())

#     return min(final_prices).replace(".", ",")


def get_price_from_tet(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("span", {"class": "i-product-data__price-inner"}):
        price = soup.find("span", {"class": "i-product-data__price-inner"}).getText().strip()
    else:
        price = '-'
    return price.replace(",", ".")


def get_price_from_balticdata(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", {"class": "EBI4ProductDetailsPriceSale"}):
        price = soup.find("div", {"class": "EBI4ProductDetailsPriceSale"}).getText().replace('€', '').strip()
    else:
        price = '-'
    return price.replace(",", ".")


def get_price_from_elkor(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find("div", {"class": "product-price"}).find("span", {"class": "current-price"}).getText().replace('€','').strip()
    return price.replace(".", ",")


# def get_price_from_aio(url):
#     html = requests.get(url).content
#     soup = BeautifulSoup(html, 'html.parser')
#     if soup.find("div", {"class": "item-page"}).find("div", {"class": "info"}).find("div", {"class": "price"}):
#         price = soup.find("div", {"class": "item-page"}).find("div", {"class": "info"}).find("div", {"class": "price"}).getText().replace('€', '').replace(',', '').strip()
#     else:
#         price = '-'
#     return price.replace(".", ",")