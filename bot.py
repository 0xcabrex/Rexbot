#!/usr/bin/python3
import discord
from discord import Intents
import random
import time
import os
from discord.ext import commands
from cogs.usefullTools.dbIntegration import *


# Get prefix

def get_prefix(bot, message):

	return fetch_prefix(message.guild.id)["prefix"]

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')
working_directory = os.getcwd()



try:
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			bot.load_extension(f"cogs.{filename[:-3]}")
except Exception as e:
	print("Cogs error: Cannot load cogs")
	print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
	print("Functionality limited!\n")
	print(f"exception thrown:\n{e}")


# Shows command prefix if asked

@bot.event
async def on_message(message):

	reply_choices = [
						"Hi",
						"Hi there",
						"Hey",
						"Hey there",
						"Whatsup",
						"Waddup",
						"Whats going on",
						"Hello",
						"Hello!",
						"Sup",
						"Howdy"
					]

	message_var = message.content


	if message.author.bot:
		return
	elif (bot.user in message.mentions) and message_var.lower().find('prefix') != -1:
		await message.channel.send(f'My command prefix is `{fetch_prefix(message.guild.id)["prefix"]}`, **{message.author.display_name}**')
	elif bot.user in message.mentions:
		if message_var.lower().find('awesome') != -1 or message_var.lower().find('cool') != -1 or message_var.lower().find('good') != -1 or message_var.lower().find('nice') != -1 :
			await message.channel.send(f'Thanks bro 😁')
		elif message_var.lower().find('bad') != -1 or message_var.lower().find('horrible') != -1 or message_var.lower().find('suck') != -1 or message_var.lower().find('terrible') != -1 or message_var.lower().find('waste') != -1 or message_var.lower().find('fk') != -1 or message_var.lower().find('fuck') != -1:
			await message.channel.send(f'No you\nI do the basic functions okay I aint dyno or mee6\n\nJesus christ.')
		elif message_var.lower().find('how are you') != -1 :
			await message.channel.send(f'I am fine, {message.author.display_name}')
		else:
			await message.channel.send(f'{random.choice(reply_choices)}, **{message.author.display_name}**!')
	if str(message.channel.type) == 'private':
		if len(message.content) > 20:
			bugs_channel1 = discord.utils.get(bot.get_all_channels(), guild__name='Cyber Experimentation Facility', name='bugs')
			bugs_channel2 = discord.utils.get(bot.get_all_channels(), guild__name='ZeroDeaths', name='bugs')
			embed = discord.Embed(
						title='BUG REPORTED',
						colour = 0x008000
				)
			embed.add_field(name='Username', value=message.author)
			embed.add_field(name='User id', value=message.author.id)
			embed.add_field(name='Bug: ', value=message.content)
			if bugs_channel1 is not None:
				await bugs_channel1.send(embed=embed)
				await bugs_channel2.send(embed=embed)
			elif bugs_channel2 is not None:
				await bugs_channel2.send(embed=embed)
			await message.channel.send("Your bug has been reported")
		else:
			await message.channel.send("Please enter your bug in more than 20 words, try describing everything")

	await bot.process_commands(message)



# Basic stuff

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your lives'))
	print("+[ONLINE] Rexbot is online")


@bot.event
async def on_member_join(member):
	try:
		print(f'+[NEW_MEMBER]    {member} has joined the server: {member.guild.name}')
		
		channel = None
		if fetch_join_log_channel(int(member.guild.id)) is not None:
			channel = bot.get_channel(fetch_join_log_channel(int(member.guild.id))["channel_id"])

		if channel is not None:
			embed = discord.Embed(
					title = 'Member joined the server',
					description=f'Member **{member.name}** joined the server!',
					colour=0x008000
				)
			members = await member.guild.fetch_members().flatten()

			bot_count = 0
			for people in members:
				if people.bot is True:
					bot_count += 1

			embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name='Number of members', value=len(members) - bot_count)
			embed.add_field(name='Number of bots', value=bot_count)
			embed.set_footer(text=f'id: {member.id}')
			await channel.send(embed=embed)
		else:
			pass
	except Exception as e:
		raise Exception




@bot.event
async def on_member_remove(member):
	try:
		print(f'+[REMOVE_MEMBER]   {member} has left the server: {member.guild.name}')

		delete_warns(member.guild.id, member.id)

		channel = None
		if fetch_leave_log_channel(int(member.guild.id)):
			channel = bot.get_channel(fetch_leave_log_channel(int(member.guild.id))["channel_id"])


		if channel is not None:
			embed = discord.Embed(
				title = 'Member left the server',
				description=f'Member **{member.name}** has left the server!',
				colour=0xFF0000
			)
			try:
				members = await member.guild.fetch_members().flatten()

				bot_count = 0
				for people in members:
					if people.bot is True:
						bot_count += 1

				embed.set_thumbnail(url=member.avatar_url)
				embed.add_field(name='Number of members', value=len(members) - bot_count)
				embed.add_field(name='Number of bots', value=bot_count)
				embed.set_footer(text=f'id: {member.id}')
				await channel.send(embed=embed)
			except:
				pass
		else:
			pass
	except Exception as e:
		raise Exception

@bot.event
async def on_guild_channel_delete(channel):

	join_channel = None
	if fetch_join_log_channel(int(channel.guild.id)) is not None:
		join_channel = fetch_join_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == join_channel:
			delete_join_log_channel(int(channel.guild.id))

	leave_channel = None
	if fetch_leave_log_channel(int(channel.guild.id)) is not None:
		leave_channel = fetch_leave_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == leave_channel:
			delete_leave_log_channel(int(channel.guild.id))

	log_channel = None
	if fetch_mod_log_channel(int(channel.guild.id)) is not None:
		mod_channel = fetch_mod_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == mod_channel:
			delete_mod_log_channel(int(channel.guild.id))



@bot.event
async def on_guild_join(guild):

	insert_prefix(guild.id, "r$")


@bot.event
async def on_guild_remove(guild):

	clear_server_data(guild.id)



# Ping

@bot.command()
async def ping(ctx):
	await ctx.send(f'Ping: {round(bot.latency * 1000)}ms')

# If the user enters something bonkers

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):

		prefix = fetch_prefix(ctx.guild.id)["prefix"]

		await ctx.send(f"command not found\nPlease use `{prefix}help` to see all commands")


TOKEN = os.getenv("REXBOT_TOKEN")
try:
	if TOKEN is None:
		try:
			with open('./token.0', 'r', encoding='utf-8') as file_handle:
				TOKEN = file_handle.read()
				if TOKEN is not None:
					print('Using token found in token file..')
					bot.run(TOKEN)
				else:
					print("Token error: Token not found")
		except FileNotFoundError:
			print("No token file or environment variable\nQuitting")
	else:
		print('Using token found in Environment variable....')
		bot.run(TOKEN)
except discord.errors.LoginFailure:
	print("\033[1;31;40mFATAL ERROR\033[0m 1;31;40m\nToken is malformed; invalid token")