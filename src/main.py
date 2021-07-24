import discord
import os
import json
from simpleplayer import SimplePlayer
from playlist import PlayListPagger

TOKEN = open('./secret.txt', 'r').read()
client = discord.Client()
sp = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message: discord.Message):
    global sp
    if message.author == client.user:
        return

    if message.content == '1':
        if sp:
            await sp.stop()
        sp = SimplePlayer(message.author.voice.channel)

    if message.content == '2':
        await sp.play()

    if message.content.startswith('3'):
        for l in message.content.split('\n'):
            _, resource = l.split(' ')
            sp.playlist.add_entry(resource)
        await sp.play()

    if message.content == '4':
        await sp.next()

    if message.content == '5':
        await sp.prev()

    if message.content == '6':
        await sp.pause()

    if message.content == '7':
        s = PlayListPagger.get_pagged_list(sp.playlist)
        msg = await message.channel.send(embed=s)
    
        
client.run(TOKEN)

## DELTEL OLD STATUS MESSAGE