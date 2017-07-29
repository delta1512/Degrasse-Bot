import discord
import asyncio
from random import randint
from urllib.request import urlopen
import warnings

global pre, blacklist, voice, player, playing, lastmessage
pre = ';'
blacklist = []
voice = None
player = None
playing = False
lastmessage = None

client = discord.Client()

@client.event
async def on_ready():
    print('Bot initialised successfully')

@client.event
async def on_message(omessage):
    global pre, blacklist, voice, player, playing, lastmessage

    message = omessage
    msg = message.content
    if message.author.id != 339176112305340416 and msg.startswith(pre):
        await client.delete_message(omessage)
    if not message.author.id in blacklist:
        lastmessage = message
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
                await client.send_message(message.channel, ':arrows_counterclockwise: ' + message.author.mention + ' > You rolled a ' + str(randint(1, limit)))

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
                    await client.send_message(message.channel, ":information_source: " + message.author.mention + " | You must specify a url, eg. `;play https://youtu.be/dQw4w9WgXcQ`.")
            else:
                await client.send_message(message.channel, ":information_source: " + message.author.mention + " | You can't play a song while another song is already playing. To queue songs, go to https://www.woofbark.dog/discordbot/")

        ##############

        if msg.startswith(pre + 'connect'):
            voice = await client.join_voice_channel(client.get_channel('201859187565789185'))
            await client.send_message(message.channel, ":white_check_mark: " + message.author.mention + " | Joined! Type `;loadqueue` to start playing.")

        ##############

        if msg.startswith(pre + "skip"):
            await client.send_message(message.channel, ":next_track: " + message.author.mention + " | Skipped!");
            playing = False
            await loadSong()

        if msg == 'lol gay':
            await client.send_message(message.channel, ':gay_pride_flag:')

        ##############

        if msg.startswith(pre + 'loadqueue'):
            if voice == None:
                await client.send_message(message.channel, ":information_source: " + message.author.mention + " | I'm not connected to a channel yet. Type `;connect` first.");
            else:
                await client.send_message(message.channel, ":arrow_down: " + message.author.mention + " | Loading queue...");
                await loadSong()

async def loadSong():
    global pre, blacklist, voice, player, playing, client
    # player.stop()
    response = urlopen('https://www.woofbark.dog/discordbot/popsong')
    song = str(response.read().decode())
    if song == "nosong":
        playing = False
    else:
        player = await voice.create_ytdl_player("https://www.youtube.com/watch?v=" + song)
        player.start()
        await client.change_status(discord.Game(name=player.title), False)
        await client.send_message(lastmessage.channel, ":arrow_forward: Queue | Now Playing **" + player.title + "**");
        if not playing:
            playing = True
            await songLoop()

async def songLoop():
    global pre, blacklist, voice, player, playing
    while True:
        if playing:
            try:
                if player.is_done():
                    await loadSong()
            except: 
                print('error on song loop!')
        await asyncio.sleep(0.5)

client.run('MzM5MTc2MTEyMzA1MzQwNDE2.DFgJ5A.QHLfQd5KMSvTcHoGoNDjxVUsnOU')