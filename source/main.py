import asyncio
import os
import re
import time
import threading

import discord
import schedule
import urllib.parse

import amazon_scraping

async def dm_send_message(user_id,return_message):
    user_dm = await client.get_user_info(user_id)
    await client.send_message(user_dm,return_message)

class CheckStock(object):
    def __init__(self):
        self.list = {}
        self.del_list = {}

    def list_set(self,user_id,key):
        if user_id not in self.list:
            self.list[user_id] = {}
        self.list[user_id].setdefault(key,key)
    
    def list_del(self):
        for user_id in self.del_list:
            for key in self.del_list[user_id]:
                del self.list[user_id][key]
            if len(self.list[user_id]) == 0:
                del self.list[user_id]
        self.del_list = {}

    def search(self,loop):
        for user_id in self.list.keys():
            self.del_list[user_id] = []
            for key in self.list[user_id].keys():
                search_word = self.list[user_id][key]
                return_message = amazon.check_search(search_word)
                if return_message != None:
                    asyncio.run_coroutine_threadsafe(
                            dm_send_message(user_id,return_message),
                            loop
                            )
                    self.del_list[user_id].append(key)
                time.sleep(50)
        self.list_del()

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
        print(return_message)
        await client.send_message(message.channel, return_message)

    if re.search(r'!amazon list ',message.content):
        keyword = urllib.parse.quote(re.sub(r'!amazon list ','',(message.content).replace('\n',' ')))
        return_message = amazon.list(keyword,message.author.id)
        print(return_message)
        await client.send_message(message.channel, return_message)

    if re.search(r'!amazon num ',message.content):
        keyword = re.sub(r'!amazon num ','',message.content).replace('\n',' ')
        return_message = amazon.direct_search(keyword,message.author.id)
        await client.send_message(message.channel, return_message)
    
    if re.search(r'!amazon set ',message.content):
        key = re.sub(r'!amazon set ','',(message.content))
        user_id = message.author.id
        check.list_set(user_id,key)
        return_message = 'I registered in the Stock check.\nI will inform you DM when it Stock'
        await client.send_message(message.channel,return_message)

    if re.search(r'!amazon debug ',message.content):
        if re.search(r'list',message.content):
            return_message = amazon.show_list_debug(message.author.id)
            await client.send_message(message.channel,return_message)
        if re.search(r'ping',message.content):
            return_message = 'pong'
            await client.send_message(message.channel,return_message)
        if re.search(r'user_check',message.content):
            check.list_check()
        if re.search(r'test',message.content):
            key = re.sub(r'!amazon debug test ','',(message.content))
            amazon.test_search(key)

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
