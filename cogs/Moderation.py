import discord
import time
from discord.ext import commands


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Kick members

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            if ctx.message.author.guild_permissions.manage_members:
                await member.kick(reason=reason)
                embed = discord.Embed(title='**USER KICKED**',description=f'User **{member}** has been kicked due to:\n **{reason}**', colour=0xff0000)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **kick**', description=f'<@&732211099264352268>\n<@{author}> Used the `kick` command, Who is not a moderator', colour=0xff0000)
                await channel.send(embed=emb)
        except:
            await ctx.send("<:nope:742029970502713385> You cant kick a mod!")

    # Kick members: Error handling

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$kick {member_name} {reason}\n      ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')

    # Ban members

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if ctx.message.author.guild_permissions.manage_members:
                if reason is None:
                    await ctx.send("What is the reason for the ban?")
                else:
                    await member.ban(reason=reason)
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{member}** has been banned due to:\n **{reason}**', colour=0xff0000)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'<@&732211099264352268>\n`<@{author}` Used the `ban` command, Who is not a moderator>', colour=0xff0000)
                await channel.send(embed=emb)
        except:
            await ctx.send("<:nope:742029970502713385> I dont have sufficient privelages!")

    # Ban members: Error handling

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$ban {member_name} {reason}\n     ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')

    # Unban members

    @commands.command()
    async def unban(self, ctx, *, member):
        if ctx.message.author.guild_permissions.manage_members:
            banned_users = await ctx.guild.ban()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(description=f'***Banned user {user.mention}***', colour=0x008000)
                    await ctx.send(embed=embed)
                    return
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **unban**', description=f'<@&732211099264352268>\n`<@{author}` Used the `unban` command, Who is not a moderator>', colour=0xff0000)
            await channel.send(embed=emb)

    # Clear command
    
    @commands.command(aliases=['remove'])
    async def clear(self, ctx, amount=0):
        if ctx.message.author.guild_permissions.manage_messages:
            if amount == 0:
                await ctx.send("How many do you want to remove?")
            else:
                await ctx.channel.purge(limit=amount + 1)
                time.sleep(0.5)
                msg = await ctx.send(f"Removed {amount} messages!")
                time.sleep(1.5)
                await msg.delete()
                #await ctx.channel.purge(limit=1)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **clear**', description=f'<@&732211099264352268>\n`<@{author}` Used the `clear` command, Who is not a moderator>', colour=0xff0000)
            await channel.send(embed=emb)

    # Announcements

    @commands.command()
    async def userpost(self, ctx, *, message=None):
        try:
            if ctx.message.author.guild_permissions.manage_messages:
                if message is None:
                    await ctx.send("What is the message?")
                else:
                    channel = discord.utils.get(ctx.guild.channels, name='general')
                    await channel.send(message)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n`<@{author}` Used the `userpost` command, Who is not a moderator>', colour=0xff0000)
                await channel.send(embed=emb)
        except:
            await ctx.send("Some weird error bot is mad about...")

    # Embeded Announcements
    @commands.command()
    async def embedpost(self, ctx, *, message=None):
        if ctx.message.author.guild_permissions.manage_messages:
            if message is None:
                await ctx.send("What is the message to send")
            else:
                channel = discord.utils.get(ctx.guild.channels, name='general')
                embed = discord.Embed(title=f'Announcement by **{ctx.message.author}**', description=f'*{message}*', colour=0x0000ff)
                await channel.send(embed=embed)
        else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n`<@{author}` Used the `userpost` command, Who is not a moderator>', colour=0xff0000)
                await channel.send(embed=emb)
        

    # Mute members

    @commands.command(aliases=['mute'])
    async def _mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if member == str(ctx.author):
                await ctx.send("**You can't mute yourself**")
            else:
                if reason is None:
                    await ctx.send("What is the reason for the mute?")
                else:
                    muted = discord.utils.get(ctx.guild.roles, name='Muted')
                    if muted is not None:
                        role = discord.utils.get(ctx.guild.roles, name='Muted')
                        await member.add_roles(role)
                        emb = discord.Embed(description=f'You have been muted in **Zerodeaths** server for **{reason}**')
                        embed = discord.Embed(title='User muted!', description=f'**{member}** was muted by **{ctx.message.author}** for:\n\n**{reason}**', colour=0xff0000)
                        await ctx.send(embed=embed)
                        await member.send(embed=emb)
                    else:
                        embed = discord.Embed(description='Member already muted')
                        await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author} Used the `userpost` command, Who is not a moderator', colour=0xff0000)
            await channel.send(embed=emb)

    # Mute member: Error handling
    @_mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$mute {member_name}\n      ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')

    # Unmute member

    @commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(member.roles, name='Muted')
            if role is not None:
                await member.remove_roles(role)
                embed = discord.Embed(title='User unmuted!', description='**{0}** was unmuted by **{1}**\n\nDon\'t be naughty again'.format(member, ctx.message.author), colour=0x008000)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'**{str(member)}** not muted lol')
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author}> Used the `userpost` command, Who is not a moderator', colour=0xff0000)
            await channel.send(embed=emb)

    # Unmute member : Error handling

    @_unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$unmute {member_name}\n        ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
        

    # Adding roles

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, role=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if role is None:
                await ctx.send(f"Which role do you want to give to **{str(member)}**? ")
            else:
                add_role = discord.utils.get(ctx.guild.roles, name=role)
                await member.add_roles(add_role)
                embed = discord.Embed(title='**ADDED ROLE**', description=f'**{str(member)}** has been given the role **{role}**', colour=0x008000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author}> Used the `userpost` command, Who is not a moderator', colour=0xff0000)
            await channel.send(embed=emb)

    # Add roles: Error handling

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$addrole {member_name} {role}\n         ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')

    # Remove roles

    @commands.command(aliases=['removerole'])
    async def purgerole(self, ctx, member: discord.Member, role=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if role is None:
                await ctx.send(f"Which role do you want to remove from **{str(member)}**? ")
            else:
                add_role = discord.utils.get(ctx.guild.roles, name=role)
                await member.remove_roles(add_role)
                embed = discord.Embed(title='**REMOVED ROLE**', description=f'**{str(member)}** has **{role}** stripped out cos he doesn\'t deserve it lol', colour=0x008000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author}> Used the `userpost` command, Who is not a moderator', colour=0xff0000)
            await channel.send(embed=emb)

    # Remove roles: Error handling

    @purgerole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('```\n$removerole {member_name} {role}\n            ^^^^^^^^^^^^^\nMissing required Argument member_name\n```')


def setup(bot):
    bot.add_cog(ModerationCog(bot))
