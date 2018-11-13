from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

uri = 'https://www.amazon.co.jp/gp/product/'
product = 'B01HEDBILK'
page=1
setTime = 20
url = uri + product + '/'
print (url)

def requestHTML(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="./python/chromedriver",chrome_options=options)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    amazonResult = BeautifulSoup(html,'html.parser')
    return amazonResult

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
        ships = re.sub(r'この出品商品には代金引換とコンビニ・ATM・ネットバンキング・電子マネー払いが利用できます。|ギフトラッピングを利用できます。',"",(result.find('div',id="merchant-info").text)).strip()
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

def html_write(amazonResult):
    path = '/python/data/log.html'
    s = str(amazonResult)
    with open(path, mode='w') as f:
        f.write(s)
    with open(path) as f:
        result= f.read()
    return result

html = requestHTML(url)
