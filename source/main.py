import discord
import os
import amazon_scraping
import re
import urllib.parse
import threading
import schedule
import time
import asyncio

async def stock_send_message(user_id,return_message):
    user_dm = await client.get_user_info(user_id)
    await client.send_message(user_dm,return_message)

class CheckStock(object):
    def __init__(self):
        self.list = {}

    def list_set(self,user_id,key):
        if user_id not in self.list:
            self.list[user_id] = {}
        num = str(len(self.list[user_id]))
        self.list[user_id].setdefault(num,key)

    def search(self,loop):
        for user_id in self.list.keys():
            for num in self.list[user_id].keys():
                key = self.list[user_id][num]
                return_message = amazon.check_search(key)
                asyncio.run_coroutine_threadsafe(stock_send_message(user_id,return_message),loop)
                time.sleep(10)
    def list_check(self):
        print(self.list)

    def check_loop(self):
        print('check start')
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def check_start(self):
        loop = asyncio.get_event_loop()
        self.check_thread = (
                threading.Thread(
                    target=self.check_loop
                    )
                )
        schedule.every(1).minutes.do(self.search,loop)
        self.check_thread.start()


client = discord.Client()
check = CheckStock()
amazon = amazon_scraping.Amazon()

@client.event
async def on_ready():
    print('ログインしました')
    developer_id = await client.get_user_info('257025417490202625')
    await client.send_message(developer_id,'Bot login')
    check.check_start()
@client.event
async def on_message(message):
    if message.content.startswith('!amazon search '):
        keyword = urllib.parse.quote(re.sub(r'!amazon search ','',(message.content).replace('\n',' ')))
        return_message = amazon.product_search(keyword)
        await client.send_message(message.channel, return_message)

    if re.search(r'!amazon list ',message.content):
        keyword = urllib.parse.quote(re.sub(r'!amazon list ','',(message.content).replace('\n',' ')))
        return_message = amazon.list(keyword,message.author.id)
        await client.send_message(message.channel, return_message)

    if re.search(r'!amazon num ',message.content):
        keyword = re.sub(r'!amazon num ','',message.content).replace('\n',' ')
        return_message = amazon.direct_search(keyword,message.author.id)
        await client.send_message(message.channel, return_message)
    
    if re.search(r'!amazon set ',message.content):
        key = re.sub(r'!amazon set ','',(message.content))
        user_id = message.author.id
        check.list_set(user_id,key)
        return_message = 'あとで考える'
        await client.send_message(message.channel,return_message)

    if re.search(r'!amazon debug ',message.content):
        if re.search(r'list',message.content):
            return_message = amazon.show_list_debug(message.author.id)
            await client.send_message(message.channel,return_message)
        if re.search(r'ping',message.content):
            return_message = 'pysm'
            await client.send_message(message.channel,return_message)
        if re.search(r'user_check',message.content):
            check.list_check()

    if re.search(r'!amazon help',message.content):
        return_message = (
                '```' + '\n' +
                'search \'Keywords\' : Product Search' + '\n' +
                'list \'Keywords\' : Product search and display list' +'\n' +
                'num \'number\' : Product detail display' + '\n' +
                '```'
                )
        await client.send_message(message.channel,return_message)

client.run(os.environ['discord-token'])
