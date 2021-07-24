import discord
import os
import json
from simpleplayer import SimplePlayer
from playlist import PlayListPager

TOKEN = open('./secret.txt', 'r').read()
client = discord.Client()
sp = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


class ReactionListener:
    def __init__(self):
        pass

    def handle_on_reaction(self, reaction: discord.Reaction, user: discord.User, ):
        pass

async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    pass

async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
    pass


@client.event
async def on_message(message: discord.Message):
    global sp
    if message.author == client.user:
        return

    if message.content == '1':
        if sp:
            await sp.stop()
        sp = SimplePlayer(message.author.voice.channel)
        await message.add_reaction('👌')

    if message.content == '2':
        await sp.play()
        await message.add_reaction('👌')

    if message.content.startswith('3'):
        for l in message.content.split('\n'):
            _, resource = l.split(' ')
            sp.playlist.add_entry(resource, discriminator=message.author.discriminator)
        await sp.spawn_status_message(message.channel)
        await sp.play()
        await message.add_reaction('👌')

    if message.content == '4':
        await sp.next()
        await message.add_reaction('👌')

    if message.content == '5':
        await sp.prev()
        await message.add_reaction('👌')

    if message.content == '6':
        sp.pause()
        await message.add_reaction('👌')
    
    
        
client.run(TOKEN)


'''
1
3 iq2zfBMwTWc
3 WywvgpTo5Kg
3 ojG9C6L61oA
3 Re6JJ_njYR4
3 q4N7EhUWOAA
3 gqRkPKCrQ_o
3 UNrvNqUqpGM
3 oW7-b8JL8Sk
3 AkRPlTrf3d8
3 BrYSAHihCWU
3 1g31KjRcgHo
3 w0ctlmHx-O8
3 HjI4W8x9Msc
3 NyXApXudtaU
# DELTEL OLD STATUS MESSAGE
'''