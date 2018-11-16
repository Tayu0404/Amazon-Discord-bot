import discord
import os
client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました')

#@client.event
#async def on_message(message):

client.run(os.environ['discord-token'])
