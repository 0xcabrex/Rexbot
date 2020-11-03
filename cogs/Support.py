import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType

class SupportCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	# Bug reporting

	@commands.command(name='bugs', aliases=['bug', 'Bug', 'Bugs'])
	@cooldown(1, 10, BucketType.guild)
	async def bug_report(self, ctx, *, message):

		if len(message) > 20:
			bugs_channel1 = discord.utils.get(self.bot.get_all_channels(), guild__name='Cyber Experimentation Facility', name='bugs')
			bugs_channel2 = discord.utils.get(self.bot.get_all_channels(), guild__name='ZeroDeaths', name='bugs')
			embed = discord.Embed(
						title='BUG REPORTED',
						colour = 0x008000
				)
			embed.add_field(name='Username', value=ctx.message.author)
			embed.add_field(name='User id', value=ctx.message.author.id)
			embed.add_field(name='Bug: ', value=message)

			if bugs_channel1 is not None:
				await bugs_channel1.send(embed=embed)
			elif bugs_channel2 is not None:
				await bugs_channel2.send(embed=embed)
			await ctx.send("Your bug has been reported")
		else:
			await ctx.send("Please enter your bug in more than 20 words, try describing everything\nOr you might have forgotten to use the quotes")


	# Bug reporting: Error handling

	@bug_report.error
	async def bug_report_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please enter the bug to be reported')
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await ctx.send("You didnt close the quotes!")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await ctx.send("Too many quotes!")
		elif isinstance(error, commands.UnexpectedQuoteError):
			await ctx.send("Unexpected quote in non-quoted string")
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error	


	# Invite for the bot

	@commands.command(name='invite', aliases=['invites'])
	@cooldown(1, 5, BucketType.channel)
	async def invite_link(self, ctx):
		
		embed = discord.Embed(
				title = f'Here is the invite link to \nadd me to your server!',
				description = '**[invite me](https://discord.com/oauth2/authorize?client_id=732538419787595846&permissions=8&scope=bot)**',
				colour=0x008000
			)
		embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRKLLYkHj1JJe1fJzP5wuz6K1X2Z4_HZ9gkvw&usqp=CAU')
		await ctx.send(embed=embed)


	# Invite: Error handling
	
	@invite_link.error
	async def invite_link_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Source code to me

	@commands.command(name='source', aliases=['sourcecode'])
	@cooldown(1, 5, BucketType.channel)
	async def source_code(self, ctx):

		embed = discord.Embed(
				title = f'Here is my source code\nGithub page link',
				description = '**[Source code](https://github.com/0xcabrex/Rexbot)**',
				colour=0x008000
			)
		embed.set_thumbnail(url='https://img.pngio.com/github-logo-repository-computer-icons-github-png-download-512-github-logo-png-900_520.jpg')
		await ctx.send(embed=embed)


	# Source code: Error handling

	@source_code.error
	async def source_code_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


	# Support server

	@commands.command(name='supportserver', aliases=['ss'])
	@cooldown(1, 10, BucketType.channel)
	async def support_server(self, ctx):
		
		embed = discord.Embed(
				title = f'Support server link:',
				description = '**[support server](https://discord.gg/Gcv69JM)**',
				colour=0x008000
			)
		await ctx.send(embed=embed)


	# Support server: Error handling
	
	@support_server.error
	async def support_server_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error



def setup(bot):
	bot.add_cog(SupportCog(bot))