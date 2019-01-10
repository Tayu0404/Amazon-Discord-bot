from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
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

    def product(self,product_id):
        url = "https://www.amazon.co.jp/dp/product/" + product_id
        html = get_html(url)
        price = re.sub("\s","",(html.find("span",id="priceblock_ourprice").text))
        details = re.sub(r"</?b>|詳細を見る","",(html.find("div",id="ddmDeliveryMessage").text)).strip()
        ships = re.sub(r"\n","",(html.find("div",id="merchant-info").text)).strip()
        name = html.find("span",id="productTitle").text.strip()
        stock = re.sub(r"\n|在庫状況について","",(html.find("div",id="availability").text)).strip()
        img_url = html.find("img",alt=name)["src"]
        message_text = (
                name +
                "```" +
                price + "/n" +
                stock + "\n" +
                details + "\n" + 
                ships + "\n" + 
                "```" +
                img_url + "\n" +
                url
                )
        return message_text

    def product_search(self,keywords):
        list_url = "https://www.amazon.co.jp/s/field-keywords=" + keywords
        list_html = get_html(list_url)
        product_id = list_html.find("li",id="result_0")["data-asin"]
        return_message_text = self.product(product_id)
        return return_message_text
