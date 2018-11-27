import discord
import os
import amazon_scraping
import re
import urllib.parse
client = discord.Client()
amazon = amazon_scraping.Amazon()
@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.content.startswith("!amazon"):
        if re.search(r"!amazon search ",message.content):
            keyword = urllib.parse.quote(re.sub(r"!amazon search ","",(message.content).replace("\n"," ")))
            amazon_list = amazon.search_list(keyword)
            return_message = ""
            print(amazon_list)
            for i in range(len(amazon_list)):
                return_message = return_message + str(i) + "```" +  amazon_list[i][1] + "\n" + amazon_list[i][2] + "``` \n"
                if i == len(amazon_list)/2:
                    await client.send_message(message.channel, urllib.parse.unquote(keyword) + "の検索結果\n" + "!amazon 0~" + str(len(amazon_list)) + "で詳細検索可能 \n" + return_message)
                    return_message = ""
                elif i == len(amazon_list)-1:
                    await client.send_message(message.channel, return_message)
        if re.search(r"!amazon product ",message.content):
            keyword = re.sub(r"!amazon product ","",(message.content))
            product_list = amazon.search_product(keyword)
            return_message = product_list[0] + "```"
            for i in range(1,len(product_list)):
                if i == len(product_list) -1:
                    return_message = return_message + "``` \n" + product_list[i]
                else :
                    return_message = return_message  + product_list[i] + "\n"
            await client.send_message(message.channel, return_message)
        
        if re.search(r"!amazon \d+",message.content):
            choice = int(re.sub(r"!amazon ","",message.content))
            product_id = amazon.amazon_list[choice][0]
            product_list = amazon.search_product(product_id)
            return_message = product_list[0] + "```"
            for i in range(1,len(product_list)-1):
                if i == len(product_list) -2:
                    return_message = return_message + "``` \n" + product_list[i]
                else :
                    return_message = return_message  + product_list[i] + "\n"
            await client.send_message(message.channel, return_message + "\n" + product_list[6])
        if re.search(r"!amazon help",message.content):
            return_message = "Help\n```!amazon search keywords : 商品検索\n!amazon Number : 詳細検索```"
            await client.send_message(message.channel, return_message)
    if message.content.startswith("!amazon Bot Stop"):
        client.logout()
client.run(os.environ['discord-token'])
