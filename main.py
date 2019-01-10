import discord
import os
import amazon_scraping
import re
import urllib.parse
import threading
client = discord.Client()
amazon = amazon_scraping.Amazon()
@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.content.startswith("!amazon search "):
        keyword = urllib.parse.quote(re.sub(r"!amazon search ","",(message.content).replace("\n"," ")))
        return_message = amazon.product_search(keyword)
        await client.send_message(message.channel, return_message)
        """
        if re.search(r"!amazon list ",message.content):
            keyword = urllib.parse.quote(re.sub(r"!amazon list ","",(message.content).replace("\n"," ")))
        if re.search(r"!amazon product ",message.content):
            keyword = re.sub(r"!amazon product ","",(message.content))
            keyword = urllib.parse.quote(re.sub(r"!amazon search ","",(message.content).replace("\n"," ")))


        if re.search(r"!amazon help",message.content):
            return_message = "Help\n```!amazon search keywords : 商品検索\n!amazon Number : 詳細検索```"
            await client.send_message(message.channel, return_message)
    if message.content.startswith("!amazon Bot Stop"):
        client.logout()
        """
client.run(os.environ['discord-token'])
