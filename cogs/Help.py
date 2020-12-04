import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from cogs.usefullTools.dbIntegration import *


class HelpCog(commands.Cog):


	def __init__(self, bot):
		self.bot = bot


	# Help console

	@commands.command()
	@cooldown(1, 3, BucketType.channel)
	async def help(self, ctx, argument=None, page = None):
		mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
		admin_role = discord.utils.get(ctx.author.roles, name='Administrator')

		prefix = fetch_prefix(ctx.guild.id)["prefix"]

		fun_embed = discord.Embed(
				title = 'Fun commands for @Rexbot',
				description=f'**8ball**\nUses AI to give you the best answers to your questions\n**Usage:** `{prefix}8ball <question>`\n\n'
							f'**meme**\nSends you a beautifully crafted meme\nUsage `{prefix}meme`\n\n'
							f'**dog | doggo | pupper**\nGets you a dog picture\n**Usage:** `{prefix}dog`\n\n'
							f'**cat | kitty**\nGets you a cat picture\n**Usage:** `{prefix}cat`\n\n'
							f'**fact | facts**\nGets you a random animal fact if it exists\n**Usage:** `{prefix}fact <animal>`\n\n'
							f'**asciify**\nASCIIfies your message\n**Usage:** `{prefix}asciify <message>`\n\n'
							f'**apod**\nGets you an Astronomy Picture Of the Day\n**Usage:** `{prefix}apod`\n\n'
							f'**joke**\nRandom joke has been delivered!\n**Usage:** `{prefix}joke`\n\n'
							f'**pjoke**\nGets you a programming related joke\n**Usage:** `{prefix}pjoke`\n\n'
							f'**quotes**\nA random quote\n**Usage:** `{prefix}quote`\n\n',
				colour=0x01a901
			)
		fun_embed.set_footer(text='Made by CABREX with ❤')

		utils_embed = discord.Embed(
				title = 'Utility commands for @Rexbot',
				description=f'**avatar** | **av**\nShows the avatar of the user mentioned\n**Usage:** `{prefix}avatar <member_name | member_tag | member_id>`\nIf nothing is provided then it shows your avatar\n\n'
							f'**userinfo | ui**\nGives the info of the mentioned user\n**Usage:** `{prefix}userinfo <member_name | member_tag | member_id>`\n\n'
							f'**serverinfo | si**\nGives the info of the server\n**Usage:** `{prefix}serverinfo`, No arguments required\n\n'
							f'**servercount | sc**\nShows you how many servers the bot is in and total number of members in those servers combined\n**Usage:** `{prefix}sc`, No arguments required\n\n'
							f'**wikipedia | wiki | ask | whatis**\nGets you information from the wiki\n**Usage:** `{prefix}wiki <query>`\nQuery is necessary\n\n'
							f'**howdoi**\nInformation from stackoverflow\n**Usage:** `{prefix}howdoi <query>`\nQuery is necessary\n\n'
							f'**cipher | morse**\nConverts your message to morse code\n**Usage:** `{prefix}cypher <message>`\n\n'
							f'**base64**\nEncodes your message to base64\n**Usage:** `{prefix}base64 "<message>" <iteration>`\nMessage must be in **quotes**\n\n'
							f'**dbase64**\nDecodes your base64 encoded message\n**Usage:** `{prefix}dbase64 "<message>"`\nMessage must be in **quotes**\n\n'
							f'**qrcode**\nConverts a text to qr code\n**Usage:** `{prefix}qrcode <message>`\n\n'
							f'**qrdecode**\nDecodes the qr code link provided\n**Usage:** `{prefix}qrdecode <url link>`\n\n'
							f'**translate**\nTranslates your messag to your desired language\n**Usage:** `{prefix}translate <source_anguage> <destination_language> <text>`\n\n'
							f'**prefix**\nChanges the prefix of the server\n**Usage:** `{prefix}prefix <prefix>`\n\n'
							f'**botstats**\nShows the bot\'s statistics\n**Usage:** `{prefix}botstats`\n\n',
				colour=0x01a901
			)
		utils_embed.set_footer(text='Made by CABREX with ❤')

		mod_embed = discord.Embed(
				title = 'Moderation commands for @Rexbot\nPage 1',
				description=f'**kick**\nKicks the member out of the server\n**Usage:** `{prefix}kick <member_name | member_id | member_tag> <reason>`, reason is not neccessary\n\n'
							f'**multikick**\nKicks multiple users out of the guild\n**Usage:** `{prefix}multikick <member_name | member_id | member_tag>`, reason is not needed\n\n'
							f'**ban | hardban**\nBans the user from the server, **purging the messages**\n**Usage:** `{prefix}ban <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**softban**\nBans the user from the server, **without removing the messages**\n**Usage:** `{prefix}softban <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**multiban**\nBans multiple users out of the guild\n**Usage:** `{prefix}multiban <member_name | member_id | member_tag>`, reason is not needed\n\n'
							f'**unban**\nUnbans the user, you need to know the member\'s name\n**Usage:** `{prefix}unban <member_name#discriminator>`\n\n'
							f'**warn**\nWarns the user\n**Usage:** `{prefix}warn <member_name | member_id | member_tag> <infraction>`\n\n'
							f'**warns | warnings**\nDisplays the infractions of the user mentioned\n**Usage:** `{prefix}warns <member_name | member_id | member_tag>`\n\n'
							f'**clearwarns | clearwarn**\nClears all the infractions of the user\n**Usage:** `{prefix}clearwarns <member_name | member_id | member_tag>`\n\n'
							f'\nDo `{prefix}help mod 2` to get next page',
				colour=0x01a901
			)
		mod_embed.set_footer(text='Made by CABREX with ❤')

		mod_embed_2 = discord.Embed(
				title = 'Page 2',
				description=f'**mute**\nMutes the user\n**Usage:** `{prefix}mute <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**unmute**\nUnmutes the user\n**Usage:** `{prefix}unmute <member_name | member_id | member_tag>`\n\n'
							f'**clear | remove | purge**\nClears messages from the channel where it is used\n**Usage:** `{prefix}clear <n>` where `n` is the number of messages to be purged\n\n'
							f'**addrole**\nAdds role to member\n**Usage:** `{prefix}addrole <member_name | member_id | member_tag> <role_name>`\n\n'
							f'**removerole | purgerole**\nRemoves role from mentioned member\n**Usage:** `{prefix}removerole <member_name | member_id | member_tag> <role_name>`\n\n',
				colour=0x01a901
			)
		mod_embed_2.set_footer(text='Made by CABREX with ❤')

		config_embed = discord.Embed(
				title = 'Configuration commands for @Rexbot',
				description=f'**setwarnthresh | setwarnthreshold**\nSets the warning threshold for the server, beyond which the member gets banned\n**Usage:** `{prefix}setwarnthresh <integer>`\n\n'
							f'**clearwanthresh(old) | delwarnthresh(old)**\nClears the warning threshold of the server\n**Usage:** `{prefix}clearwarnthresh`\n\n'
							f'**serverconfig | config | serversetup | setup**\nConfigures the channels for moderation logging\n**Usage:** `{prefix}config`\n\n'
							f'**showconfig**\nShows channels that are for logging\n**Usage:** `{prefix}showconfig <args>`\nArgs can be optional (type `help` to get a list)\n\n',
				colour=0x01a901
			)
		config_embed.set_footer(text='Made by CABREX with ❤')

		support_embed = discord.Embed(
				title = 'Support commands for @Rexbot',
				description=f'**bug | bugs**\nFound any bugs? Use this command to report the bugs\n**Usage:** `{prefix}bugs "<message>"`\n\nMessage must be greater than 20 charecters.\nYou can also direct message the bot instead of invoking the command\n\n'
							f'**invite**\nInvite me to your server! 😁\n**Usage:** `{prefix}invite`\n\n'
							f'**source | sourcecode**\nWant to know what was I written in? I\'ll send you a github link 😉\n**Usage:** `{prefix}source`\nNo argument required\n\n'
							f'**supportserver | ss**\nLink to the support server\n**Usage:** `{prefix}ss`\n\n',
				colour=0x01a901
			)
		support_embed.set_footer(text='Made by CABREX with ❤')

		initial_help_dialogue = discord.Embed(
				title = 'Help command',
				description=f'`{prefix}help Fun`\nFun commands\n\n'
							f'`{prefix}help Moderation` | `{prefix}help mod`\nModeration commands\n\n'
							f'`{prefix}help utils` | `{prefix}help util`\nUtility commands\n\n'
							f'`{prefix}help config`\nConfiguration commands\n\n'
							f'`{prefix}help support`\nSupport commands\n\n',
				colour=0x01a901
			)
		initial_help_dialogue.set_footer(text='Made by CABREX with ❤')

		if argument is None:
			await ctx.send(embed=initial_help_dialogue)
		elif argument.lower() == 'fun':
			await ctx.send(embed=fun_embed)
		elif argument.lower() == 'moderation' or argument.lower() == 'mod':

			if page == '1' or page is None:
				await ctx.send(embed=mod_embed)
			elif page == '2':
				await ctx.send(embed=mod_embed_2)
			else:
				await ctx.send(embed=mod_embed)

		elif argument.lower() == 'utils' or argument.lower() == 'util':
			await ctx.send(embed=utils_embed)
		elif argument.lower() == 'support':
			await ctx.send(embed=support_embed)
		elif argument.lower() == 'config':
			await ctx.send(embed=config_embed)
		else:
		  pass


	# Help console: Error handling

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX')
			raise error


def setup(bot):
	bot.add_cog(HelpCog(bot))