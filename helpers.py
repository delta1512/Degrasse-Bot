import discord
import asyncio
from urllib.request import urlopen
from ImageDestroyer import Destroyer

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
				'scratch', 'worms']
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
			else:
				return 1
			destroyer.prepare_reiterate()
		destroyer.save('0')
		return 0
	except Exception as e:
		print('[ERROR] Error caught in destroy_image()')
		print(e)
		return 1



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

'''
###

destroy_image(['jumble'], [{'url' : 'https://cdn.discordapp.com/attachments/320670306010398730/361697510470713344/unknown.png'}])
'''
