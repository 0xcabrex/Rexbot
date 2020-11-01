import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request
from discord.ext.commands import MemberConverter
import aiohttp
import asyncio
import pyfiglet
import wikipedia
from howdoi import howdoi
import base64
import urllib.parse

from googletrans import Translator


class GeneralCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# Help console

	@commands.command()
	@cooldown(1, 3, BucketType.channel)
	async def help(self, ctx, argument=None):
		mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
		admin_role = discord.utils.get(ctx.author.roles, name='Administrator')

		fun_embed = discord.Embed(
				title = 'Fun commands for @Rexbot',
				description='**8ball**\nUses AI to give you the best answers to your questions\nUsage: `r$8ball {question}`\n\n'
							'**meme**\nSends you a beautifully crafted meme\nUsage `r$meme`\n\n'
							'**dog | doggo | pupper**\nGets you a dog picture\nUsage: `r$dog`\n\n'
							'**cat | kitty**\nGets you a cat picture\nUsage: `r$cat`\n\n'
							'**asciify**\nASCIIfies your message\nUsage: `r$asciify {message}`\n\n'
							'**apod**\nGets you an Astronomy Picture Of the Day\nUsage: `r$apod`\n\n'
							'**joke**\nRandom joke has been delivered!\nUsage: `r$joke`\n\n'
							'**pjoke**\nGets you a programming related joke\nUsage: `r$pjoke`\n\n'
							'**quotes**\nA random quote\nUsage: `r$quote`\n\n',
				colour=0x01a901
			)
		fun_embed.set_footer(text='Made by CABREX with ❤')

		utils_embed = discord.Embed(
				title = 'Utility commands for @Rexbot',
				description='**avatar** | **av**\nShows the avatar of the user mentioned\nUsage: `r$avatar | $av {member_name | member_tag | member_id}`\nIf nothing is provided then it shows your avatar\n\n'
							'**userinfo | ui**\nGives the info of the mentioned user\nUsage: `r$userinfo {member_name | member_tag | member_id}`\n\n'
							'**serverinfo | si**\nGives the info of the server\nUsage: `r$serverinfo`, No arguments required\n\n'
							'**servercount | sc**\nShows you how many servers the bot is in and total number of members in those servers combined\nUsage: `r$sc`, No arguments required\n\n'
							'**wikipedia | wiki | ask | whatis**\nGets you information from the wiki\nUsage: `r$wiki {query}`\nQuery is necessary\n\n'
							'**howdoi**\nInformation from stackoverflow\nUsage: `r$howdoi {query}`\nQuery is necessary\n\n'
							'**cipher | morse**\nConverts your message to morse code\nUsage: `r$cypher {message}`\n\n'
							'**base64**\nEncodes your message to base64\nUsage: `r$base64 "{message}" {iteration}`\nMessage must be in **quotes**\n\n'
							'**dbase64**\nDecodes your base64 encoded message\nUsage: `r$dbase64 "{message}"`\nMessage must be in **quotes**\n\nUsage'
							'**qrcode**\nConverts a text to qr code\nUsage: `r$qrcode {message}`\n\n'
							'**qrdecode**\nDecodes the qr code link provided\nUsage: `r$qrdecode {url link}`\n\n'
							'**translate**\nTranslates your messag to your desired language\nUsage: `r$translate {source_anguage} {destination_language} {text}`\n\n',
				colour=0x01a901
			)
		utils_embed.set_footer(text='Made by CABREX with ❤')

		mod_embed = discord.Embed(
				title = 'Moderation commands for @Rexbot',
				description = '**kick**\nKicks the member out of the server\nUsage: `r$kick {member_name | member_id | member_tag} {reason}`, reason is not neccessary\n\n'
							  '**multikick**\nKicks multiple users out of the guild\nUsage: `r$multikick {member_name | member_id | member_tag}`, reason is not needed\n\n'
							  '**ban | hardban**\nBans the user from the server, **purging the messages**\nUsage: `r$ban {member_name | member_id | member_tag} {reason}`, reason is not necessary\n\n'
							  '**softban**\nBans the user from the server, **without removing the messages**\nUsage: `r$softban {member_name | member_id | member_tag} {reason}`, reason is not necessary\n\n'
							  '**multiban**\nBans multiple users out of the guild\nUsage: `r$multiban {member_name | member_id | member_tag}`, reason is not needed\n\n'
							  '**unban**\nUnbans the user, you need to know the member\'s name\nUsage: `r$unban {member_name#discriminator}`\n\n'
							  '**warn**\nWarns the user\nUsage: `r$warn {member_name | member_id | member_tag} {infraction}`\n\n'
							  '**warns | warnings**\nDisplays the infractions of the user mentioned\nUsage: `r$warns {member_name | member_id | member_tag}`\n\n'
							  '**clearwarns | clearwarn**\nClears all the infractions of the user\nUsage: `r$clearwarns {member_name | member_id | member_tag}`\n\n'
							  '**setwarnthresh | setwarnthreshold**\nSets the warning threshold for the server, beyond which the member gets banned\nUsage: `r$setwarnthresh {integer}`\n\n'
							  '**clearwanthresh(old) | delwarnthresh(old)**\nClears the warning threshold of the server\nUsage: `r$clearwarnthresh`\n\n'
							  '**mute**\nMutes the user\nUsage: `r$mute {member_name | member_id | member_tag} {reason}`, reason is not necessary\n\n'
							  '**unmute**\nUnmutes the user\nUsage: `r$unmute {member_name | member_id | member_tag}`\n\n'
							  '**clear | remove | purge**\nClears messages from the channel where it is used\nUsage: `r$clear {n}` where `n` is the number of messages to be purged\n\n'
							  '**addrole**\nAdds role to member\nUsage: `r$addrole {member_name | member_id | member_tag} {role_name}`\n\n'
							  '**removerole | purgerole**\nRemoves role from mentioned member\nUsage: `r$removerole {member_name | member_id | member_tag} {role_name}`\n\n',
				colour=0x01a901
			)
		mod_embed.set_footer(text='Made by CABREX with ❤')

		support_embed = discord.Embed(
				title = 'Support commands for @Rexbot',
				description = '**bug | bugs**\nFound any bugs? Use this command to report the bugs\nUsage: `r$bugs "{message}"`\n\nMessage must be greater than 20 charecters.\nYou can also direct message the bot instead of invoking the command\n\n'
							  '**invite**\nInvite me to your server! 😁\nUsage: `r$invite`\n\n'
							  '**source | sourcecode**\nWant to know what was I written in? I\'ll send you a github link 😉\n`Usage: r$source`\nNo argument required\n\n'
							  '**supportserver | ss**\nLink to the support server\nUsage: `r$ss`\n\n',
				colour=0x01a901
			)
		support_embed.set_footer(text='Made by CABREX with ❤')        

		initial_help_dialogue = discord.Embed(
				title = 'Help command',
				description = '`r$help Fun`\nFun commands\n\n'
							  '`r$help Moderation` | `r$help mod`\nModeration commands\n\n'
							  '`r$help utils` | `r$help util`\nUtility commands\n\n'
							  '`r$help support`\nSupport commands\n\n',
				colour=0x01a901
			)
		initial_help_dialogue.set_footer(text='Made by CABREX with ❤')

		if argument is None:
			await ctx.send(embed=initial_help_dialogue)
		elif argument.lower() == 'fun':
			await ctx.send(embed=fun_embed)
		elif argument.lower() == 'moderation' or argument.lower() == 'mod':
			await ctx.send(embed=mod_embed)
		elif argument.lower() == 'utils' or argument.lower() == 'util':
			await ctx.send(embed=utils_embed)
		elif argument.lower() == 'support':
			await ctx.send(embed=support_embed)
		else:
		  pass


	# Help console: Error handling

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Avatar fetcher

	@commands.command(aliases=['av'])
	@cooldown(1, 5, BucketType.channel)
	async def avatar(self, ctx, member, override=None):

		if member[0] == '<' and member[1] == '@':
			converter = MemberConverter()
			member = await converter.convert(ctx, member)
		elif member.isnumeric():
			member = int(member)
		else:
			pass

		members = await ctx.guild.fetch_members().flatten()
		multiple_member_array = []
			
		if isinstance(member, discord.Member):
			for members_list in members:
				if member.name.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
				else:
					pass
		elif isinstance(member, int):
			for member_list in members:
				if member_list.id == member:
					multiple_member_array.append(member_list)
				else:
					pass
		else:
			for members_list in members:
				if member.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
				else:
					pass

		if member is discord.Member:
			if member.isnumeric() and member.lower() == 'me' and override == 'override':
				embed = discord.Embed(colour=0x0000ff)
				embed.set_image(url=f'{ctx.author.avatar_url}')
				await ctx.send(embed=embed)

		elif len(multiple_member_array) == 1:

			if isinstance(member, int):
				embed = discord.Embed(colour=0x0000ff)
				embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
			else:
				embed = discord.Embed(colour=0x0000ff)
				embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
			await ctx.send(embed=embed)

		elif len(multiple_member_array) > 1:

			multiple_member_array_duplicate_array = []
			for multiple_member_array_duplicate in multiple_member_array:
				if len(multiple_member_array_duplicate_array) < 10:
					multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
				else:
					break

			embed = discord.Embed(
					title=f'Search for {member}\nFound multiple results (Max 10)',
					description=f'\n'.join(multiple_member_array_duplicate_array),
					colour=0x808080
				)
			await ctx.send(embed=embed)

		else:
			await ctx.send(f'The member `{member}` does not exist!')
	


	# Avatar fetcher: Error handling

	@avatar.error
	async def avatar_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(colour=0x0000ff)
			embed.set_image(url=f'{ctx.author.avatar_url}')
			await ctx.send(embed=embed)
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Userinfo

	@commands.command(aliases=['ui', 'Ui'])
	@cooldown(1, 5, BucketType.channel)
	async def userinfo(self, ctx, member):

		if member[0] == '<' and member[1] == '@':
			converter = MemberConverter()
			member = await converter.convert(ctx, member)
		elif member.isnumeric():
			member = int(member)

		members = await ctx.guild.fetch_members().flatten()
		multiple_member_array = []
	  
		
		if isinstance(member, discord.Member):
			for members_list in members:
				if member.name.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
				else:
					pass

		elif isinstance(member, int):
			for member_list in members:
				if member_list.id == member:
					multiple_member_array.append(member_list)
				else:
					pass

		else:
			for members_list in members:
				if member.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
				else:
					pass

		if len(multiple_member_array) == 1:

			roles = []
			for role in multiple_member_array[0].roles:
				roles.append(role)

			embed = discord.Embed(
				colour = 0x0000ff,
			)
			embed.set_author(name=f'User Info - {multiple_member_array[0]}')
			embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
			embed.set_footer(text='made by CABREX with ❤')

			embed.add_field(name='ID:', value=multiple_member_array[0].id)
			embed.add_field(name='Member Name:', value=multiple_member_array[0])
			embed.add_field(name='Member Nickname:', value=multiple_member_array[0].display_name)

			embed.add_field(name='Created at: ', value=multiple_member_array[0].created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
			embed.add_field(name='Joined at:', value=multiple_member_array[0].joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

			if len(roles) == 1:
				embed.add_field(name=f'Roles ({len(roles) - 1})', value='**NIL**')
			else:
				embed.add_field(name=f'Roles ({len(roles) - 1})', value=' '.join([role.mention for role in roles if role.name != '@everyone']))

			embed.add_field(name='Bot?', value=multiple_member_array[0].bot)

			await ctx.send(embed=embed)


		elif len(multiple_member_array) > 1:

			multiple_member_array_duplicate_array = []
			for multiple_member_array_duplicate in multiple_member_array:
				if len(multiple_member_array_duplicate_array) < 10:
					multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
				else:
					break

			embed = discord.Embed(
					title=f'Search for {member}\nFound multiple results (Max 10)',
					description=f'\n'.join(multiple_member_array_duplicate_array),
					colour=0x808080
				)
			await ctx.send(embed=embed)

		else:
			await ctx.send(f'The member `{member}` does not exist!')


	# Userinfo: Error handling

	@userinfo.error
	async def userinfo_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('```\n$userinfo {member_name}\n          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, discord.errors.Forbidden):
			await ctx.send('I am Forbidden from doing this command, please check if `server members intent` is enabled')
		else:
			await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
			raise error


	# Server info

	@commands.command(aliases=['si', 'Si'])
	@cooldown(1, 4, BucketType.channel)
	async def serverinfo(self, ctx):
	
		count = 0

		members = await ctx.guild.fetch_members().flatten()

		for people in members:
			if people.bot:
				count = count + 1
		else:
			pass

		embed = discord.Embed(
			title = f'{ctx.guild.name} info',
			colour = 0x0000ff
		)
		embed.set_thumbnail(url=ctx.guild.icon_url)

		embed.add_field(name='Owner name:', value=f'<@{ctx.guild.owner_id}>')
		embed.add_field(name='Server ID:', value=ctx.guild.id)

		embed.add_field(name='Server region:', value=ctx.guild.region)
		embed.add_field(name='Members:', value=ctx.guild.member_count)
		embed.add_field(name='bots:', value=count)
		embed.add_field(name='Humans:', value=ctx.guild.member_count - count)

		embed.add_field(name='Number of roles:', value=len(ctx.guild.roles))
		embed.add_field(name='Number of boosts:', value=ctx.guild.premium_subscription_count)

		embed.add_field(name='Text Channels:', value=len(ctx.guild.text_channels))
		embed.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels))
		embed.add_field(name='Categories:', value=len(ctx.guild.categories))

		embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		await ctx.send(embed=embed)


	# Serverinfo: Error handling

	@serverinfo.error
	async def serverinfo_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
			raise error
		else:
			await ctx.send(f"An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX.")
			raise error


	# Servercount

	@commands.command(name='servercount', aliases=['Servercount', 'Sc', 'sc'])
	@cooldown(1, 1, BucketType.channel)
	async def servercount(self, ctx):
		
		member_count = 0
		for guild in self.bot.guilds:
			member_count += guild.member_count

		await ctx.send(f'Present in `{len(self.bot.guilds)}` servers, moderating `{member_count}` members')

	
	# Servercount: cooldown

	@servercount.error
	async def sc_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Wikipedia support

	@commands.command(name='wikipedia', aliases=['ask', 'whatis', 'wiki'])
	@cooldown(1, 2,BucketType.channel)
	async def wiki(self, ctx, *, query=None):
		if query is not None:
			r = wikipedia.page(query)
			embed = discord.Embed(
				title = r.title,
				description = r.summary[0 : 2000],
				colour = 0x808080
			)
			async with ctx.typing():
				await asyncio.sleep(2)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"Your query is empty {ctx.author.mention}!\nEnter something!")


	# Wikipedia: Error handling

	@wiki.error
	async def wiki_error(self, ctx, error):
		if isinstance(error, wikipedia.exceptions.DisambiguationError):
			await ctx.send(f'There are many articles that match your query, please be more specific {ctx.author.mention}')
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error has occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Howdoi stackoverflow API

	@commands.command(name='howdoi')
	@cooldown(1, 2, BucketType.channel)
	async def howdoi(self, ctx, *, query=None):
		if query is not None:
			parser = howdoi.get_parser()
			arguments = vars(parser.parse_args(query.split(' ')))

			embed = discord.Embed(
				title = f'how to {query}',
				description = howdoi.howdoi(arguments)
			)
			async with ctx.typing():
				await asyncio.sleep(2)
			await ctx.channel.send(embed=embed)
		else:
			await ctx.send(f'Your query is empty, please ask a question {ctx.author.mention}')


	# Howdoi: Error Handling

	@howdoi.error
	async def howdoi_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
			raise error


	# Morse code cypher

	@commands.command(name='cypher', aliases=['Cypher', 'morse', 'Morse'])
	@cooldown(1, 2, BucketType.channel)
	async def cypher(self, ctx, *, message):
		
		MORSE_DICT = { 'A':'.-', 'B':'-...', 
					'C':'-.-.', 'D':'-..', 'E':'.', 
					'F':'..-.', 'G':'--.', 'H':'....', 
					'I':'..', 'J':'.---', 'K':'-.-', 
					'L':'.-..', 'M':'--', 'N':'-.', 
					'O':'---', 'P':'.--.', 'Q':'--.-', 
					'R':'.-.', 'S':'...', 'T':'-', 
					'U':'..-', 'V':'...-', 'W':'.--', 
					'X':'-..-', 'Y':'-.--', 'Z':'--..', 
					'1':'.----', '2':'..---', '3':'...--', 
					'4':'....-', '5':'.....', '6':'-....', 
					'7':'--...', '8':'---..', '9':'----.', 
					'0':'-----', ', ':'--..--', '.':'.-.-.-', 
					'?':'..--..', '/':'-..-.', '-':'-....-', 
					'(':'-.--.', ')':'-.--.-'}

		cipher = ''

		for letter in message.upper():
			if letter != ' ':
				cipher += MORSE_DICT[letter] + ' '
			else:
				cipher += ' '

		await ctx.send(f'Here is your cyphered text:\n```\n{cipher}\n```')


	# Morse code cypher: Error handling

	@cypher.error
	async def cypher_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.BadArgument):
			await ctx.send('What do you want to cypher?')
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Base64 encoding

	@commands.command(name='base64', aliases=['Base64'])
	@cooldown(1, 2, BucketType.channel)
	async def base64(self, ctx, message, iterations=1):

		if iterations <= 20:
			message_bytecode = message.encode('ascii')

			for i in range(iterations):
				message_bytecode = base64.b64encode(message_bytecode)
				base64_message = message_bytecode.decode('ascii')

			await ctx.send(f'Here is the base64 encoded version encoded {iterations} time(s):\n```\n{base64_message}\n```')
		else:
			await ctx.send(f"Maximum number of iterations possible are 20, **{iterations}** number of ierations not allowed")
		


	# Base64 encoding: Error handling

	@base64.error
	async def base64_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('What are the arguments')
		elif isinstance(error, commands.BadArgument):
			await ctx.send("Please enter your text to be encode in quotes")
		elif isinstance(error, base64.binascii.Error):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await ctx.send("You didnt close the quotes!")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await ctx.send("Too many quotes!")
		elif isinstance(error, commands.UnexpectedQuoteError):
			await ctx.send("Unexpected quote in non-quoted string")
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Base64 decoding

	@commands.command(name='dbase64', aliases=['Dbase64'])
	@cooldown(1, 2, BucketType.channel)
	async def base64_decode(self, ctx, message):

		message_bytecode = message.encode('ascii')

		decode_bytecode = base64.b64decode(message_bytecode)
		base64_message = decode_bytecode.decode('ascii')

		await ctx.send(f'Here is the base64 decoded version:\n```\n{base64_message}\n```')
		


	# Base64 decoding: Error handling

	@base64_decode.error
	async def base64_decode_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('What are the arguments')
		elif isinstance(error, commands.BadArgument):
			await ctx.send("Please enter your text to be encode in quotes")
		elif isinstance(error, base64.binascii.Error) or isinstance(error, binascii.Error):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, UnicodeDecodeError):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await ctx.send("You didnt close the quotes!")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await ctx.send("Too many quotes!")
		elif isinstance(error, commands.UnexpectedQuoteError):
			await ctx.send("Unexpected quote in non-quoted string")
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# QR Code generator

	@commands.command(name='qrcode')
	@cooldown(1, 5, BucketType.channel)
	async def qr_code_generator(self, ctx, *, message=None):
		if message is not None:
			embed = discord.Embed(
				title = 'Here is your encoded text',
				colour = 0x01a901
			)

			query = urllib.parse.quote(message, safe='')

			url = f'http://api.qrserver.com/v1/create-qr-code/?data={query}'

			embed.set_image(url=url)
			await ctx.send(embed=embed)
		else:
			await ctx.send("Please enter a message to qrcode encode it")


	# QR Code generator: Error handling

	@qr_code_generator.error
	async def qr_code_generator_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# QR Code reader

	@commands.command(name='qrdecode')
	@cooldown(1, 5, BucketType.channel)
	async def qr_code_decode(self, ctx, message):

		encoded_url = urllib.parse.quote(message, safe='')
		

		url = f'http://api.qrserver.com/v1/read-qr-code/?fileurl={encoded_url}&format=json'

		async with request("GET", url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				symbol = data[0]["symbol"]

				if symbol[0]["data"] is not None:
					await ctx.send(f'Here is the decoded qr code:\n```\n{symbol[0]["data"]}\n```')
				else:
					await ctx.send(f'An error occured: **{symbol[0]["error"]}**')


	# QR Code reader: Error handling

	@qr_code_generator.error
	async def qr_code_generator_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Translator 

	@commands.command(name='translate')
	@cooldown(1, 5, BucketType.channel)
	async def translator(self, ctx, source_language: str = 'en', destination_language: str = 'en', *, message):

		translator = Translator()

		translation = translator.translate(
			message, dest=destination_language, src=source_language
		)
		embed = discord.Embed(
			title="Translation",
			description=f"Sentence : **{message}**\n\nTranslation : **{translation.text}**\n\nType : **{translation.src} > {translation.dest}**",
			color=0x008000,
		)
		await ctx.send(embed=embed)


	# Translator: Error handling

	@translator.error
	async def translator_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("What do you want to translate?")
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error



def setup(bot):
	bot.add_cog(GeneralCog(bot))
