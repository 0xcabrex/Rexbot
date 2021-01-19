import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType,TextChannelConverter,RoleConverter
from cogs.usefullTools.dbIntegration import *
import asyncio

class ConfigCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# Moderation config

	async def moderation_config(self, ctx):

		mod_channel = None
		if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
			mod_channel = fetch_mod_log_channel(int(ctx.guild.id))["channel_id"]
			mod_channel = self.bot.get_channel(mod_channel)

		embed = discord.Embed(
				title = 'Server config',
				description = 'Type out the channel for moderation logs\nType `none` to delete pre-existing logging\n\n'
							  f'Current moderation logs channel - {mod_channel.mention if mod_channel is not None else mod_channel}\n\n'
							  '**Note: Config will timeout in 1 minute**',
				colour = 0x008000
		)

		sent1 = await ctx.send(embed=embed)

		try: 
			msg1 = await self.bot.wait_for(
					"message",
					check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
					timeout = 60
			)

			if msg1:

				if msg1.content.lower() == 'none':

					done1 = await ctx.send('removed the moderation logging channel, if it exists')
					delete_mod_log_channel(int(ctx.guild.id))

				else:
					converter = TextChannelConverter()
					new_channel = await converter.convert(ctx, f'{msg1.content}')

					done1 = await ctx.send(f"{new_channel.mention} has been made the moderation logging channel successfully")

					insert_mod_log_channel(int(ctx.guild.id), int(new_channel.id))

				return sent1, msg1, done1				

		except asyncio.TimeoutError:
			await sent1.delete()
			embed = discord.Embed(
					title='Server config',
					description='Cancelling server configuration due to timeout\nPrevious entries were logged',
					colour=0xff0000
			)

			await ctx.send(embed=embed)

			return None, None, None

	# join logs config 

	async def join_log_config(self, ctx):
		
		join_channel = None
		if fetch_join_log_channel(int(ctx.guild.id)) is not None:
			join_channel = fetch_join_log_channel(int(ctx.guild.id))["channel_id"]
			join_channel = self.bot.get_channel(join_channel)

		embed = discord.Embed(
				title='Server Config',
				description='Type out the channel for logging when a member joins\nType `none` to delete pre-existing logging\n\n'
							f'Current Joins logging channel - {join_channel.mention if join_channel is not None else join_channel}\n\n'
							'NB: It would be better if you make it a private logging channel\n'
							'**Note: Config will timeout in a minute**',
				colour = 0x008000
		)

		sent2 = await ctx.send(embed=embed)

		try:
			msg2 = await self.bot.wait_for(
					"message",
					check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
					timeout = 60
			)

			if msg2:

				if msg2.content.lower() == 'none':

					done2 = await ctx.send('Removed the moderation join logging channel, if it exists')
					delete_join_log_channel(int(ctx.guild.id))
					
				else:

					converter = TextChannelConverter()
					new_channel = await converter.convert(ctx, f'{msg2.content}')

					done2 = await ctx.send(f'{new_channel.mention} has been made the joins logging channel successfully')

					insert_join_log_channel(int(ctx.guild.id), int(new_channel.id))

				return sent2, msg2, done2

				

		except asyncio.TimeoutError:
			await sent2.delete()

			embed = discord.Embed(
					title='Server config',
					description='Cancelling server configuration due to timeout\nPrevious entries were logged',
					colour=0xff0000
			)

			await ctx.send(embed=embed)

			return None, None, None


	# Leave logs config

	async def leave_log_config(self, ctx):

		leave_channel = None
		if fetch_leave_log_channel(int(ctx.guild.id)) is not None:
			leave_channel = fetch_leave_log_channel(int(ctx.guild.id))["channel_id"]
			leave_channel = self.bot.get_channel(leave_channel)

		embed = discord.Embed(
				title='Server Config',
				description='Type out the channel for logging when a member leaves\nType `none` to delete pre-existing logging\n\n'
							f'Current leaves logging channel - {leave_channel.mention if leave_channel is not None else leave_channel}\n\n'
							'NB: It would be better if you make it a private logging channel\n'
							'**Note: Config will timeout in a minute**',
				colour = 0x008000
		)

		sent3 = await ctx.send(embed=embed)

		try:
			msg3 = await self.bot.wait_for(
					"message",
					check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
					timeout = 60
			)

			if msg3:

				if msg3.content.lower() == 'none':

					done3 = await ctx.send('Removed the moderation leave logging channel, if it exists')
					delete_leave_log_channel(int(ctx.guild.id))

				else:

					converter = TextChannelConverter()
					new_channel = await converter.convert(ctx, f'{msg3.content}')

					done3 = await ctx.send(f'{new_channel.mention} has been made the leaves logging channel successfully')

					insert_leave_log_channel(int(ctx.guild.id), int(new_channel.id))

				return sent3, msg3, done3				

		except asyncio.TimeoutError:
			await sent3.delete()

			embed = discord.Embed(
					title='Server config',
					description='Cancelling server configuration due to timeout\nPrevious entries were logged',
					colour=0xff0000
			)

			await ctx.send(embed=embed)

			return None, None, None


	# Message log channel

	async def message_log_config(self, ctx):

		message_channel = None
		if fetch_message_edit_log_channel(int(ctx.guild.id)) is not None:
			message_channel = fetch_message_edit_log_channel(int(ctx.guild.id))["channel_id"]
			message_channel = self.bot.get_channel(message_channel)

		embed = discord.Embed(
				title='Server Config',
				description='Type out the channel that would log message edits\nType `none` to delete pre-existing channel\n\n'
							f'Existing message edits channel - {message_channel.mention if message_channel is not None else message_channel}\n\n'
							'**Note: Config will timeout in a minute**',
				colour=0x008000
		)

		sent4 = await ctx.send(embed=embed)

		try:
			msg4 = await self.bot.wait_for(
					"message",
					check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
					timeout = 60
			)

			if msg4:

				if msg4.content.lower() == 'none':

					done4 = await ctx.send('Removed the moderation leave logging channel, if it exists')
					delete_leave_log_channel(int(ctx.guild.id))

				else:

					converter = TextChannelConverter()
					new_channel = await converter.convert(ctx, f'{msg4.content}')

					done4 = await ctx.send(f'{new_channel.mention} has been made the message edits logging channel successfully')

					insert_message_edit_log_channel(int(ctx.guild.id), int(new_channel.id))

				return sent4, msg4, done4

		except asyncio.TimeoutError:
			await sent3.delete()

			embed = discord.Embed(
					title='Server config',
					description='Cancelling server configuration due to timeout\nPrevious entries were logged',
					colour=0xff0000
			)

			await ctx.send(embed=embed)

			return None, None, None



	# Mute role config

	async def mute_role_config(self, ctx):

		mute_role = None
		if fetch_mute_role(int(ctx.guild.id)) is not None:
			mute_role = fetch_mute_role(int(ctx.guild.id))["mute_role_id"]
			mute_role = ctx.guild.get_role(mute_role)

		embed = discord.Embed(
				title='Server Config',
				description='Type out the role that would be the role for muting\nType `none` to delete pre-existing role\n\n'
							f'Existing muted role - {mute_role.mention if mute_role is not None else mute_role}\n\n'
							'**Note: Config will timeout in a minute**',
				colour=0x008000
		)

		sent5 = await ctx.send(embed=embed)

		try:
			msg5 = await self.bot.wait_for(
					"message",
					check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
					timeout = 60
			)

			if msg5:

				if msg5.content.lower() == 'none':
					done5 = await ctx.send("Removed the mute role, if it exists")
					delete_mute_role(int(ctx.guild.id))

				else:

					converter = RoleConverter()
					mute_role = await converter.convert(ctx, f'{msg5.content}')

					done5 = await ctx.send(f'{mute_role.mention} has been made the mute role of this server')

					insert_mute_role(int(ctx.guild.id), int(mute_role.id))

				return sent5, msg5, done5

		except asyncio.TimeoutError:
			await sent5.delete()

			embed = discord.Embed(
					title='Server config',
					description='Cancelling server configuration due to timeout\nPrevious entries were logged',
					colour=0xff0000
			)

			await ctx.send(embed=embed)

			return None, None, None

	# ------------------------------------------------------------------breakpoint----------------------------------------------------------


	# Warn threshold

	@commands.command(name='setwarnthresh', aliases=['setwarnthreshold'])
	async def set_warn_threshold(self, ctx, threshold: int):
		if ctx.message.author.guild_permissions.kick_members:
			
			insert_warn_thresh(ctx.guild.id, threshold)
			await ctx.send(f"{ctx.author.mention}, Set warn threshold to **{threshold}** in this server")

		else:
			embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
			await ctx.send(embed=embed)
			channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
			if channel is not None:
				emb = discord.Embed(title='Illegal use of command **setwarnthresh**', description=f'{ctx.author.mention} Used the `setwarnthresh` command, Who is not authorized', colour=0xff0000)
				await channel.send(embed=emb)


	# Warn threshold: Error Handling

	@set_warn_threshold.error
	async def set_warn_threshold_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Please enter just integers")
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Please provide the number for the threshold")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
			raise error


	# Delete warn threshold

	@commands.command(name='delwarnthresh', aliases=['delwarnthreshold', 'clearwarnthresh', 'clearwarnthreshold'])
	async def delete_warn_threshold(self, ctx):
		if ctx.message.author.guild_permissions.kick_members:

			results = fetch_warn_thresh(ctx.guild.id)

			if results is not None:
				warn_thresh = results["threshold"]

				del_warn_thresh(ctx.guild.id)
				await ctx.send(f"Deleted warning threshold in this server\nWas previously {warn_thresh}")
			else:
				await ctx.send(f'{ctx.author.mention}, A warning threshold has not been set on this server\nHence is not removed')


		else:
			embed = discord.Embed(title='**YOU ARE NOT AUTHORIZED**', description="You do not have the authorization to perform this action\n You action will be reported", colour=0xff0000)
			await ctx.send(embed=embed)
			channel = None
			if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
				channel = self.bot.get_channel(fetch_mod_log_channel(int(ctx.guild.id))["channel_id"])
			if channel is not None:
				emb = discord.Embed(title='Illegal use of command **delwarnthresh**', description=f'{ctx.author.mention} Used the `delwarnthresh` command, Who is not authorized', colour=0xff0000)
				await channel.send(embed=emb)


	# Delete warn threshold: Error Handling

	@delete_warn_threshold.error
	async def delete_warn_threshold_error(self, ctx, error):    
		await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
		raise error


	# Server configuration

	@commands.command(name='setup', aliases=['serversetup', 'serverconfig', 'config'])
	@commands.has_permissions(administrator=True)
	@commands.max_concurrency(1, BucketType.guild)
	async def server_config(self, ctx, arg="none"):

		prefix = fetch_prefix(ctx.guild.id)["prefix"]

		if arg.lower() != 'help':
			await ctx.message.delete()

		# Moderation logs config

		if arg.lower() == 'mod' or arg.lower() == 'moderation' or arg.lower() == 'modlog':

			sent1, msg1, done1 = await self.moderation_config(ctx)

			await asyncio.sleep(3)

			if sent1 is None and msg1 is None and done1 is None:
				return

			else:

				mod_channel = None
				if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
					mod_channel = fetch_mod_log_channel(int(ctx.guild.id))["channel_id"]
					mod_channel = self.bot.get_channel(mod_channel)

				embed = discord.Embed(
						title='Configuration complete',
						description=f'Updated the moderation logs channel to {mod_channel.mention if mod_channel is not None else mod_channel}',
						colour=0x008000
				)

				await ctx.send(embed=embed)

			
				await msg1.delete()
				await sent1.delete()
				await done1.delete()
				return

		# joins config	

		elif arg.lower() == 'joins' or arg.lower() == 'join' or arg.lower() == 'joinlog':

			sent2, msg2, done2 = await self.join_log_config(ctx)

			await asyncio.sleep(3)

			if sent2 is None and msg2 is None and done2 is None:
				return

			else:

				join_channel = None
				if fetch_join_log_channel(int(ctx.guild.id)) is not None:
					join_channel = fetch_join_log_channel(int(ctx.guild.id))["channel_id"]
					join_channel = self.bot.get_channel(join_channel)

				embed = discord.Embed(
						title='Configuration complete',
						description=f'Updated the join logs channel to {join_channel.mention if join_channel is not None else join_channel}',
						colour=0x008000
				)

				await ctx.send(embed=embed)
			
				await msg2.delete()
				await sent2.delete()
				await done2.delete()

				return

		# Leaves config		

		elif arg.lower() == 'leaves' or arg.lower() == 'leave' or arg.lower() == 'leavelog' :

			sent3, msg3, done3 = await self.leave_log_config(ctx)

			await asyncio.sleep(3)

			if msg3 is None and msg3 is None and done3 is None:
				return

			else:

				leave_channel = None
				if fetch_leave_log_channel(int(ctx.guild.id)) is not None:
					leave_channel = fetch_leave_log_channel(int(ctx.guild.id))["channel_id"]
					leave_channel = self.bot.get_channel(leave_channel)

				embed = discord.Embed(
						title='Configuration complete',
						description=f'Updated the leave logs channel to {leave_channel.mention if leave_channel is not None else leave_channel}',
						colour=0x008000
				)

				await ctx.send(embed=embed)

			
				await msg3.delete()
				await sent3.delete()
				await done3.delete()

				return

		# Message log channel

		elif arg.lower() == 'msg' or arg.lower() == 'message' or arg.lower() == 'messagelog':

			sent4, msg4, done4 = await self.message_log_config(ctx)

			await asyncio.sleep(3)

			if sent4 is None and msg4 is None and done4 is None:
				return
			else:

				message_channel = None
				if fetch_message_edit_log_channel(int(ctx.guild.id)) is not None:
					message_channel = fetch_message_edit_log_channel(int(ctx.guild.id))["channel_id"]
					message_channel = self.bot.get_channel(message_channel)

				embed = discord.Embed(
						title='Configuration complete',
						description=f'Updated the leave logs channel to {message_channel.mention if message_channel is not None else message_channel}',
						colour=0x008000
				)

				await ctx.send(embed=embed)

				await sent4.delete()
				await msg4.delete()
				await done4.delete()

				return


		# Mute role config		

		elif arg.lower() == 'mute_role' or arg.lower() == 'mute' or arg.lower() == 'muterole':

			sent5, msg5, done5 = await self.mute_role_config(ctx)

			await asyncio.sleep(3)

			if sent5 is None and msg5 is None and done5 is None:
				return
			else:

				mute_role = None
				if fetch_mute_role(int(ctx.guild.id)) is not None:
					mute_role = fetch_mute_role(int(ctx.guild.id))["mute_role_id"]
					mute_role = ctx.guild.get_role(mute_role)

				embed = discord.Embed(
						title='Configuration complete',
						description=f'Updated the mute role to {mute_role.mention if mute_role is not None else mute_role}',
						colour=0x008000
				)

				await ctx.send(embed=embed)

				await msg5.delete()
				await sent5.delete()
				await done5.delete()

				return

		elif arg == 'help':

			prefix = fetch_prefix(int(ctx.guild.id))["prefix"]

			embed = discord.Embed(
					title='Configuration commands',
					description='Here are the various commands for configuring this guild\n\n'
								f'**Usage:** {prefix}config <args>\n'
								'  1) `mod, modlog` - Configures just the moderation logs\n'
								'  2) `join, joinlog` - Configures just the join logs channel\n'
								'  3) `leave, leavelog` - Configures just the leave logs channel\n'
								'  4) `messagelog, msg` - Configures just the message edits\n'
								'  5) `mute, muterole` - Configures just the mute role\n'
								'  6) `help` - Shows you this dialogue\n\n'
								'Applying no arguments will configure everything.',
					colour=0x008000
			)

			await ctx.send(embed=embed)

		else:

			sent1, msg1, done1 = await self.moderation_config(ctx)
			await asyncio.sleep(3)
			if sent1 is None and msg1 is None and done1 is None:
				return

			sent2, msg2, done2 = await self.join_log_config(ctx)
			await asyncio.sleep(3)
			if sent2 is None and msg2 is None and done2 is None:
				return
				
			sent3, msg3, done3 = await self.leave_log_config(ctx)
			await asyncio.sleep(3)
			if sent3 is None and msg3 is None and done3 is None:
				return
				
			sent4, msg4, done4 = await self.message_log_config(ctx)
			await asyncio.sleep(3)
			if sent4 is None and msg4 is None and done4 is None:
				return
				
			sent5, msg5, done5 = await self.mute_role_config(ctx)
			await asyncio.sleep(3)
			if sent5 is None and msg5 is None and done5 is None:
				return

			# Setup complete

			embed = discord.Embed(
					title = 'Server configuration complete',
					description=f'The configuration has been completed, to check the log channels, use command\n'
								f'`{prefix}showconfig` to list all configurations of the server',
					colour = 0x008000
			)
			embed.set_footer(text='made by CABREX with ❤')

			sent = await ctx.send(embed=embed)

			await asyncio.sleep(3)


			# Purging messages

			await done1.delete()
			await sent1.delete()
			await msg1.delete()

			await done2.delete()
			await sent2.delete()
			await msg2.delete()

			await done3.delete()
			await sent3.delete()
			await msg3.delete()

			await done4.delete()
			await sent4.delete()
			await msg4.delete()

			await done5.delete()
			await sent5.delete()
			await msg5.delete()




	# Server configuration: Error handling

	@server_config.error
	async def server_config_error(self, ctx, error):
		if isinstance(error, commands.ChannelNotFound):
			await ctx.send("Channel was not found\nConfig cancelled\nAll previous options were logged, if made")
		elif isinstance(error, commands.RoleNotFound):
			await ctx.send("Role was not found\nConfig cacelled\nAll previous options were logged, if made")
		elif isinstance(error, commands.MaxConcurrencyReached):
			await ctx.send("You can only run this command till it executes")
		elif isinstance(error, commands.CheckFailure):
			await ctx.send("you do not have enough permissions to perform this action ")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
			raise error


	# Show log channels

	@commands.command(name='showconfig')
	@commands.has_permissions(administrator=True)
	async def show_log_channel(self, ctx):

		join_channel = None
		if fetch_join_log_channel(int(ctx.guild.id)) is not None:
			join_channel = fetch_join_log_channel(int(ctx.guild.id))["channel_id"]
			join_channel = self.bot.get_channel(join_channel)

		leave_channel = None
		if fetch_leave_log_channel(int(ctx.guild.id)) is not None:
			leave_channel = fetch_leave_log_channel(int(ctx.guild.id))["channel_id"]
			leave_channel = self.bot.get_channel(leave_channel)

		mod_channel = None
		if fetch_mod_log_channel(int(ctx.guild.id)) is not None:
			mod_channel = fetch_mod_log_channel(int(ctx.guild.id))["channel_id"]
			mod_channel = self.bot.get_channel(mod_channel)

		message_channel = None
		if fetch_message_edit_log_channel(int(ctx.guild.id)) is not None:
			message_channel = fetch_message_edit_log_channel(int(ctx.guild.id))["channel_id"]
			message_channel = self.bot.get_channel(message_channel)

		mute_role = None
		if fetch_mute_role(int(ctx.guild.id)) is not None:
			mute_role = fetch_mute_role(int(ctx.guild.id))["mute_role_id"]
			mute_role = ctx.guild.get_role(mute_role)
		
		embed = discord.Embed(
				title=f'Configurations for {ctx.guild.name}',
				description=f'Logging channels of this server:\n'
							f'1) Infraction logs - {mod_channel.mention if mod_channel is not None else mod_channel}\n'
							f'2) Mod channel for members joining - {join_channel.mention if join_channel is not None else join_channel}\n'
							f'3) Mod channel for members leaving - {leave_channel.mention if leave_channel is not None else leave_channel}\n'
							f'4) Message edits logging channel - {message_channel.mention if message_channel is not None else message_channel}\n'
							f'5) Mute role for muting members - {mute_role.mention if mute_role is not None else mute_role}\n'
		)
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text='made by CABREX with ❤')

		await ctx.send(embed=embed)


	# Show log channels: Error handling

	@show_log_channel.error
	async def show_log_channel_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send("You do not have enough permissions to run this command")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
			raise error


	# # Reaction roles

	# @commands.command(name='rr',aliases=['reactionroles'])
	# @commands.has_permissions(administrator=True)
	# @commands.max_concurrency(1, BucketType.guild)
	# async def reaction_roles(self, ctx):
		
	# 	await ctx.delete()

	# 	await ctx.send(f"Hey! **{ctx.author.name}**\nThis is the setup for reaction roles!")

	# 	# Channel setup

	# 	sent1 = await ctx.send("Which channel do you want it to be in?")

	# 	try:

	# 		msg1 = await self.bot.wait_for(
	# 				"message",
	# 				check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel,
	# 				timeout = 60
	# 		)

	# 		if msg1:

	# 			converter = TextChannelConverter()
	# 			new_channel = await converter.convert(ctx, f'{msg3.content}')

	# 			done1 = await ctx.send(f'Okay, {new_channel.mention} is the channel')


	# 	except:
	# 		await sent1.delete()

	# 		await ctx.send("Timeout! Bye!")

	# 	# The message

		



	# @reaction_roles.error
	# async def reaction_roles_error(self, error):
	# 	if isinstance(error, commands.ChannelNotFound):
	# 		await ctx.send("Channel was not found\nConfig cancelled")
	# 	elif isinstance(error, commands.RoleNotFound):
	# 		await ctx.send("Role was not found\nConfig cacelled")
	# 	elif isinstance(error, commands.MaxConcurrencyReached):
	# 		await ctx.send("You can only run this command till it executes")
	# 	elif isinstance(error, commands.CheckFailure):
	# 		await ctx.send("you do not have enough permissions to perform this action ")
	# 	else:
	# 		await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
	# 		raise error




def setup(bot):
	bot.add_cog(ConfigCog(bot))