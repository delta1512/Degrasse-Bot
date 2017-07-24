import discord
import asyncio
from random import randint
from urllib.request import urlopen

global pre, blacklist, voice, player, playing
pre = ';'
blacklist = []
player = None
playing = False

client = discord.Client()

@client.event
async def on_ready():
    print('Bot initialised successfully')

@client.event
async def on_message(message):
    global blacklist
    if not message.author.id in blacklist:
        global pre, voice, player, playing
        msg = message.content
        if msg.startswith(pre + 'owo'):
            await client.send_message(message.channel, 'OwO what\'s this?')

        ##############

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

        ##############

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

        ##############

        if msg.startswith(pre + 'blacklist'):
            args = msg.split()
            if len(args) > 1:
                blacklist.append(args[1])
                await client.send_message(message.channel, 'Client ID blacklisted')
            else:
                await client.send_message(message.channel, 'Error: No ID specified')

        ##############

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

        ##############

        if msg.startswith(pre + 'play'):
            if not playing or player.is_done():
                args = msg.split()
                if len(args) > 1:
                    try:
                        player = await voice.create_ytdl_player(str(args[1]))
                        player.start()
                        playing = True
                    except:
                        await client.send_message(message.channel, 'Error: Something went wrong')
                else:
                    await client.send_message(message.channel, 'Error: No URL specified')

        ##############

        if msg.startswith(pre + 'connect'):
            voice = await client.join_voice_channel(client.get_channel('voiceChannelID'))

        ##############

        if msg == 'lol gay':
            await client.send_message(message.channel, ':gay_pride_flag:')

        ##############

        if msg.startswith(pre + 'loadfromweb'):
            playing = True
            await loadSong()

async def loadSong():
    global voice, player
    response = urlopen('https://www.woofbark.dog/discordbot/popsong')
    song = str(response.read().decode())
    if song == "nosong":
        playing = False
    else:
        player = await voice.create_ytdl_player("https://www.youtube.com/watch?v=" + song)
        player.start()
        if not playing:
            playing = True
            songLoop()

async def songLoop():
    global player, playing
    while True:
        print('checkloop')
        if playing:
            try:
                if player.is_done():
                    await loadSong()
            except: 
                print("error on is live or something")
        await asyncio.sleep(3)

client.run('token')