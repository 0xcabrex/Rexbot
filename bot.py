#!/usr/bin/python3

import discord
import random
import time
import os
from discord.ext import commands

command_prefix='$'

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

try:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")
except Exception as e:
    print("Cogs error: Cannot load cogs")
    print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
    print("Functionality limited!\n")
    print(f"exception thrown:\n{e}")


# Basic stuff

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with your lives'))
    print("+[ONLINE] Rexbot is online")


@bot.event
async def on_member_join(member):
    print(f'+[NEW_MEMBER]    {member} has joined the server: {member.guild.name}')
    channel = discord.utils.get(member.guild.channels, name='moderation-logs')
    if channel is not None:
        embed = discord.Embed(
                title = 'Member joined the server',
                description=f'Member **{member.name}** joined the server!',
                colour=0x008000
            )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Number of members', value=str(member.guild.members))
        await channel.send(embed=embed)
    else:
        pass




@bot.event
async def on_member_remove(member):
    print(f'+[REMOVE_MEMBER]   {member} has left the server: {member.guild.name}')
    channel = discord.utils.get(member.guild.channels, name='moderation-logs')
    if channel is not None:
        embed = discord.Embed(
            title = 'Member left the server',
            description=f'Member **{member.name}** has left the server!',
            colour=0xFF0000
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Number of members', value=str(member.guild.members))
        await channel.send(embed=embed)
    else:
        pass

# Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping: {round(bot.latency * 1000)}ms')

# If the user enters something bonkers

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"command not found\nPlease use `$help` to see all commands")


TOKEN = os.getenv("REXBOT_TOKEN")
if TOKEN is None:
    try:
        with open('./token.0', 'r', encoding='utf-8') as file_handle:
            TOKEN = file_handle.read()
            if TOKEN is not None:
                print('Using token found in token file..')
                bot.run(TOKEN)
            else:
                print("Token error: Token not found")
    except:
        print("File handle error")
else:
    print('Using token found in Environment variable....')
    bot.run(TOKEN)
