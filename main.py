import discord
import asyncio
from random import randint
from urllib.request import urlopen

global pre, blacklist, voice
pre = ';'
blacklist = []

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global blacklist
    if not message.author.id in blacklist:
        global pre, voice
        msg = message.content
        if msg.startswith(pre + 'owo'):
            await client.send_message(message.channel, 'OwO what\'s this?')
        if msg.startswith(pre + 'rtd'):
            args = msg.split()
            if len(args) > 1:
                try:
                    limit = int(args[1])
                except:
                    limit = -1
                    await client.send_message(message.channel, 'Error: Invalid number')
            else:
                limit = 6
            if limit > 0:
                await client.send_message(message.channel, 'You rolled a ' + str(randint(1, limit)))
        if msg.startswith(pre + 'prefix'):
            args = msg.split()
            if len(args) > 1:
                if len(argv[1]) <= 5:
                    pre = str(argv[1])
                    await client.send_message(message.channel, 'Prefix changed successfully: `' + pre + '`')
                else:
                    await client.send_message(message.channel, 'Error: prefix is too long')
            else:
                await client.send_message(message.channel, 'Error: No prefix specified')
        if msg.startswith(pre + 'blacklist'):
            args = msg.split()
            if len(args) > 1:
                blacklist.append(args[1])
                await client.send_message(message.channel, 'Client ID blacklisted')
            else:
                await client.send_message(message.channel, 'Error: No ID specified')
        if msg.startswith(pre + 'whitelist'):
            args = msg.split()
            if len(args) > 1:
                try:
                    blacklist.remove(args[1])
                    await client.send_message(message.channel, 'Client ID removed from blacklist')
                except:
                    await client.send_message(message.channel, 'Error: Client ID not in blacklist')
            else:
                await client.send_message(message.channel, 'Error: No ID specified')
        if msg.startswith(pre + 'play'):
            args = msg.split()
            if len(args) > 1:
                try:
                    player = await voice.create_ytdl_player(str(args[1]))
                    player.start()
                except:
                    await client.send_message(message.channel, 'Error: Something went wrong')
            else:
                await client.send_message(message.channel, 'Error: No URL specified')
        if msg.startswith(pre + 'connect'):
            voice = await client.join_voice_channel(client.get_channel('channelID'))
        if msg == 'lol gay':
            await client.send_message(message.channel, ':gay_pride_flag:')
        if msg.startswith(pre + 'loadfromweb'):
            response = urlopen('https://www.woofbark.dog/discordbot/feed')
            q = str(response.read().decode());
            try:
                player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=' + q)
                player.start()
            except:
                await client.send_message(message.channel, 'Error: Something went wrong')

client.run('token')
