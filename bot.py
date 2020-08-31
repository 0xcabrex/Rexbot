#!/usr/bin/python3

import discord
import random
import time
import os
from discord.ext import commands

bot = commands.Bot(command_prefix=('$'))
bot.remove_command('help')
working_directory = os.getcwd()

# Loading cogs
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


#if working_directory !='/home/tron/ZeroDeaths/rexbot':
#	print("Cogs error: Cannot load cogs")
#	print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
#	print("Functionality limited!\n")
#else:
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")


# Basic stuff
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your lives'))
    print("+[ONLINE] Rexbot is online")


@bot.event
async def on_member_join(member):
    print(f'+[NEW_MEMBER]    {member} has joined the server!')


@bot.event
async def on_member_remove(member):
    print(f'+[REMOVE_MEMBER]   {member} has left the server!')


# Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'+[PING] ping: {round(bot.latency * 1000)}ms')

# If the user enters something bonkers
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Bruh what is that?")


TOKEN = os.getenv("REXBOT_TOKEN")
if TOKEN is None:
    with open('./token.0', 'r', encoding='utf-8') as file_handle:
        TOKEN = file_handle.read()
        if TOKEN is not None:
            bot.run(TOKEN)
        else:
            print("Token error: Token not found")

else:
    bot.run(TOKEN)
