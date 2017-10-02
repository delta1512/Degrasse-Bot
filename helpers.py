import discord
import asyncio
from urllib.request import urlopen
from ImageDestroyer import Destroyer

man_man = ''':information_source: | Did not specify any bot function.
```Options
queue
imdestroy
other```'''

man_queue = '''```Queuebot music queueing service:
The music functionality of the bot does not handle links sent within any
textual chat, however handling the entire queue service on a seperate entity
as a web service.

To access the service visit: https://www.woofbark.dog/queuebot/?id=[SERVER_ID]
where SERVER_ID is the ID of the server the bot is operating its music service
on.

The server ID can be accessed by enabling developer mode in your discord settings
and right-clicking on the server name/dropdown in the top left corner and
selecting "Copy ID"

Commands:
	connect 	- Tells the bot to join the voice channel you are currently in.
				Note that this command will only work if you are currently in a
				voice chat.
	disconnect  - Tells the bot to leave any connected voice chats within the
				server. This command can be shortened to "dc".```'''

man_imdestroy = '''```Image Destroyer application:
Image Destroyer is a functionality of the bot added that allows for the
destruction of images based on implemented image processing algorithms.

Usage:
The bot should be given an image as either an attachment to a message or a URL
placed directly after the calling command. In time, it will then provide a
processed image as a result of the called arguments.

Command:
	destroy [URL] {ARGS}
	- Calls the image destroyer program with the attached image or URL provided
	by the "[URL]" argument, performing the operations signified by "{ARGS}".

Arguments {ARGS}:
	grey
	jumble
	incbright
	randbright
	displace [threshold]	- "threshold" usually denotes a chance of some sort
	scratch [threshold] [max propagation length]
	worms [amount] [min propagation] [threshold]
	compress [threshold]```'''

def updateBlacklist():
	blacklist = []
	f = open("blacklist.dat", 'a+')
	f.close()
	f = open("blacklist.dat", 'r')
	for line in f:
	    blacklist.append(line.rstrip().split("#")[0])
	f.close()
	return blacklist;

def blacklist(uid, uname):
	f = open("blacklist.dat", 'a+')
	f.write(uid + "#" + uname + "\r\n")
	f.close()
	return updateBlacklist()

def pardon(uid, uname):
	blacklist = []
	f = open("blacklist.dat", 'a+')
	f.close()
	f = open("blacklist.dat", 'r')
	for line in f:
	    blacklist.append(line.rstrip())
	f.close()
	try:
		blacklist.pop(blacklist.index(uid + "#" + uname))
	except:
		pass #user doesn't exist
	f = open("blacklist.dat", 'w+')
	for user in blacklist:
		f.write(user + "\r\n")
	f.close()
	return blacklist

def findVoteEmojis(client):
	upemoji = "arrow_up"
	downemoji = "arrow_down"

	for x in client.get_all_emojis():
		if (x.name == "updoot" or x.name == "upvote"):
			upemoji = x.name + ":" + x.id
		if (x.name == "downdoot" or x.name == "downvote"):
			downemoji = x.name + ":" + x.id

	return upemoji, downemoji

def destroy_image(tmpargs, images):
	commands = ['grey', 'jumble', 'incbright', 'randbright', 'displace',
				'scratch', 'worms', 'compress']
	args = []
	vals = []
	if len(images) > 0:
		image = images[0]['url']
	else:
		image = tmpargs.pop(0)
	try:
		destroyer = Destroyer(image)
		for x in tmpargs:
			if x not in commands:
				vals.append(x)
			else:
				args.append(x)
		for i, arg in enumerate(args):
			if arg == 'grey':
				destroyer.greyscale()
			elif arg == 'jumble':
				destroyer.edge_jumbler()
			elif arg == 'incbright':
				destroyer.incremental_brightness()
			elif arg == 'randbright':
				destroyer.random_brightness()
			elif arg == 'displace':
				thresh = float(vals.pop(0))
				destroyer.random_displacer(thresh)
			elif arg == 'scratch':
				thresh = float(vals.pop(0))
				prop_length = int(vals.pop(0))
				destroyer.scratches(thresh, prop_length)
			elif arg == 'worms':
				amount = int(vals.pop(0))
				minP = int(vals.pop(0))
				thresh = float(vals.pop(0))
				destroyer.worms(amount, minP, thresh)
			elif arg == 'compress':
				thresh = float(vals.pop(0))
				destroyer.compress(thresh)
			else:
				return 1
			destroyer.prepare_reiterate()
		destroyer.save('0')
		return 0
	except:
		return 1

async def man(client, message):
	args = message.content.split()
	if len(args) > 1:
		if args[1] == 'queue':
			await client.send_message(message.channel, man_queue)
		elif args[1] == 'imdestroy':
			await client.send_message(message.channel, man_imdestroy)
		else:
			await client.send_message(message.channel, ':thinking: | It appears the manual page you are attempting to look up does not exist. Try annoying the developers to make some.')
	else:
		await client.send_message(message.channel, man_man)

async def asciify(client, message):
	args = message.content.split()
	args.pop(0) #delete calling function

	lines = []
	linelen = 0
	line = 0
	lines.append("")
	for word in args:
		if linelen + len(word) < 28:
			lines[line] += (word + "%20")
			linelen += len(word)
		else:
			linelen = 0
			line += 1
			lines.append("")
			lines[line] += word
			linelen += len(word)

	response = "```"
	for line in lines:
		response += "\n" + urlopen('http://artii.herokuapp.com/make?font=small&text=' + line).read().decode();
	response += "```\n -- " + message.author.mention;
	await client.send_message(message.channel, response)
