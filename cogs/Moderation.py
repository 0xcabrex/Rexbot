import discord
import time
from discord.ext import commands
from discord.ext.commands import MemberConverter
import asyncio
from cogs.usefullTools.dbIntegration import *


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Kick members

    @commands.command(name='kick')
    async def kick(self, ctx, member, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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

                if ctx.guild.me.top_role > multiple_member_array[0].top_role:

                    results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                    if results is not None:
                        delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                    await multiple_member_array[0].kick(reason=reason)
                    if reason is None:
                        embed = discord.Embed(
                                title='**USER KICKED**',
                                description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **No Reason Specified**',
                                colour=0xff0000
                            )

                        user_embed = discord.Embed(
                                title='You have been kicked',
                                description=f'You have been kicked from **{ctx.guild.name}**\n**Reason:** No Reason Specified',
                                colour=0xff0000
                            )
                    else:
                        embed = discord.Embed(
                                title='**USER KICKED**',
                                description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **{reason}**',
                                colour=0xff0000
                            )

                        user_embed = discord.Embed(
                                title='You have been kicked',
                                description=f'You have been kicked from **{ctx.guild.name}**\n**Reason:** {reason}',
                                colour=0xff0000
                            )

                    await ctx.send(embed=embed)
                    try:
                        await multiple_member_array[0].send(embed=user_embed)
                    except:
                        pass
                    await multiple_member_array[0].kick(reason=reason)

                else:
                    await ctx.send(f"My role is either equal to or lesser than **{multiple_member_array[0].display_name}'s** roles\nHence cannot kick")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **kick**', description=f'{ctx.author.mention} Used the `kick` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)

 
    # Kick members: Error handling

    @kick.error
    async def kick_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}kick <member_name | member_id | member_tag> <reason>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **kick**', description=f'{ctx.author.mention} Used the `kick` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to kick!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error


    # Multi kick

    @commands.command(name = 'multikick')
    async def multikick(self, ctx, *, member):
        if ctx.message.author.guild_permissions.kick_members:

            list_of_users = member.split()
            reason = 'Kicked during a multikick process'

            for member in list_of_users:
                if member[0] == '<' and member[1] == '@':
                    converter = MemberConverter()
                    member = await converter.convert(ctx, member)
                elif member.isdigit():
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

                    if ctx.guild.me.top_role > multiple_member_array[0].top_role:

                        results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        if results is not None:
                            delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        
                        embed = discord.Embed(
                            title='**USER KICKED**',
                            description=f'User **{multiple_member_array[0]}** has been kicked due to:\n **{reason}**',
                            colour=0xff0000
                        )

                        user_embed = discord.Embed(
                                title='You have been kicked',
                                description=f'You have been kicked from **{ctx.guild.name}**\n**Reason:** Banned during a multikick process',
                                colour=0xff0000
                            )

                        await ctx.send(embed=embed)
                        try:
                            await multiple_member_array[0].send(embed=user_embed)
                        except:
                            pass
                        await multiple_member_array[0].kick(reason=reason)
                    else:
                        await ctx.send(f"My role is either equal to or lesser than **{multiple_member_array[0].display_name}'s** roles\nHence cannot kick")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **multikick**', description=f'{ctx.author.mention} Used the `multikick` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Multikick: error

    @multikick.error
    async def error_multikick(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.kick_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}multikick ...<member_name | member_id | member_tag> <reason>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **multikick**', description=f'{ctx.author.mention} Used the `multikick` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to kick!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error


    # Multi ban

    @commands.command(name = 'multiban')
    async def multiban(self, ctx, *, member):
        if ctx.message.author.guild_permissions.ban_members:

            list_of_users = member.split()
            reason = 'Banned during a multiban process'

            for member in list_of_users:
                if member[0] == '<' and member[1] == '@':
                    converter = MemberConverter()
                    member = await converter.convert(ctx, member)
                elif member.isdigit():
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

                    if ctx.guild.me.top_role > multiple_member_array[0].top_role:

                        results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        if results is not None:
                            delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        
                        embed = discord.Embed(
                                title='**USER BANNED**',
                                description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', 
                                colour=0xff0000
                        )

                        user_embed = discord.Embed(
                                title='You have been banned',
                                description=f'You have been banned from **{ctx.guild.name}**\n**Reason:** **{reason}**',
                                colour=0xff0000
                            )

                        await ctx.send(embed=embed)
                        try:
                            await multiple_member_array[0].send(embed=user_embed)
                        except:
                            pass
                        await multiple_member_array[0].ban(reason=reason)
                    else:
                        await ctx.send(f"My role is either equal to or lesser than **{multiple_member_array[0].display_name}'s** roles\nHence cannot ban")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            await ctx.send(embed=embed)
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **multiban**', description=f'{ctx.author.mention} Used the `multiban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Multiban: error

    @multiban.error
    async def error_multiban(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}multiban ...<member_name | member_id | member_tag> <reason>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **multiban**', description=f'{ctx.author.mention} Used the `multiban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)            
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have the required permissions to ban!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error

        

    # Hard ban members

    @commands.command(name='ban', aliases=['hardban'])
    async def ban(self, ctx, member, *, reason=None):
        
        if ctx.message.author.guild_permissions.ban_members:
            
                
            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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
                    await ctx.send('What is the reason for the ban?')
                else:
                    if ctx.guild.me.top_role > multiple_member_array[0].top_role:

                        results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        if results is not None:
                            delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        embed = discord.Embed(
                            title='**USER BANNED**'
                            ,description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', 
                            colour=0xff0000
                        )
                        user_embed = discord.Embed(
                                title='You have been banned',
                                description=f'You have been banned from **{ctx.guild.name}**\n**Reason:** **{reason}**',
                                colour=0xff0000
                            )
                        try:
                            multiple_member_array[0].send(embed=user_embed)
                        except:
                            pass
                        await multiple_member_array[0].ban(reason=reason, delete_message_days=7)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"My role is either equal to or lesser than **{multiple_member_array[0].display_name}'s** roles\nHence cannot ban")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Hard Ban members: Error handling

    @ban.error
    async def ban_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}ban <member_name | member_id | member_tag> <reason>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member was not found!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to ban !')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        

    # Soft Ban members

    @commands.command(name='softban')
    async def softban(self, ctx, member, *, reason=None):
        
        if ctx.message.author.guild_permissions.ban_members:
                
            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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
                    await ctx.send("What is the reason for the ban?")
                else:
                    if ctx.guild.me.top_role > multiple_member_array[0].top_role:

                        results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        if results is not None:
                            delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                        embed = discord.Embed(
                            title='**USER BANNED**',
                            description=f'User **{multiple_member_array[0]}** has been banned due to:\n **{reason}**', 
                            colour=0xff0000
                        )

                        user_embed = discord.Embed(
                                title='You have been banned',
                                description=f'You have been banned from **{ctx.guild.name}**\n**Reason:** **{reason}**',
                                colour=0xff0000
                            )
                        try:
                            multiple_member_array[0].send(embed=user_embed)
                        except:
                            pass
                        await multiple_member_array[0].ban(reason=reason, delete_message_days=0)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"My role is either equal to or lesser than **{multiple_member_array[0].display_name}'s** roles\nHence cannot ban")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `softban` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Softban members: Error handling

    @softban.error
    async def ban_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.ban_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}softban <member_name | member_id | member_tag> <reason>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                await ctx.send(embed=embed)
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **ban**', description=f'{ctx.author.mention} Used the `ban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member was not found!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to ban !')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error        


    # Unban members

    @commands.command(name='unban')
    async def unban(self, ctx, *, member):

        if ctx.guild.me.guild_permissions.ban_members:

            prefix = fetch_prefix(ctx.guild.id)["prefix"]
            
            if ctx.message.author.guild_permissions.ban_members:
                banned_users = [e.user for e in await ctx.guild.bans()]
                
                member_name = None
                member_discriminator = None

                if member.isdigit():
                    try:
                        user = (await ctx.guild.fetch_ban(discord.Object(int(member)))).user
                        await ctx.guild.unban(user)
                        embed = discord.Embed(description=f'***Unbanned user {user.mention}***', colour=0x008000)
                        await ctx.send(embed=embed)

                    except discord.NotFound:
                        await ctx.send(f"Member with the id `{member}` was not found to be banned in this server")
                        return
                else:
                
                    if member.find("#") != -1 and member.find("#") != (len(member) + 1):            
                        member_name, member_discriminator = member.split('#')
                    else:
                        await ctx.send(f"```\n{prefix}unban <username>#<discriminator>\nMissing required argument discriminator\n```")
                        return

                    if len(member_discriminator) != 4:
                        await ctx.send(f"Member discriminator must be 4 digits, {len(member_discriminator)} not allowed")
                        return

                    if member_discriminator.isdigit():

                        member_found = False

                        for user in banned_users:

                            if (user.name, user.discriminator) == (member_name, member_discriminator):
                                await ctx.guild.unban(user)
                                embed = discord.Embed(description=f'***Unbanned user {user.mention}***', colour=0x008000)
                                await ctx.send(embed=embed)
                                member_found = True
                                return

                        if member_found is False:

                            embed = discord.Embed(
                                    title='Cannot unban',
                                    description=f'Cannot unban `{member}`, member does not exist or is not banned',
                                    colour=0xff0000
                            )
                            await ctx.send(embed=embed)
                    else:
                        if member_discriminator == '':
                            await ctx.send(f"```\n{prefix}unban <username>#<discriminator>\nMissing required argument discriminator\n```")
                        else:
                            await ctx.send(f'Member discriminator must be an integer, {member_discriminator} not allowed')

            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **unban**', description=f'{ctx.author.mention} Used the `unban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        else:

            embed = discord.Embed(
                    title='Error',
                    description='I do not have enoug permissions to unban members, please give me the ban_members option',
                    colour=0xff0000
            )

            await ctx.send(embed=embed)


    # Unban mambers: Error handling

    @unban.error
    async def unban_error(self, ctx, error):
        
        if isinstance(error, ValueError):
            if ctx.message.author.guild_permissions.ban_members:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f"Too few arguments\nSyntax: `{prefix}unban <username>#<discriminator>`")
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **unban**', description=f'{ctx.author.mention} Used the `unban` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have enough permissions!')
        elif isinstance(error, ValueError):
            await ctx.send("Too few arguments\nSyntax: `$unban <username>#<discriminator>`")
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        
                
    
    # Clear command
    
    @commands.command(name='clear', aliases=['remove','purge'])
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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
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
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **clear**', description=f'{ctx.author.mention} Used the `clear` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Please enter a valid amount {ctx.message.author.mention}')
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have enough permissions!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        
                
    
    # Mute members

    @commands.command(name='mute')
    async def mute(self, ctx, member, *, reason=None):
        if ctx.message.author.guild_permissions.manage_roles:
            
            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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
                    muted1 = None
                    is_user_muted = False

                    if fetch_mute_role(int(ctx.guild.id)) is not None:
                        muted1 = ctx.guild.get_role(fetch_mute_role(int(ctx.guild.id))["mute_role_id"])   #discord.utils.get(ctx.guild.roles, name='Muted')

                    if muted1 is not None:
                        for role in multiple_member_array[0].roles:
                            if role is not None:
                                if role.id == muted1.id:
                                    is_user_muted = True
                                else:
                                    is_user_muted = False
                            else:
                                is_user_muted = False
                            
                    if muted1 is not None:
                        if is_user_muted:
                            embed = discord.Embed(title='Already muted', description=f'**{multiple_member_array[0].name}** is already muted!', colour=0xf86000)
                            await ctx.send(embed=embed)
                        else:
                            if ctx.guild.me.top_role > muted1:
                                await multiple_member_array[0].add_roles(muted1)
                                if reason is not None:
                                    emb = discord.Embed(
                                        title=f'You have been muted in {ctx.guild.name}', 
                                        description=f'You have been muted in **{ctx.guild.name}** server for **{reason}**', 
                                        colour=0xff0000
                                    )
                                    embed = discord.Embed(
                                        title='User muted!', 
                                        description=f'**{multiple_member_array[0]}** was muted by **{ctx.message.author}** for:\n\n**{reason}**', 
                                        colour=0xff0000
                                    )
                                else:
                                    emb = discord.Embed(
                                        title=f'You have been muted in {ctx.guild.name}', 
                                        description=f'You have been muted in **{ctx.guild.name}** server for **No Reason Specified**', 
                                        colour=0xff0000
                                    )
                                    embed = discord.Embed(
                                        title='User muted!', 
                                        description=f'**{multiple_member_array[0]}** was muted by **{ctx.message.author}** for:\n\n**No Reason Specified**', 
                                        colour=0xff0000
                                    )
                                await ctx.send(embed=embed)
                                try:
                                    await multiple_member_array[0].send(embed=emb)
                                except:
                                    pass
                            else:
                                embed = discord.Embed(
                                        title = 'Can not mute!',
                                        description = f'Can not mute {multiple_member_array[0].mention} because the muted role has higher priority than\nMy role\nPlease adjust the roles.',
                                        colour=0xff0000
                                )
                                await ctx.send(embed = embed)
                    else:

                        prefix = fetch_prefix(int(ctx.guild.id))["prefix"]

                        embed = discord.Embed(
                                title='ERROR: Mute role does not exist in this server!',
                                description=f'A mute role is not configure on this server\nPlease configure it with the `{prefix}config` command',
                                colour=0xff0000
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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Mute member: Error handling

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}mute <member_name | member_id | member_tag>\nMissing Required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            if ctx.author.guild_permissions.manage_roles:
                await ctx.send('Member does not exist!')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to mute!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        
                
    

    # Unmute member

    @commands.command(name='unmute')
    async def unmute(self, ctx, member):
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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
                    embed = discord.Embed(
                        title='User unmuted!', 
                        description=f'**{multiple_member_array[0]}** was unmuted by **{ctx.message.author}**\n\nDon\'t be naughty again', 
                        colour=0x008000
                    )
                    await ctx.send(embed=embed)
                    emb = discord.Embed(
                        title='Unmuted', 
                        description=f'You have been unmuted from the server **{multiple_member_array[0].guild.name}**\nDon\'t be naughty again', 
                        colour=0x008000
                    )
                    try:
                        await multiple_member_array[0].send(embed=emb)
                    except:
                        pass

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **unmute**', description=f'{ctx.author.mention} Used the `unmute` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Unmute member : Error handling

    @unmute.error
    async def unmute_error(self, ctx, error):        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}unmute <member_name | member_id | member_tag>\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **mute**', description=f'{ctx.author.mention} Used the `mute` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)       
                elif isinstance(error, commands.BadArgument):            
                    await ctx.send('The user does not exist!')
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough permissions to unmute!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        
                

    # Adding roles

    @commands.command(name='addrole', aliases=['add'])
    async def addrole(self, ctx, member, *, role=None):
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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

                            if ctx.guild.me.top_role > add_role:
                                await multiple_member_array[0].add_roles(add_role)
                                embed = discord.Embed(title='**ADDED ROLE**', description=f'**{str(multiple_member_array[0])}** has been given the role **{role}**', colour=0x008000)
                                await ctx.send(embed=embed)
                            else:
                                await ctx.send(f"I cannot add a role that has a higher priority than mine, **{ctx.author.mention}**")
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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)

    
    # Add roles: Error handling

    @addrole.error
    async def addrole_error(self, ctx, error):        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.guild_permissions.manage_roles:            

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}addrole <member_name | member_id | member_tag> <role>\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have enough enough permissions to add roles!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
        
                
    

    # Remove roles

    @commands.command(name='removerole', aliases=['purgerole'])
    async def purgerole(self, ctx, member, *, role=None):
        
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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
                            if ctx.guild.me.top_role > remove_role:
                                await multiple_member_array[0].remove_roles(remove_role)
                                embed = discord.Embed(title='**REMOVED ROLE**', description=f'Removed **{role}** from user **{str(multiple_member_array[0])}**', colour=0x008000)
                                await ctx.send(embed=embed)
                            else:
                                await ctx.send(f"I cannot remove a role that has a higher priority than mine, **{ctx.author.mention}**")
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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **removerole**', description=f'{ctx.author.mention} Used the `removerole` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)
                
    
    # Remove roles: Error handling

    @purgerole.error
    async def addrole_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_roles:

                prefix = fetch_prefix(ctx.guild.id)["prefix"]

                await ctx.send(f'```\n{prefix}removerole <member_name | member_id | member_tag> <role>\nMissing required Argument member_name\n```')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **addrole**', description=f'{ctx.author.mention} Used the `addrole` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, discord.Forbidden):
            await ctx.send(f'{ctx.author.mention}, I do not have the enough permissions to remove roles!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error



    # Warning user 

    @commands.command(name='warn')
    async def warn(self, ctx, member, *, warning=None):
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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

                guild_id = ctx.guild.id
                member_id = multiple_member_array[0].id
                mod_id = ctx.author.id

                if warning is not None:
                    results = None
                    results = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                    warn_thresh = fetch_warn_thresh(multiple_member_array[0].guild.id)

                    if results is not None and warn_thresh is not None:

                        infraction_count = 0
                        infraction_count = len(results["warning"].split('\n'))
                        warn_thresh_count = warn_thresh["threshold"]

                        embed = discord.Embed(
                                title=f'You have been banned from **{ctx.guild.name}**',
                                description=f'You have been banned from **{ctx.guild.name}** for exceeding `{infraction_count+1}` warnings',
                                colour=0xff0000
                        )

                        embed_1 = discord.Embed(
                                title='You have been warned',
                                description=f'You have been warned for the `{infraction_count+1}th` time in {ctx.guild.name}\n**Reason:** {warning}',
                                colour=0xff0000
                        )

                        if infraction_count >= warn_thresh_count:

                            delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                            await multiple_member_array[0].ban(reason=f"Exceded warning limit of {warn_thresh_count} warnings", delete_message_days=0)
                            await ctx.send(f"**{multiple_member_array[0].display_name}** has been banned for exceeding warning limit of **{warn_thresh_count}** warns")
                            try:                                
                                await multiple_member_array[0].send(embed=embed)
                            except:
                                pass
                        else:
                            insert_warns(guild_id, member_id, mod_id, warning)
                            await ctx.send(f"`{multiple_member_array[0].display_name}` has been warned for the `{infraction_count+1}th` time\n**Reason:** `{warning}`")
                            try:
                                await multiple_member_array[0].send(embed=embed_1)
                            except:
                                pass
                    else:
                        insert_warns(guild_id, member_id, mod_id, warning)
                        await ctx.send(f"`{multiple_member_array[0].display_name}` has been warned for the `{infraction_count+1}` times\n**Reason:** `{warning}`")
                        try:
                            await multiple_member_array[0].send(embed=embed_1)
                        except:
                            pass
                else:
                    await ctx.send(f"What is the warning, **{ctx.author.display_name}**?")


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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **warn**', description=f'{ctx.author.mention} Used the `warn` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Warn user: Error handling

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            prefix = fetch_prefix(ctx.guild.id)["prefix"]

            await ctx.send(f"```\n{prefix}warn <member_name | member_id | member_tag>\nMissing required argument member name\n```")
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error
            

    # Display infractions of the user

    @commands.command(name='warns', aliases=['warnings'])
    async def warns(self, ctx, member):
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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

                try:
                    warnings = fetch_warns(str(multiple_member_array[0].guild.id), str(multiple_member_array[0].id))["warning"].split('\n')
                    moderator_guy = fetch_warns(str(multiple_member_array[0].guild.id), str(multiple_member_array[0].id))["mod_id"].split('\n')

                    warn_list = '\n'.join([warning for warning in warnings])

                    embed = discord.Embed(
                            title=f'Infractions for member {multiple_member_array[0].name}',
                            description = f'Number of Infractions: **{len(warnings)}**',
                            colour=0x808080
                    )

                    embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
                    
                    for i in range(len(warnings)):                        
                        embed.add_field(name=f'{i+1}) {warnings[i]}', value=f'Moderator id: {moderator_guy[i]}', inline=False)

                    await ctx.send(embed=embed)

                except TypeError:
                    await ctx.send(f"no warnings for **{multiple_member_array[0].name}**")

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **warns**', description=f'{ctx.author.mention} Used the `warns` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Display infractions of user: error handling

    @warns.error
    async def warns_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            prefix = fetch_prefix(ctx.guild.id)["prefix"]

            await ctx.send(f'```\n{prefix}warns <member_name | member_id | member_tag>\nMissing required argument member name\n```')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error


    # Clear warnings 

    @commands.command(name='clearwarns', aliases=['clearwarn'])
    async def clearwarns(self, ctx, member):
        if ctx.message.author.guild_permissions.manage_roles:

            if member[0] == '<' and member[1] == '@':
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
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

                data = fetch_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                if data is not None:
                    warnings = data["warning"].split('\n')
                    number_of_infractions = len(warnings)

                    delete = delete_warns(multiple_member_array[0].guild.id, multiple_member_array[0].id)

                    if number_of_infractions == 1:
                        await ctx.send(f"{ctx.author.mention}, cleared **{number_of_infractions}** warning for **{multiple_member_array[0].name}**")
                    else:
                        await ctx.send(f"{ctx.author.mention}, cleared **{number_of_infractions}** warning for **{multiple_member_array[0].name}**")

                else:
                    await ctx.send(f"**{multiple_member_array[0].name}** does not have any infractions to clear")
                

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
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = None
            if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
                channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **clearwarn**', description=f'{ctx.author.mention} Used the `clearwarn` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Clear warnings : Error handling

    @clearwarns.error
    async def clear_warns_error(self, ctx, error):
        if isinstance(error,  commands.MissingRequiredArgument):

            prefix = fetch_prefix(ctx.guild.id)["prefix"]

            await ctx.send(f'```\n{prefix}clearwarns <member_name | member_id | member_tag>\nMssing required argument member name\n```')
        else:    
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error



                        
    

def setup(bot):
    bot.add_cog(ModerationCog(bot))
