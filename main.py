import discord
import asyncio
from random import randint
from urllib.request import urlopen
import warnings

pre = ';'
blacklist = []
voice = None
audio_player = None
playing = False
last_message_source = None

client = discord.Client()

@client.event
async def on_ready():
	print('Bot initialized successfully.');

@client.event
async def on_message(message):
	global last_message_source

	if message.author.id != 339176112305340416 and message.content.startswith(pre):
		await client.delete_message(message)
	if not message.author.id in blacklist:

		#Start command declaration
		cmd = message.content

		if cmd.startswith(pre):
			last_message_source = message.channel

		#Misc / Fun commands
		if cmd.startswith(pre + 'owo'):
			await owo_check(message)

		elif cmd.startswith(pre + 'rtd'):
			await roll_the_dice(message)

		#Administration commands
		elif cmd.startswith(pre + 'prefix'):
			await set_prefix(message)

		# elif cmd.startswith(pre + 'blacklist'):
		# 	await blacklist_user(message)

		# elif cmd.startswith(pre + 'whitelist'):
		# 	await whitelist_user(message)

		#Music commands
		elif cmd.startswith(pre + 'play'):
			await song_play(message)

		elif cmd.startswith(pre + 'connect'):
			await voice_connect(message)

		elif cmd.startswith(pre + 'disconnect'):
			await voice_disconnect(message)

		elif cmd.startswith(pre + 'loadqueue'):
			await song_load_queue(message)

		# else if cmd.startswith(pre + 'skip'):
		# 	song_skip(message)

		# else if cmd.startswith(pre + 'dc'):
		# 	voice_disconnect(message)

#Command definitions

async def owo_check(message):
	await client.send_message(message.channel, 'OwO what\'s this?')

async def roll_the_dice(message):
	args = message.content.split()
	if len(args) > 1:
		try:
			limit = int(args[1])
		except:
			limit = -1
			await client.send_message(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Invalid number')
	else:
		limit = 6
	if limit > 0:
		await client.send_message(message.channel, ':game_die: ' + message.author.mention + ' | You rolled a ' + str(randint(1, limit)))
	else:
		await client.send_message(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Invalid number')

async def set_prefix(message):
	mlength = 3
	args = message.content.split()
	if len(args) == 2:
		if len(args[1]) <= mlength:
			global pre;
			pre = str(args[1])
			await client.send_message(message.channel, ':asterisk: ' + message.author.mention + ' | Prefix changed to: `' + pre + '`')
		else:
			await client.send_message(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Prefix is too long. Maximum length: ' + string(mlength))
	else:
		await client.send_message(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Correct usage: `prefix [newprefix]`')

async def song_play(message):
	await client.send_message(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Go here to add your song to the queue: https://woofbark.dog/discordbot')

async def voice_connect(message):
	global voice

	for vchannel in message.author.server.channels:
		found_user = False
		if vchannel.type == discord.ChannelType.voice:
			print("> " + vchannel.name)
			for member in vchannel.voice_members:
				print(member.name)
				if member.id == message.author.id:
					voice = await client.join_voice_channel(client.get_channel(vchannel.id))
					await client.send_message(message.channel, ":white_check_mark: " + message.author.mention + " | Joined your voice channel!")
					break
		if found_user: break

async def voice_disconnect(message):
	global voice, playing

	playing = False
	await voice.disconnect()
	voice = None
	await client.send_message(message.channel, ":white_check_mark: " + message.author.mention + " | Disconnected.")

async def song_load_queue(message):
	global voice, playing
	if voice == None:
		await client.send_message(message.channel, ":information_source: " + message.author.mention + " | I'm not connected to a channel yet. Type `;connect` first.");
	elif playing:
		await client.send_message(message.channel, ":information_source: " + message.author.mention + " | I'm already playing from the queue. Type `;skip` to skip the current song.")
	else:
		if not playing:
			await client.send_message(message.channel, ":arrow_down: " + message.author.mention + " | Loading queue...");
			await songLoop()

#Functions

async def songLoop():
	global player, voice, last_message_source, playing
	playing = True
	while (playing):
		response = urlopen('https://www.woofbark.dog/discordbot/popsong')
		url = str(response.read().decode())
		if url != "nosong":
			player = await voice.create_ytdl_player("https://www.youtube.com/watch?v=" + url)
			player.start()
			await client.change_status(discord.Game(name=player.title), False)
			await client.send_message(last_message_source, ":arrow_forward: Queue | Now Playing **" + player.title + "**");
			await waitTillDone()
		else:
			await asyncio.sleep(1)

async def waitTillDone():
	global player
	while not player.is_done():
		await asyncio.sleep(0.5)
	return True

client.run('MzM5MTc2MTEyMzA1MzQwNDE2.DF1qVA.UqW9GwapGBzyAIIw-UOb4dbKY-w')