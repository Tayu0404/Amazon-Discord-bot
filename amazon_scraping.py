from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

def get_html(url):
    print (url)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="./python/chromedriver",chrome_options=options)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    result = BeautifulSoup(html,'html.parser')
    return result

def search (keywords):
    url = "https://www.amazon.co.jp/s/field-keywords=" + keywords
    return url

def product (product_id):
    url = "https://www.amazon.co.jp/dp/product/" + product_id
    return url

def price(result):
    try:
        price = re.sub('\s',"",(result.find('span',id="priceblock_ourprice").text))
        print("値段:")
        print(price)
        return price
    except AttributeError:
        print("price error")

def details(result):
    try:
        details = re.sub(r'</?b>|詳細を見る',"",(result.find('div',id="deliveryPromiseInsideBuyBox_feature_div").text)).strip()
        print("詳細:")
        print(details)
        return details
    except AttributeError:
        print("details error")

def ships(result):
    try:
        ships = re.sub(
            r'この出品商品には代金引換とコンビニ・ATM・ネットバンキング・電子マネー払いが利用できます。| ギフトラッピングを利用できます。',
            "",
            (result.find('div',id="merchant-info").text)
            ).strip()
        print("販売元:")
        print(ships)
        return ships
    except AttributeError:
        print("ships error")

def name(result):
    try:
        name = (result.find('span',id="productTitle").text).strip()
        print("商品名:")
        print(name)
        return name
    except AttributeError:
        print("name error")

def stock(result):
    try:
        stock = re.sub(r'\n|在庫状況について',"",(result.find('div',id="availability").text)).strip()
        print("在庫状況:")
        print(stock)
        return stock
    except AttributeError:
        print("stock error")

def url_img_src(result,name):
    try:
        img_src = result.find('img',alt=name)
        img_url = img_src['src']

        print("画像URL:")
        print(img_url)
    except AttributeError:
        print("img url error")


def search_list (result):
    int_count =20
    product_list = []
    for i in range(int_count):
        count = "result_" + str(i)
        search = result.find('li',id=count)
        product_id = search['data-asin']
        name = search.find('h2').text
        price = re.sub('\s',"",(search.find('span',class_="a-color-price").text))
        product_list.append([product_id,name,price])
    return product_list

html = get_html(search("Intel"))

search_list(html)
