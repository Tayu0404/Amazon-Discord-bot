from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import time
import re
import urllib
import schedule

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
        self.user_product = {}
        self.stock_check_list = {}
        
    def list(self,keywords,user_id):
        url = "https://www.amazon.co.jp/s/field-keywords=" + keywords
        html = get_html(url)
        list_temp = html.find("ul",id="s-results-list-atf")
        result_num_list = re.findall(r"id=\"result_[^\"]*\"", str(list_temp))
        num_list = []
        for i in result_num_list:
            num_list.append(int(re.sub(r"\D","",i)))
        num_max = None
        if max(num_list) > 10 :
            num_max = 10
        else :
            num_max = (max(num_list))
        
        return_message_text = (
                urllib.parse.unquote(keywords) + "の検索結果"
                )
        self.user_product[user_id] = {}
        for i in range(num_max):
            count = "result_" + str(i)
            result = list_temp.find("li",id=count)
            product_id = result["data-asin"]
            name = result.find("h2").text
            price = re.sub("\s","",(result.find("span",class_="a-color-price").text)) 
            return_message_text = (
                    return_message_text +
                    "\n" +
                    str(i) + "\n" +
                    name + "\n" +
                    "```" + "\n" +
                    price + "\n" +
                    product_id + "\n" +
                    "```"
                        )
            self.user_product[user_id].setdefault(str(i),product_id)
        print(self.user_product)
        return return_message_text

    def product(self,product_id):
        url = "https://www.amazon.co.jp/dp/product/" + product_id
        html = get_html(url)
        price = re.sub("\s","",(html.find("span",id="priceblock_ourprice").text))
        details = re.sub(r"</?b>|詳細を見る","",(html.find("div",id="ddmDeliveryMessage").text)).strip()
        ships = re.sub(r"\n","",(html.find("div",id="merchant-info").text)).strip()
        name = html.find("span",id="productTitle").text.strip()
        stock = re.sub(r"\n|在庫状況について","",(html.find("div",id="availability").text)).strip()
        img_url = html.find("img",alt=name)["src"]
        return_message_text = (
                name +
                "```" +
                price + "\n" +
                stock + "\n" +
                details + "\n" + 
                ships + "\n" + 
                "```" +
                img_url + "\n" +
                url
                )
        return return_message_text

    def direct_search(self,keywords,user_id):
        url = "https://www.amazon.co.jp/dp/" + self.user_product[user_id][str(keywords)]
        html = get_html(url)
        price = re.sub("\s","",(html.find("span",id="priceblock_ourprice").text))
        details = re.sub(r"</?b>|詳細を見る","",(html.find("div",id="ddmDeliveryMessage").text)).strip()
        ships = re.sub(r"\n","",(html.find("div",id="merchant-info").text)).strip()
        name = html.find("span",id="productTitle").text.strip()
        stock = re.sub(r"\n|在庫状況について","",(html.find("div",id="availability").text)).strip()
        img_url = html.find("img",alt=name)["src"]
        return_message_text = (
                name +
                "```" +
                price + "\n" +
                stock + "\n" +
                details + "\n" + 
                ships + "\n" + 
                "```" +
                img_url + "\n" +
                url
                )
        return return_message_text

    def product_search(self,keywords):
        list_url = "https://www.amazon.co.jp/s/field-keywords=" + keywords
        list_html = get_html(list_url)
        product_id = list_html.find("li",id="result_0")["data-asin"]
        return_message_text = self.product(product_id)
        return return_message_text
    
    def show_list_debug(self,user_id):
        user_list = self.user_product[user_id]
        return_message_text = "User ID : " + user_id
        for i in range(len(user_list)):
            return_message_text = return_message_text + "\n" + str(i) + " : " + user_list[str(i)]
        return return_message_text
