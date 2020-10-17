import discord
import time
from discord.ext import commands
from discord.ext.commands import MemberConverter
import asyncio


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Kick members

    @commands.command(aliases=['Kick'])
    async def kick(self, ctx, member, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members:

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

                await multiple_member_array[0].kick(reason=reason)
                if reason is None:
                    embed = discord.Embed(title='**USER KICKED**',description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **No Reason Specified**', colour=0xff0000)
                else:
                    embed = discord.Embed(title='**USER KICKED**',description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **{reason}**', colour=0xff0000)
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
        
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **kick**', description=f'{ctx.author.mention} Used the `kick` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)

 
    # Kick members: Error handling

    @kick.error
    async def kick_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send('```\nr$kick {member_name | member_id | member_tag} {reason}\n       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **kick**', description=f'{ctx.author.mention} Used the `kick` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to kick!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error


    # Multi kick

    @commands.command(name = 'multikick', aliases = ['Multikick'])
    async def multikick(self, ctx, *, member):
        if ctx.message.author.guild_permissions.kick_members:

            list_of_users = member.split()
            reason = 'Kicked during a multikick process'

            for member in list_of_users:
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

                    await multiple_member_array[0].kick(reason=reason)
                    embed = discord.Embed(title='**USER KICKED**',description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **{reason}**', colour=0xff0000)
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
        
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **multikick**', description=f'{ctx.author.mention} Used the `multikick` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Multikick: error

    @multikick.error
    async def error_multikick(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:
                await ctx.send('```\nr$multikick ...{member_name | member_id | member_tag} {reason}\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **multikick**', description=f'{ctx.author.mention} Used the `multikick` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to kick!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error

    # Multi ban

    @commands.command(name = 'multiban', aliases = ['Multiban'])
    async def multiban(self, ctx, *, member):
        if ctx.message.author.guild_permissions.ban_members:

            list_of_users = member.split()
            reason = 'Banned during a multiban process'

            for member in list_of_users:
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

                    await multiple_member_array[0].ban(reason=reason)
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', colour=0xff0000)
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
        
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **multiban**', description=f'{ctx.author.mention} Used the `multiban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Multiban: error

    @multiban.error
    async def error_multiban(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:
                await ctx.send('```\nr$multiban ...{member_name | member_id | member_tag} {reason}\n              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **multiban**', description=f'{ctx.author.mention} Used the `multiban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to ban!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error

        

    # Hard ban members

    @commands.command(aliases=['Ban', 'hardban', 'Hardban'])
    async def ban(self, ctx, member, *, reason=None):
        
        if ctx.message.author.guild_permissions.ban_members:
            
                
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
                if reason is None:
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{multiple_member_array[0]}** has been banned due to:\n **No Reason Specified**', colour=0xff0000)
                else:
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', colour=0xff0000)
                await multiple_member_array[0].ban(reason=reason, delete_message_days=7)
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

        
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Hard Ban members: Error handling

    @ban.error
    async def ban_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:                
                await ctx.send('```\nr$ban {member_name | member_id | member_tag} {reason}\n      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member was not found!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to ban !')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        



    # Soft Ban members

    @commands.command(aliases=['Softban'])
    async def softban(self, ctx, member, *, reason=None):
        
        if ctx.message.author.guild_permissions.ban_members:
                
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
                if reason is None:
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{multiple_member_array[0]}** has been banned due to:\n **No Reason Specified**', colour=0xff0000)
                else:
                    embed = discord.Embed(title='**USER BANNED**',description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', colour=0xff0000)
                await multiple_member_array[0].ban(reason=reason)
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

        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `softban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Softban members: Error handling

    @softban.error
    async def ban_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:
                await ctx.send('```\nr$softban {member_name | member_id | member_tag} {reason}\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member was not found!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to ban !')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error        


    # Unban members

    @commands.command(aliases=['Unban'])
    async def unban(self, ctx, *, member):
        
        if ctx.message.author.guild_permissions.ban_members:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            if member_discriminator.isnumeric():
                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await ctx.guild.unban(user)
                        embed = discord.Embed(description=f'***Unbanned user {user.mention}***', colour=0x008000)
                        await ctx.send(embed=embed)
                        return
            else:
                await ctx.send(f'Member discriminator must be an integer, {member_discriminator} not allowed')
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **unban**', description=f'{ctx.author.mention} Used the `unban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Unban mambers: Error handling

    @unban.error
    async def unban_error(self, ctx, error):
        
        if isinstance(error, ValueError):
            if ctx.message.author.guild_permissions.ban_members:
                await ctx.send("Too few arguments\nSyntax: `r$unban <username>#<discriminator>`")
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **unban**', description=f'{ctx.author.mention} Used the `unban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have enough permissions!')
        elif isinstance(error, ValueError):
            await ctx.send("Too few arguments\nSyntax: `$unban <username>#<discriminator>`")
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                
    
    # Clear command
    
    @commands.command(aliases=['remove','purge','Remove','Purge'])
    async def clear(self, ctx, amount: int):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if amount > 0 and amount < 30:
                    await ctx.channel.purge(limit=amount + 1)
                    await asyncio.sleep(0.5)
                    msg = await ctx.send(f"Removed {amount} messages!")
                    await asyncio.sleep(1.5)
                    await msg.delete()
                else:
                    await ctx.send(f'{ctx.message.author.mention}, Enter an amount between 0 and 30, cannot delete {amount} messages!')
            except Exception as e:
                await ctx.send(e)
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **clear**', description=f'{ctx.author.mention} Used the `clear` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Clear command: Error handling
    
    @clear.error
    async def clear_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send(f'How many do you want to remove, {ctx.author.mention}?')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **clear**', description=f'{ctx.author.mention} Used the `clear` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Please enter a valid amount {ctx.message.author.mention}')
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have enough permissions!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                
    
    # Mute members

    @commands.command(aliases=['Mute'])
    async def mute(self, ctx, member, *, reason=None):
        if ctx.message.author.guild_permissions.manage_roles:
            
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
                if str(multiple_member_array[0].name) == str(ctx.author.name):
                    await ctx.send(f"**You can't mute yourself {ctx.author.mention}**")
                else:
                    mute_role_exist = True
                    is_user_muted = False

                    muted1 = discord.utils.get(ctx.guild.roles, name='Muted')

                    for role in multiple_member_array[0].roles:
                        if role.id == muted1.id:
                            is_user_muted = True
                        else:
                            is_user_muted = False

                    if mute_role_exist:
                        if is_user_muted:
                            embed = discord.Embed(title='Already muted', description=f'**{multiple_member_array[0].name}** is already muted!', colour=0xf86000)
                            await ctx.send(embed=embed)
                        else:
                            await multiple_member_array[0].add_roles(muted1)
                            if reason is not None:
                                emb = discord.Embed(title=f'You have been muted in {ctx.guild.name}', description=f'You have been muted in **{ctx.guild.name}** server for **{reason}**', colour=0xff0000)
                                embed = discord.Embed(title='User muted!', description=f'**{multiple_member_array[0]}** was muted by **{ctx.message.author}** for:\n\n**{reason}**', colour=0xff0000)
                            else:
                                emb = discord.Embed(title=f'You have been muted in {ctx.guild.name}', description=f'You have been muted in **{ctx.guild.name}** server for **No Reason At All**', colour=0xff0000)
                                embed = discord.Embed(title='User muted!', description=f'**{multiple_member_array[0]}** was muted by **{ctx.message.author}** for:\n\n**No Reason At All**', colour=0xff0000)
                            await ctx.send(embed=embed)
                            await multiple_member_array[0].send(embed=emb)
                    else:
                        embed = discord.Embed(title='ERROR', description=f'Mute role does not exist in this server!\n I cannot mute {member.mention}', colour=0xff0000)
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
                
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Mute member: Error handling

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:                
                await ctx.send('```\nr$mute {member_name | member_id | member_tag}\n       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('Member does not exist!')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
            
        elif isinstance(error, HTTPException):
            await ctx.send('Cant send DMs!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to mute!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                
    

    # Unmute member

    @commands.command(aliases=['Unmute'])
    async def unmute(self, ctx, member):
        if ctx.message.author.guild_permissions.manage_roles:

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
                role = discord.utils.get(multiple_member_array[0].roles, name='Muted')
                if role is not None:
                    await multiple_member_array[0].remove_roles(role)
                    embed = discord.Embed(title='User unmuted!', description=f'**{multiple_member_array[0]}** was unmuted by **{ctx.message.author}**\n\nDon\'t be naughty again', colour=0x008000)
                    await ctx.send(embed=embed)
                    emb = discord.Embed(title='Unmuted', description=f'You have been unmuted from the server **{multiple_member_array[0].guild.name}**\nDon\'t be naughty again', colour=0x008000)
                    await multiple_member_array[0].send(embed=emb)
                else:
                    embed = discord.Embed(
                        title = 'User not muted',
                        description = f'{multiple_member_array[0].mention} is not muted!',
                        colour=0xf86000
                    )
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
            
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **unmute**', description=f'{ctx.author.mention} Used the `unmute` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Unmute member : Error handling

    @unmute.error
    async def unmute_error(self, ctx, error):        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:         
                await ctx.send('```\nr$unmute {member_name | member_id | member_tag}\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)       
                elif isinstance(error, commands.BadArgument):            
                    await ctx.send('The user does not exist!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to unmute!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                

    # Adding roles

    @commands.command()
    async def addrole(self, ctx, member, *, role=None):
        if ctx.message.author.guild_permissions.manage_roles:

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

                if role is None:
                    await ctx.send(f"Which role do you want to give to **{multiple_member_array[0].name}**? ")
                if member is None:
                    await ctx.send(f'Please enter a valid member\nMember **{multiple_member_array[0].name}** does not exist')
                else:
                    add_role = discord.utils.get(ctx.guild.roles, name=role)
                    if add_role is not None:

                        does_have_role = False
                        
                        for add_role_check in multiple_member_array[0].roles:
                            if add_role == add_role_check:
                                does_have_role = True
                                break
                            else:
                                pass
                                
                        if does_have_role:
                            embed = discord.Embed(title='**USER ALREADY HAS THE ROLE**', description=f'**{multiple_member_array[0]}** already has the role **{role}**', colour=0xf86000)
                            await ctx.send(embed=embed)
                        else:
                            await multiple_member_array[0].add_roles(add_role)
                            embed = discord.Embed(title='**ADDED ROLE**', description=f'**{str(multiple_member_array[0])}** has been given the role **{role}**', colour=0x008000)
                            await ctx.send(embed=embed)

                    elif role is None:
                        pass
                    else:
                        await ctx.send(f'the role **{role}** does not exist!\n**NOTE:** the addrole command is **case sensitive**')

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
            
        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)

    
    # Add roles: Error handling

    @addrole.error
    async def addrole_error(self, ctx, error):        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:            
                await ctx.send('```\nr$addrole {member_name | member_id | member_tag} {role}\n          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough enough permissions to add roles!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                
    

    # Remove roles

    @commands.command(aliases=['removerole'])
    async def purgerole(self, ctx, member, *, role=None):
        
        if ctx.message.author.guild_permissions.manage_roles:

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

                if role is None:
                    await ctx.send(f"Which role do you want to remove from **{str(multiple_member_array[0])}**? ")
                else:
                    remove_role = discord.utils.get(ctx.guild.roles, name=role)
                    if remove_role is not None:

                        does_have_role = False

                        for remove_role_check in multiple_member_array[0].roles:
                            if remove_role == remove_role_check:
                                does_have_role = True
                                break
                            else:
                                pass

                        if does_have_role:
                            await multiple_member_array[0].remove_roles(remove_role)
                            embed = discord.Embed(title='**REMOVED ROLE**', description=f'Removed **{role}** from user **{str(multiple_member_array[0])}**', colour=0x008000)
                            await ctx.send(embed=embed)
                        else:
                            embed = discord.Embed(title='**USER DOES NOT HAVE THE ROLE**', description=f'**{multiple_member_array[0]}** does not have the role **{role}**', colour=0xf86000)
                            await ctx.send(embed=embed)

                    elif role is None:
                        pass
                    else:
                        await ctx.send(f'Role **{role}** does not exist!\n**NOTE**: the removerole/purgerole command is **case sensitive**')

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

        else:
            embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **removerole**', description=f'{ctx.author.mention} Used the `removerole` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Remove roles: Error handling

    @purgerole.error
    async def addrole_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_roles:         
                await ctx.send('```\nr$removerole {member_name | member_id | member_tag} {role}\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
                await ctx.send(embed=embed)
                channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have the enough permissions to remove roles!')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback, or raise an issue to CABREX#4141')
            raise error
        
                    
    

def setup(bot):
    bot.add_cog(ModerationCog(bot))
