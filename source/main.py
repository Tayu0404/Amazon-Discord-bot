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

    if re.search(r"!amazon list ",message.content):
        keyword = urllib.parse.quote(re.sub(r"!amazon list ","",(message.content).replace("\n"," ")))
        return_message = amazon.list(keyword,message.author.id)
        await client.send_message(message.channel, return_message)

    if re.search(r"!amazon num ",message.content):
        keyword = re.sub(r"!amazon num ","",message.content).replace("\n"," ")
        return_message = amazon.direct_search(keyword,message.author.id)
        await client.send_message(message.channel, return_message)
    
    if re.search(r"!amazon debug ",message.content):
        if re.search(r"list",message.content):
            return_message = amazon.show_list_debug(message.author.id)
            await client.send_message(message.channel,return_message)
        if re.search(r"ping",message.content):
            return_message = "pysm"
            await client.send_message(message.channel,return_message)

    if re.search(r"!amazon help",message.content):
        return_message = (
                "```" + "\n" +
                "search \"Keywords\" : Product Search" + "\n" +
                "list \"Keywords\" : Product search and display list" +"\n" +
                "num \"number\" : Product detail display" + "\n" +
                "```"
                )
        await client.send_message(message.channel,return_message)

client.run(os.environ['discord-token'])
