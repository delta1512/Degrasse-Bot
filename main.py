import discord
import asyncio
import helpers
from random import randint
from urllib.request import urlopen
from os import popen

client = discord.Client()
pre = ';'
blacklist = []
voice = None
allow_nick_changing = True
last_message_source = None
out_channels = {'201859187565789184' : '307345792296026112',
				'332660239104999424' : '356233195986878495'}
original_nick = None
sid = ''
upemoji = ''
downemoji = ''
blacklist = helpers.updateBlacklist()

@client.event
async def on_ready():
	global out_channels, original_nick, upemoji, downemoji

	upemoji, downemoji = helpers.findVoteEmojis(client)
	print('[DEBUG] Bot initialized successfully')
	for server in client.servers:
		#hashed out for future deliberation on method
		#out_channels[server.id] = server.default_channel.id
		print('[DEBUG] Is in server ' + server.id)


@client.event
async def on_message(message):
	global last_message_source, upemoji, downemoji, blacklist

	if message.content.startswith(pre) and (not ';-;' in message.content) and (not message.content.startswith(pre + 'destroy')):
		await client.delete_message(message)
	if not message.author.id in blacklist:

		#Voting reaction handler
		if (len(message.attachments) > 0 or len(message.embeds) > 0) and (not message.content.startswith(pre)):
			await client.add_reaction(message, upemoji)
			await client.add_reaction(message, downemoji)

		#Start command declaration
		cmd = message.content

		if cmd.startswith(pre):
			last_message_source = message.channel

		#Misc / Fun commands
		if cmd.startswith(pre + 'owo'):
			await discord_send(message.channel, 'OwO what\'s this?')

		elif cmd.startswith(pre + 'rtd'):
			await roll_the_dice(message)

		elif cmd.startswith(pre + 'time'):
			await discord_send(message.channel,  ':clock3: ' + message.author.mention + ' | Time [Unix | Nano]: ' + popen('date \'+%s %N\'').read())

		elif cmd.startswith('what time is it'):
			await discord_send(message.channel, "ARE YOU WIMBLY WOMBLY MATE!? ITS ALMOST SAX APPLE DIN DIN SPROINGO TOINGO SIXY CHAP")

		elif cmd.startswith(pre + 'asciify'):
			await helpers.asciify(client, message)

		elif cmd.startswith(pre + 'destroy'):
			if len(message.attachments) > 0:
				exit_code = helpers.destroy_image(message.content.split()[1:], message.attachments)
				if exit_code == 0:
					await client.send_file(message.channel, '/tmp/0.png')
				else:
					await discord_send(message.channel, ':thinking: | Something went wrong:\n`Input: ' + message.content + '`')
			else:
				await discord_send(message.channel, ':grey_question: | No images were supplied')

		#Administration commands
		elif cmd.startswith(pre + 'prefix'):
			await set_prefix(message)

		elif cmd.startswith(pre + 'blacklist'):
			users = message.mentions
			for user in users:
				blacklist = helpers.blacklist(user.id, user.name);

		elif cmd.startswith(pre + 'pardon'):
			users = message.mentions
			for user in users:
				blacklist = helpers.pardon(user.id, user.name);

		#Music commands
		elif cmd.startswith(pre + 'play'):
			await song_play(message)

		elif cmd.startswith(pre + 'connect'):
			await voice_connect(message)

		elif cmd.startswith(pre + 'disconnect') or cmd.startswith(pre + 'dc'):
			await voice_disconnect(message)

		elif cmd.startswith(pre + 'skip'):
			await song_skip(message)

#Command definitions
async def roll_the_dice(message):
	args = message.content.split()
	if len(args) > 1:
		try:
			limit = int(args[1])
		except:
			limit = -1
			await discord_send(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Invalid number')
	else:
		limit = 6
	if limit > 0:
		await discord_send(message.channel, ':game_die: ' + message.author.mention + ' | You rolled a ' + str(randint(1, limit)))
	else:
		await discord_send(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Invalid number')

async def set_prefix(message):
	mlength = 3
	args = message.content.split()
	if len(args) == 2:
		if len(args[1]) <= mlength:
			global pre;
			pre = str(args[1])
			await discord_send(message.channel, ':asterisk: ' + message.author.mention + ' | Prefix changed to: `' + pre + '`')
		else:
			await discord_send(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Prefix is too long. Maximum length: ' + string(mlength))
	else:
		await discord_send(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Correct usage: `prefix [newprefix]`')

async def song_play(message):
	await discord_send(message.channel, ':negative_squared_cross_mark: ' + message.author.mention + ' | Add songs here > http://queue-bot.tk/')

async def song_skip(message):
	global player, out_channels

	player.stop()
	await discord_send(client.get_channel(out_channels[message.server.id]), ':white_check_mark: ' + message.author.mention + ' | Skipped the current song!')

async def voice_connect(message):
	global voice, player, out_channels, sid

	sid = message.server.id;

	if voice != None:
		await discord_send(client.get_channel(out_channels[message.server.id]), ":information_source: " + message.author.mention + " | I'm already playing from the queue. Type `;skip` to skip the current song.")
	else:
		for vchannel in message.author.server.channels:
			found_user = False
			if vchannel.type == discord.ChannelType.voice:
				print("[DEBUG] Joined Channel: " + vchannel.name)
				for member in vchannel.voice_members:
					print("[DEBUG] Connected Users: " + member.name)
					if member.id == message.author.id:
						voice = await client.join_voice_channel(client.get_channel(vchannel.id))
						await discord_send(client.get_channel(out_channels[message.server.id]), ":white_check_mark: " + message.author.mention + " | Joined your voice channel!")
						found_user = True
						break
			if found_user: break
		await discord_send(client.get_channel(out_channels[message.server.id]), ":arrow_down: " + message.author.mention + " | Loading queue...");
		await songLoop()

async def voice_disconnect(message):
	global voice, player, out_channels

	await voice.disconnect()
	voice = None
	player.stop()
	await discord_send(client.get_channel(out_channels[message.server.id]), ":white_check_mark: " + message.author.mention + " | Disconnected.")

#Intrinsic Functions
async def songLoop():
	global player, voice, out_channels, sid
	while voice != None:
		try:
			response = urlopen('https://www.woofbark.dog/queuebot/data/queue_pull?id=' + sid).read().decode().split(",")
			url = str(response[0])
			if url != "nosong":
				left = str(response[1])
				player = await voice.create_ytdl_player(url)
				player.start()
				await client.change_presence(game=discord.Game(name=left + " Songs Queued"))
				await discord_send(client.get_channel(out_channels[message.server.id]), ":arrow_forward: Queue | Now Playing **" + player.title + "**");
				while not player.is_done():
					await asyncio.sleep(0.3)
			else:
				await asyncio.sleep(1)
		except Exception as e:
			print("[ERROR]\n", e)
			await asyncio.sleep(1)

async def nick_default():
	global allow_nick_changing, original_nick
	allow_nick_changing = False
	await client.change_nickname(original_nick, None)

async def discord_send(channel, string):
	# await nick_default()
	await client.send_message(channel, string)

client.run('MzM5MTc2MTEyMzA1MzQwNDE2.DF1qVA.UqW9GwapGBzyAIIw-UOb4dbKY-w')
