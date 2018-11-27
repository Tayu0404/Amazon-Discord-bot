from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

def get_html(url):
    print (url)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path="./python/chromedriver",chrome_options=options)
    driver.get(url)
    html = driver.page_source.encode("utf-8")
    result = BeautifulSoup(html,"html.parser")
    return result

class Amazon(object):
    def __init__(self):
        self.amazon_list = []
    
    def search_list (self,keywords):
        self.amazon_list = []
        url = "https://www.amazon.co.jp/s/field-keywords=" + keywords
        html = get_html(url)
        max_count = max([
            int(intStrings)
                for finded in re.findall(r"result_[0-1]?[0-9]", str(html))
                    for intStrings in re.findall(r"\d+", finded)
        ]) + 1
        for i in range(max_count):
            count = "result_" + str(i)
            search = html.find("li",id=count)
            product_id = search["data-asin"]
            name = search.find("h2").text
            price = re.sub("\s","",(search.find("span",class_="a-color-price").text))
            self.amazon_list.append([product_id,name,price])
        return self.amazon_list

    def search_product (self,product_id):
        url = "https://www.amazon.co.jp/dp/product/" + product_id
        html = get_html(url)
        price = re.sub("\s","",(html.find("span",id="priceblock_ourprice").text))
        details = re.sub(r"</?b>|詳細を見る","",(html.find("div",id="deliveryPromiseInsideBuyBox_feature_div").text)).strip()
        ships = re.sub(
            r"この出品商品には代金引換とコンビニ・ATM・ネットバンキング・電子マネー払いが利用できます。| ギフトラッピングを利用できます。",
            "",
            (html.find("div",id="merchant-info").text)
            ).strip()
        name = (html.find("span",id="productTitle").text).strip()
        stock = re.sub(r"\n|在庫状況について","",(html.find("div",id="availability").text)).strip()
        img_url = html.find("img",alt=name)["src"]
        product_details = []
        product_details.extend([name, price,stock,details,ships,img_url,url])
        return product_details
    def search_details (self, choice):
        product_id = self.amazon_list[choice][0]
        product_list = searchi_product(product_id)
        return product_list
