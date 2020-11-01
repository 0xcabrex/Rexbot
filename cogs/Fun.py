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


class FunCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# the eight ball

	@commands.command(name='8ball')
	@cooldown(1,5,BucketType.channel)
	async def eight_ball(self, ctx, *, question=None):
		responses = ["It is certain.",
					 "It is decidedly so.",
					 "Without a doubt.",
					 "Yes - definitely.",
					 "You may rely on it.",
					 "As I see it, yes.",
					 "Most likely.",
					 "Outlook good.",
					 "Yes.",
					 "Signs point to yes.",
					 "Reply hazy, try again.",
					 "Ask again later.",
					 "Better not tell you now.",
					 "Cannot predict now.",
					 "Concentrate and ask again.",
					 "Don't count on it.",
					 "My reply is no.",
					 "My sources say no.",
					 "Outlook not so good.",
					 "Very doubtful."
					 ]

		if question is not None:
			embed = discord.Embed(title='*The 8ball*', description=f'**{ctx.message.author}** asked a question.\n\nThe question was: **{question}**\n\n\n{random.choice(responses)}', colour=0x0000ff)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Ask me a question!')


	# eightball: Error handling

	@eight_ball.error
	async def eightball_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')


	# Memes

	@commands.command(aliases=['Meme'])
	@cooldown(1, 3, BucketType.channel)
	async def meme(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		meme_url = "https://meme-api.herokuapp.com/gimme?nsfw=false"
		async with request("GET", meme_url, headers={}) as response:
			if response.status==200:
				data = await response.json()
				image_link = data["url"]
			else:
				image_link = None

		async with request("GET", meme_url, headers={}) as response:
			if response.status==200:
				data = await response.json()
				embed = discord.Embed(
					title=data["title"],
					url=image_link,
					colour=random.choice(colour_choices)
				)
				if image_link is not None:
					embed.set_image(url=image_link)
					await ctx.send(embed=embed)

			else:
				await ctx.send(f"The API seems down, says {response.status}")


	# Memes: Error handling

	@meme.error
	async def meme_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
			raise error


	# Dog pictures

	@commands.command(aliases=['doggo','pupper'])
	@cooldown(1, 1, BucketType.channel)
	async def dog(self, ctx):
	  
		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		dog_url="https://random.dog/woof.json"
		async with request("GET", dog_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				image_link = data["url"]
				embed = discord.Embed(
					colour = random.choice(colour_choices)
				)
				embed.set_image(url=image_link)
				await ctx.send(embed=embed)

			else:
				await ctx.send(f"The API seems down, says {response.status}")


	# Dog pictures: Error handling

	@dog.error
	async def dog_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
			raise error


	# Cat pictures

	@commands.command(aliases=['Cat'])
	@cooldown(1, 1, BucketType.channel)
	async def cat(self, ctx):
	  
		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		cat_url = "http://aws.random.cat/meow"
		async with request("GET", cat_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				image_link = data["file"]
				embed = discord.Embed(
						colour= random.choice(colour_choices)
				)
				embed.set_image(url=image_link)
				await ctx.send(embed=embed)

			else:
				await ctx.send(f'The API seems down, says {response.status}')


	# Cat pictures: Error handling

	@cat.error
	async def cat_picture_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
			raise error


	# Animal facts

	@commands.command(name='fact', aliases=['facts'])
	async def animal_facts(self, ctx, animal:str):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		if animal.lower() in {'dog', 'cat', 'bird'}:
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url=f"https://some-random-api.ml/img/{'birb' if animal=='bird' else animal}"
			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]
				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					description = data["fact"]
					if len(description) > 2045:
						description = f'{data["fact"][:2045].strip()}...'
					else:
						description = data["fact"]

			embed = discord.Embed(
				title = f'Facts about {animal.lower()}',
				description=description,
				colour=random.choice(colour_choices)
			)

			if image_link is not None:
				embed.set_image(url = image_link)
			embed.set_footer(text='Made by CABREX with ❤')

			await ctx.send(embed=embed)


	# Animal Facts: Error handling

	@animal_facts.error
	async def animal_facts_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Which animal do you want the facts for?")
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error 


	# ASCIIfy your message

	@commands.command(name='asciify')
	@cooldown(1, 1, BucketType.channel)
	async def asciify_message(self, ctx, *, message=None):
		if message is not None:
			if message[0] == '<' and (message[1] == ':'):
				await ctx.send('im not doing that 😂')
			elif message[0] == '<' and message[1] == '@':
				await ctx.send('im not doing that 😂')
			elif ctx.author.is_on_mobile and len(message) > 8:
				await ctx.send('The output might look a bit weird on your phone! 😅\n Landscape mode might make it look Better')
				msg = pyfiglet.figlet_format(message)
				await ctx.send(f'```css\n{msg}\n```')
			else:
				msg = pyfiglet.figlet_format(message)
				await ctx.send(f'```css\n{msg}\n```')
		else:
			await ctx.send('Whats it you want to asciify?')


	# ASCIIfy: Error handling

	@asciify_message.error
	async def asciify_message_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error

	# APOD

	@commands.command(name='apod')
	@cooldown(1, 2, BucketType.channel)
	async def apod(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff] 
		

		with open('./NASA_API_TOKEN.0', 'r', encoding='utf-8') as nasa_api_token_file_handle:
			API = nasa_api_token_file_handle.read()

		apod_url = f'https://api.nasa.gov/planetary/apod?api_key={API}'
		data = None

		async with request("GET", apod_url, headers={}) as response:    
			data = await response.json()

		try:
			if len(data["explanation"]) > 2048:
				description = f"{data['explanation'][:2045].strip()}..."
			else:
				description = data["explanation"]
		except KeyError:
			await ctx.send('There is a problem in the content, please try again')

		embed = discord.Embed(
			title=data["title"],
			description=description,
			color=random.choice(colour_choices)
		)
		embed.set_image(url=data["hdurl"])
		embed.set_footer(text=f"Here is the Astronomy Picture of the Day")

		async with ctx.typing():
			await asyncio.sleep(2)
		await ctx.send(embed=embed)



	# APOD: Error handling

	@apod.error
	async def apod_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Random Jokes 

	@commands.command(name='joke', aliases=['Joke','jokes','Jokes'])
	@cooldown(1, 2, BucketType.channel)
	async def jokes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		jokes_url = 'https://official-joke-api.appspot.com/random_joke'

		async with request("GET", jokes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				title = data["setup"]
				description = data["punchline"]

				embed = discord.Embed(
								title = title,
								description = description,
								colour = random.choice(colour_choices)
					)
				await ctx.send(embed=embed)
			else:
				await ctx.send(f'The API seems down, say {response.status}')


	# Random jokes: Error handling

	@jokes.error
	async def jokes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error            


	# Programming jokes

	@commands.command(name='pjoke', aliases=['Pjoke','pjokes','Pjokes'])
	@cooldown(1, 2, BucketType.channel)
	async def programmingjokes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		jokes_url = 'https://official-joke-api.appspot.com/jokes/programming/random'

		async with request("GET", jokes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				title = data[0]["setup"]
				description = data[0]["punchline"]

				embed = discord.Embed(
								title = title,
								description = description,
								colour = random.choice(colour_choices)
					)
				await ctx.send(embed=embed)
			else:
				await ctx.send(f'The API seems down, say {response.status}')


	# Programming jokes: Error handling

	@programmingjokes.error
	async def programmingjokes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Quotes 

	@commands.command(name='quotes', aliases=['Quotes', 'quote', 'Quote'])
	@cooldown(1, 2, BucketType.channel)
	async def quotes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		quotes_url = 'http://staging.quotable.io/random'

		async with request("GET", quotes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				
				quote = data["content"]
				author = data["author"]

				await ctx.send(f'```\n{quote}\n```\n**-{author}**')
			else:
				await ctx.send(f"API seems down, says {response.status} code")


	# Quotes: Error handling

	@quotes.error
	async def quotes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


def setup(bot):
	bot.add_cog(FunCog(bot))
