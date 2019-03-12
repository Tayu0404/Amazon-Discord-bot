import re
import threading
import urllib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_html(url):
    print (url)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path='./python/chromedriver',chrome_options=options)
    driver.get(url)
    html = driver.page_source.encode('utf-8')
    result = BeautifulSoup(html,'html.parser')
    driver.quit()
    return result

class Amazon(object):
    def __init__(self):
        self.user_product = {}
        
    def list(self,keywords,user_id):
        try:
            url = 'https://www.amazon.co.jp/s/field-keywords=' + keywords
            html = get_html(url)
            list_temp = html.find('ul',id='s-results-list-atf')
            result_num_list = re.findall(r'id="result_[^"]*"', str(list_temp))
            num_list = []
            for i in result_num_list:
                num_list.append(int(re.sub(r'\D','',i)))
            num_max = None
            if max(num_list) > 10 :
                num_max = 10
            else :
                num_max = (max(num_list))
            
            return_message_text = (
                    urllib.parse.unquote(keywords) + 'の検索結果'
                    )
            self.user_product[user_id] = {}
            for i in range(num_max):
                count = 'result_' + str(i)
                result = list_temp.find('li',id=count)
                product_id = result['data-asin']
                name = result.find('h2').text
                price = re.sub('\s','',(result.find('span',class_='a-color-price').text)) 
                return_message_text = (
                        return_message_text +
                        '\n' +
                        str(i) + '\n' +
                        name + '\n' +
                        '```' + '\n' +
                        price + '\n' +
                        product_id + '\n' +
                        '```'
                            )
                self.user_product[user_id].setdefault(str(i),product_id)
            return return_message_text
        except:
            return_message_text = 'あとで考える'
            return return_message_text
    def product(self,product_id):
        try:
            url = 'https://www.amazon.co.jp/dp/product/' + product_id
            html = get_html(url)
            stock = re.sub(r'\n|在庫状況について','',(html.find('div',id='availability').text)).strip()
            price = re.sub('\s','',(html.find('span',id='priceblock_ourprice').text))
            details = re.sub(r'</?b>|詳細を見る','',(html.find('div',id='ddmDeliveryMessage').text)).strip()
            ships = re.sub(r'\n','',(html.find('div',id='merchant-info').text)).strip()
            name = html.find('span',id='productTitle').text.strip()
            img_url = html.find('img',alt=name)['src']
            return_message_text = (
                    name +
                    '```' +
                    price + '\n' +
                    stock + '\n' +
                    details + '\n' + 
                    ships + '\n' + 
                    '```' +
                    img_url + '\n' +
                    url
                    )
            return return_message_text
        except:
            return_message_text = (
            'I could not find the item\n' \
            'The following can be considered\n' \
            '```\n' \
            '・There is no inventory of goods\n' \
            '・There is no seller\n' \
            '・Search words is wrong\n' \
            '```'
            )
            return return_message_text
    def direct_search(self,keywords,user_id):
        url = 'https://www.amazon.co.jp/dp/' + self.user_product[user_id][str(keywords)]
        html = get_html(url)
        price = re.sub('\s','',(html.find('span',id='priceblock_ourprice').text))
        details = re.sub(r'</?b>|詳細を見る','',(html.find('div',id='ddmDeliveryMessage').text)).strip()
        ships = re.sub(r'\n','',(html.find('div',id='merchant-info').text)).strip()
        name = html.find('span',id='productTitle').text.strip()
        stock = re.sub(r'\n|在庫状況について','',(html.find('div',id='availability').text)).strip()
        img_url = html.find('img',alt=name)['src']
        return_message_text = (
                name +
                '```' +

                details + '\n' + 
                ships + '\n' + 
                '```' +
                img_url + '\n' +
                url
                )
        return return_message_text

    def product_search(self,keyword):
        try:
            url = 'https://www.amazon.co.jp/s/field-keywords=' + keyword
            html = get_html(url)
            product_id = html.find('li',id='result_0')['data-asin']
            return_message = self.product(product_id)
            return return_message
        except:
            return_message_text = (
            'I could not find the item\n' \
            'The following can be considered\n' \
            '```\n' \
            '・There is no inventory of goods\n' \
            '・There is no seller\n' \
            '・Search words is wrong\n' \
            '```'
            )
            return return_message_text

    def check_search(self,key):
        url = 'https://www.amazon.co.jp/dp/product/' + key
        html= get_html(url)
        stock = re.sub(r'\n|在庫状況について','',(html.find('div',id='availability').text)).strip()
        if re.search(r'在庫あり|残り',stock):
            price = re.sub('\s','',(html.find('span',id='priceblock_ourprice').text))
            details = re.sub(r'</?b>|詳細を見る','',(html.find('div',id='ddmDeliveryMessage').text)).strip()
            ships = re.sub(r'\n','',(html.find('div',id='merchant-info').text)).strip()
            name = html.find('span',id='productTitle').text.strip()
            img_url = html.find('img',alt=name)['src']
            return_message_text = (
                    name +
                    '```' +
                    price + '\n' +
                    stock + '\n' +
                    details + '\n' + 
                    ships + '\n' + 
                    '```' +
                    img_url + '\n' +
                    url
                    )
            return return_message_text
