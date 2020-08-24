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
                embed = discord.Embed(title='**USER KICKED**',description=f'User **{member}** has been kicked due to:\n **{reason}**', colour=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(732199652757340283)
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **kick**', description=f'<@&732211099264352268>\n<@{author}> Used the `kick` command, Who is not a moderator', colour=discord.Color.red())
                await channel.send(embed=emb)
        except:
            await ctx.send("<:nope:742029970502713385> You cant kick a mod!")

    # Ban members

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if ctx.message.author.guild_permissions.manage_members:
                if reason is None:
                    await ctx.send("What is the reason for the ban?")
                else:
                    await member.ban(reason=reason)
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{member}** has been banned due to:\n **{reason}**', colour=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(732199652757340283)
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'<@&732211099264352268>\n`<@{author}` Used the `ban` command, Who is not a moderator>', colour=discord.Color.red())
                await channel.send(embed=emb)
        except:
            await ctx.send("<:nope:742029970502713385> I dont have sufficient privelages!")

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
                    embed = discord.Embed(description=f'***Banned user {user.mention}***', colour=discord.Color.green())
                    await ctx.send(embed=embed)
                    return
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
            await ctx.send(embed=embed)
            channel = self.bot.get_channel(732199652757340283)
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **unban**', description=f'<@&732211099264352268>\n`<@{author}` Used the `unban` command, Who is not a moderator>', colour=discord.Color.red())
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
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
            await ctx.send(embed=embed)
            channel = self.bot.get_channel(732199652757340283)
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **clear**', description=f'<@&732211099264352268>\n`<@{author}` Used the `clear` command, Who is not a moderator>', colour=discord.Color.red())
            await channel.send(embed=emb)

    # Announcements

    @commands.command()
    async def userpost(self, ctx, *, message=None):
        try:
            if ctx.message.author.guild_permissions.manage_messages:
                if message is None:
                    await ctx.send("What is the message?")
                else:
                    channel = self.bot.get_channel(732197521711038586)
                    await channel.send(message)
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(732199652757340283)
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n`<@{author}` Used the `userpost` command, Who is not a moderator>', colour=discord.Color.red())
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
                channel = self.bot.get_channel(732197521711038586)
                embed = discord.Embed(title=f'Announcement by **{ctx.message.author}**', description=f'*{message}*', colour=discord.Color.blue())
                await channel.send(embed=embed)
        else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
                await ctx.send(embed=embed)
                channel = self.bot.get_channel(732199652757340283)
                author = message.author.id
                emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n`<@{author}` Used the `userpost` command, Who is not a moderator>', colour=discord.Color.red())
                await channel.send(embed=emb)
        

    # Mute members

    @commands.command(aliases=['mute'])
    async def _mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if reason is None:
                await ctx.send("What is the reason for the mute?")
            else:
                muted = discord.utils.get(ctx.guild.roles, name='Muted')
                if muted is not None:
                    role = discord.utils.get(ctx.guild.roles, name='Muted')
                    await member.add_roles(role)
                    emb = discord.Embed(description=f'You have been muted in **Zerodeaths** server for **{reason}**')
                    embed = discord.Embed(title='User muted!', description=f'**{member}** was muted by **{ctx.message.author}** for:\n\n**{reason}**', colour=discord.Color.red())
                    await ctx.send(embed=embed)
                    await member.send(embed=emb)
                else:
                    embed = discord.Embed(description='Member already muted')
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
            await ctx.send(embed=embed)
            channel = self.bot.get_channel(732199652757340283)
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author} Used the `userpost` command, Who is not a moderator', colour=discord.Color.red())
            await channel.send(embed=emb)

    # Unmute member

    @commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.remove_roles(role)
            embed = discord.Embed(title='User unmuted!', description='**{0}** was unmuted by **{1}**\n\nDon\'t be naughty again'.format(member, ctx.message.author), colour=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=discord.Color.red())
            await ctx.send(embed=embed)
            channel = self.bot.get_channel(732199652757340283)
            author = message.author.id
            emb = discord.Embed(title='Illegal use of command **userpost**', description=f'<@&732211099264352268>\n<@{author}> Used the `userpost` command, Who is not a moderator', colour=discord.Color.red())
            await channel.send(embed=emb)
                        


def setup(bot):
    bot.add_cog(ModerationCog(bot))
