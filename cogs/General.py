import discord
import random
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request


class GeneralCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # the eight ball

    @commands.command(aliases=['8ball'])
    @cooldown(1,3,BucketType.channel)
    async def eight_ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."
                     ]

        embed = discord.Embed(title='*The 8ball*', description=f'**{ctx.message.author}** asked a question.\n\nThe question was: **{question}**\n\n\n{random.choice(responses)}', colour=0x0000ff)
        await ctx.send(embed=embed)

    # Help console

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def help(self, ctx, helprole=None):
        mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
        admin_role = discord.utils.get(ctx.author.roles, name='Administrator')

        general_embed = discord.Embed(
                title = 'Bot commands for @Rexbot',
                description='**8ball**- Uses AI to give you the best answers to your questions\n'
                            '**avatar**- Shows the avatar of the user entered\n'
                            '**userinfo**- Gives the info of the entered user\n'
                            '**serverinfo**- Gives the info of the server\n'
                            '**meme**- Sends a beautiful meme\n'
                            '**dog**-Gets you a dog picture\n',
                colour=0x01a901
            )
        general_embed.set_footer(text='Made by CABREX with ❤')

        mod_embed = discord.Embed(
                title = 'Moderation commands for @Rexbot',
                description = '**help**\ngives you this dialogue\n\n'
                              '**kick**\nKicks the member out of the server\nUsage: $kick {member_name | member_id | member_tag} {reason}, reason is neccessary\n\n'
                              '**ban**\nbans the user from the server\nUsage: $ban {member_name | member_id | member_tag} {reason}, reason is necessary\n\n'
                              '**unban**\nunbans the user, you need to know the member\'s name\nUsage: $unban {member_name#discriminator}\n\n'
                              '**mute**\nmutes the user\nUsage: $mute {member_name | member_id | member_tag} {reason}, reason is necessary\n\n'
                              '**unmute**\nunmutes the user\nUsage: {member_name | member_id | member_tag}\n\n'
                              '**clear | remove | purge**\n clears messages from the channel where it is used\nUsage: $clear {n} where `n` is the number of messages to be purged\n\n'
                              '**embedpost**\nWill post an embedded announcement\nUsage: $embedpost {message}\n\n'
                              '**userpost**\nWill send message instead of you in general\nUsage: $userpost {message}\n\n'
                              '**addrole**\nAdds role to member\nUsage: $addrole {member_name | member_id | member_tag} {role_name}\n\n'
                              '**removerole | purgerole**\nRemoves role from member\nUsage: $removerole {member_name | member_id | member_tag} {role_name}',
                colour=0x01a901
            )
        mod_embed.set_footer(text='Made by CABREX with ❤')

        if (mod_role is not None or admin_role is not None or ctx.message.author.guild_permissions.manage_messages):            
            
            await ctx.send(embed=general_embed)
            user = ctx.author
            await user.send(embed=mod_embed)

        else:

          await ctx.send(embed=general_embed)

    # Avatar fetcher

    @commands.command(aliases=['av'])
    @cooldown(1,5,BucketType.channel)
    async def avatar(self, ctx, member):
      try:

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

          if isinstance(member, int):
            embed = discord.Embed(colour=0x0000ff)
            embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
          else:
            if member is None or multiple_member_array[0].name.lower() == 'me':
              embed = discord.Embed(colour=0x0000ff)
              embed.set_image(url=f'{ctx.author.avatar_url}')
            else:
              embed = discord.Embed(colour=0x0000ff)
              embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
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
      except Exception as e:
        await ctx.send(f'Exception thrown: {e}')


    # Avatar fetcher: Error handling

    @avatar.error
    async def avatar_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=0x0000ff)
        embed.set_image(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
      else:
        await ctx.send(f'{error}')


    # Userinfo

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def userinfo(self, ctx, member):

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

        roles = []
        for role in multiple_member_array[0].roles:
            roles.append(role)

        embed = discord.Embed(
            colour = 0x0000ff,
        )
        embed.set_author(name=f'User Info - {multiple_member_array[0]}')
        embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
        embed.set_footer(text='made by CABREX with ❤')

        embed.add_field(name='ID:', value=multiple_member_array[0].id)
        embed.add_field(name='\nMember Name:', value=multiple_member_array[0].display_name)

        embed.add_field(name='\nCreated at: ', value=multiple_member_array[0].created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
        embed.add_field(name='\nJoined at:', value=multiple_member_array[0].joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        embed.add_field(name=f'\nRoles ({len(roles)})', value=' '.join([role.mention for role in roles]))

        embed.add_field(name='\nBot?', value=multiple_member_array[0].bot)

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


    # Userinfo: Error handling

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('```\n$userinfo {member_name}\n          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
        else:
          await ctx.send(f'**{error}**')


    # Server info

    @commands.command()
    @cooldown(1,4,BucketType.channel)
    async def serverinfo(self, ctx):

        count = 0
        for people in ctx.guild.members:
          if people.bot:
            count = count + 1
          else:
            pass

        embed = discord.Embed(
              title = f'{ctx.guild.name} info',
              colour = 0x0000ff
          )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name='Owner name:', value=ctx.guild.owner.display_name)
        embed.add_field(name='Server ID:', value=ctx.guild.id)

        embed.add_field(name='Server region:', value=ctx.guild.region)
        embed.add_field(name='Members:', value=len(ctx.guild.members))
        embed.add_field(name='bots:', value=count)

        embed.add_field(name='Text Channels:', value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels))

        embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        await ctx.send(embed=embed)


    # Memes

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def meme(self, ctx):

        colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

        meme_url = "https://meme-api.herokuapp.com/gimme?nsfw=false"
        async with request("GET", meme_url, headers={}) as response:
          if response.status==200:
            data = await response.json()
            image_link = data["url"]
          else:
            image_link = None

        async with request("GET", meme_url, headers={}) as response:
          if response.status==200:
            data = await response.json()
            embed = discord.Embed(
              title=data["title"],
              colour=random.choice(colour_choices)
            )
            if image_link is not None:
              embed.set_image(url=image_link)
              await ctx.send(embed=embed)

          else:
            await ctx.send(f"The API seems down, says {response.status}")

    # Dog pictures

    @commands.command()
    @cooldown(1,1,BucketType.channel)
    async def dog(self, ctx):
      
      colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

      dog_url="https://random.dog/woof.json"
      async with request("GET", dog_url, headers={}) as response:
        if response.status == 200:
          data = await response.json()
          image_link = data["url"]
          embed = discord.Embed(
              colour = random.choice(colour_choices)
          )
          embed.set_image(url=image_link)
          await ctx.send(embed=embed)

        else:
          await ctx.send(f"The API seems down, says {response.status}")





def setup(bot):
    bot.add_cog(GeneralCog(bot))
