import discord
from urllib.request import urlopen
import asyncio

def updateBlacklist():
	blacklist = []
	file = open("blacklist.dat", 'a+')
	file.close()
	file = open("blacklist.dat", 'r')
	for line in file:
	    blacklist.append(line.rstrip().split("#")[0])
	file.close()
	return blacklist;

def blacklist(uid, uname):
	file = open("blacklist.dat", 'a+')
	file.write(uid + "#" + uname + "\r\n")
	file.close()
	return updateBlacklist()

def pardon(uid, uname):
	blacklist = []
	file = open("blacklist.dat", 'a+')
	file.close()
	file = open("blacklist.dat", 'r')
	for line in file:
	    blacklist.append(line.rstrip())
	file.close()

	try:
		blacklist.pop(blacklist.index(uid + "#" + uname))
	except:
		print("doesnt exist lololololol")

	file = open("blacklist.dat", 'w+')
	for user in blacklist:
		file.write(user + "\r\n")
	file.close()

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
