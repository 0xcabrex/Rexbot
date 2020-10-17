import discord
import random
import os
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request
from discord.ext.commands import MemberConverter
import aiohttp
import asyncio
import pyfiglet
import wikipedia
from howdoi import howdoi


class GeneralCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # the eight ball

    @commands.command(name='8ball')
    @cooldown(1,5,BucketType.channel)
    async def eight_ball(self, ctx, *, question=None):
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

        if question is not None:
            embed = discord.Embed(title='*The 8ball*', description=f'**{ctx.message.author}** asked a question.\n\nThe question was: **{question}**\n\n\n{random.choice(responses)}', colour=0x0000ff)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Ask me a question!')


    # eightball: Error handling

    @eight_ball.error
    async def eightball_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')


    # Help console

    @commands.command()
    @cooldown(1,5,BucketType.channel)
    async def help(self, ctx, argument=None):
        mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
        admin_role = discord.utils.get(ctx.author.roles, name='Administrator')

        fun_embed = discord.Embed(
                title = 'Fun commands for @Rexbot',
                description='**8ball**\nUses AI to give you the best answers to your questions\nUsage: r$8ball {question}\n\n'
                            '**meme**\nSends you a beautifully crafted meme\n\n'
                            '**dog | doggo | pupper**\nGets you a dog picture\n\n'
                            '**cat | kitty**\nGets you a cat picture\n\n'
                            '**asciify**\nASCIIfies your message\nUsage: $asciify {message}\n\n'
                            '**wikipedia | wiki | ask | whatis**\nGets you information from the wiki\nUsage: r$wiki {query}\nQuery is necessary\n\n'
                            '**howdoi**\nInformation from stackoverflow\nUsage: r$howdoi {query}\nQuery is necessary\n\n'
                            '**apod**\nGets you and Astronomy Picture Of the Day\nUsage: r$apod\n\n',
                colour=0x01a901
            )
        fun_embed.set_footer(text='Made by CABREX with ❤')

        utils_embed = discord.Embed(
                title = 'Utility commands for @Rexbot',
                description='**avatar** | **av**\nShows the avatar of the user mentioned\nUsage: r$avatar | $av {member_name | member_tag | member_id}\nIf nothing is provided then it shows your avatar\n\n'
                            '**userinfo | ui**\nGives the info of the mentioned user\nUsage: r$userinfo {member_name | member_tag | member_id}\n\n'
                            '**serverinfo | si**\nGives the info of the server (No arguments required)\n\n'
                            '**servercount | sc**\nShows you how many servers the bot is in and total number of members in those servers combined (No arguments required)\n\n',
                colour=0x01a901
            )

        mod_embed = discord.Embed(
                title = 'Moderation commands for @Rexbot',
                description = '**kick**\nKicks the member out of the server\nUsage: r$kick {member_name | member_id | member_tag} {reason}, reason is not neccessary\n\n'
                              '**multikick**\nKicks multiple users out of the guild\nUsage: r$multikick {member_name | member_id | member_tag}, reason is not needed\n\n'
                              '**ban**\nBans the user from the server,**with purging the messages**\nUsage: r$ban {member_name | member_id | member_tag} {reason}, reason is not necessary\n\n'
                              '**softban**\nBans the user from the server, **without removing the messages**\nUsage: r$softban {member_name | member_id | member_tag} {reason}, reason is not necessary\n\n'
                              '**multiban**\nBans multiple users out of the guild\nUsage: r$multiban {member_name | member_id | member_tag}, reason is not needed\n\n'
                              '**unban**\nUnbans the user, you need to know the member\'s name\nUsage: r$unban {member_name#discriminator}\n\n'
                              '**mute**\nMutes the user\nUsage: r$mute {member_name | member_id | member_tag} {reason}, reason is not necessary\n\n'
                              '**unmute**\nUnmutes the user\nUsage: r$unmute {member_name | member_id | member_tag}\n\n'
                              '**clear | remove | purge**\nClears messages from the channel where it is used\nUsage: r$clear {n} where `n` is the number of messages to be purged\n\n'
                              '**addrole**\nAdds role to member\nUsage: r$addrole {member_name | member_id | member_tag} {role_name}\n\n'
                              '**removerole | purgerole**\nRemoves role from mentioned member\nUsage: r$removerole {member_name | member_id | member_tag} {role_name}',
                colour=0x01a901
            )
        mod_embed.set_footer(text='Made by CABREX with ❤')

        initial_help_dialogue = discord.Embed(
                title = 'Help command',
                description = '`r$help Fun`- Some fun commands\n`r$help Moderation` | `r$help mod` - Moderation commands\n`r$help utils` | `r$help util` - Utility commands',
                colour=0x01a901
            )
        initial_help_dialogue.set_footer(text='Made by CABREX with ❤')

        if argument is None:
            await ctx.send(embed=initial_help_dialogue)
        elif argument.lower() == 'fun':
            await ctx.send(embed=fun_embed)
        elif argument.lower() == 'moderation' or argument.lower() == 'mod':
            await ctx.send(embed=mod_embed)
        elif argument.lower() == 'utils' or argument.lower() == 'util':
            await ctx.send(embed=utils_embed)
        else:
          pass


    # Help console: Error handling

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error


    # Avatar fetcher

    @commands.command(aliases=['av'])
    @cooldown(1,5,BucketType.channel)
    async def avatar(self, ctx, member, override=None):

        if member[0] == '<' and member[1] == '@':
            converter = MemberConverter()
            member = await converter.convert(ctx, member)
        elif member.isnumeric():
            member = int(member)
        else:
            pass

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

        if member is discord.Member:
            if member.isnumeric() and member.lower() == 'me' and override == 'override':
                embed = discord.Embed(colour=0x0000ff)
                embed.set_image(url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)

        elif len(multiple_member_array) == 1:

            if isinstance(member, int):
                embed = discord.Embed(colour=0x0000ff)
                embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
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
    


    # Avatar fetcher: Error handling

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(colour=0x0000ff)
            embed.set_image(url=f'{ctx.author.avatar_url}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error


    # Userinfo

    @commands.command(aliases=['ui', 'Ui'])
    @cooldown(1,5,BucketType.channel)
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
            embed.add_field(name='\nMember Name:', value=multiple_member_array[0])
            embed.add_field(name='\nMember Nickname:', value=multiple_member_array[0].display_name)

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
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send('I am Forbidden from doing this command, please check if `server members intent` is enabled')
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
            raise error


    # Server info

    @commands.command(aliases=['si', 'Si'])
    @cooldown(1,4,BucketType.channel)
    async def serverinfo(self, ctx):
    
        count = 0

        members = await ctx.guild.fetch_members().flatten()

        for people in members:
            if people.bot:
                count = count + 1
        else:
            pass

        embed = discord.Embed(
            title = f'{ctx.guild.name} info',
            colour = 0x0000ff
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name='Owner name:', value=f'<@{ctx.guild.owner_id}>')
        embed.add_field(name='Server ID:', value=ctx.guild.id)

        embed.add_field(name='Server region:', value=ctx.guild.region)
        embed.add_field(name='Members:', value=ctx.guild.member_count)
        embed.add_field(name='bots:', value=count)

        embed.add_field(name='Text Channels:', value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels))

        embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        await ctx.send(embed=embed)



    # Serverinfo: Error handling

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
            raise error
        else:
            await ctx.send(f"An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141.")
            raise error


    # Memes

    @commands.command(aliases=['Meme'])
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


    # Memes: Error handling

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
            raise error


    # Dog pictures

    @commands.command(aliases=['doggo','pupper'])
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


    # Dog pictures: Error handling

    @dog.error
    async def dog_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
            raise error


    # Cat pictures

    @commands.command(aliases=['Cat'])
    @cooldown(1,1,BucketType.channel)
    async def cat(self, ctx):
      
        colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

        cat_url = "http://aws.random.cat/meow"
        async with request("GET", cat_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["file"]
                embed = discord.Embed(
                        colour= random.choice(colour_choices)
                )
                embed.set_image(url=image_link)
                await ctx.send(embed=embed)

            else:
                await ctx.send(f'The API seems down, says {response.status}')


    # Cat pictures: Error handling

    @cat.error
    async def cat_picture_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
            raise error


    # Animal facts

    @commands.command(name='fact', aliases=['facts'])
    async def animal_facts(self, ctx, animal:str):

        colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

        if animal.lower() in {'dog', 'cat', 'bird'}:
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url=f"https://some-random-api.ml/img/{'birb' if animal=='bird' else animal}"
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    description = data["fact"]
                    if len(description) > 2045:
                        description = f'{data["fact"][:2045].strip()}...'
                    else:
                        description = data["fact"]

            embed = discord.Embed(
                title = f'Facts about {animal.lower()}',
                description=description,
                colour=random.choice(colour_choices)
            )

            if image_link is not None:
                embed.set_image(url = image_link)
            embed.set_footer(text='Made by CABREX with ❤')

            await ctx.send(embed=embed)


    # Animal Facts: Error handling

    @animal_facts.error
    async def animal_facts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Which animal do you want the facts for?")
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error 




    # Servercount

    @commands.command(name='servercount', aliases=['Servercount', 'Sc', 'sc'])
    @cooldown(1,1,BucketType.channel)
    async def servercount(self, ctx):
        
        member_count = 0
        for guild in self.bot.guilds:
            member_count += guild.member_count

        await ctx.send(f'Present in `{len(self.bot.guilds)}` servers, moderating `{member_count}` members')

    
    # Servercount: cooldown

    @servercount.error
    async def sc_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error


    # ASCIIfy your message

    @commands.command(name='asciify')
    @cooldown(1,1,BucketType.channel)
    async def asciify_message(self, ctx, *, message=None):
        if message is not None:
            if message[0] == '<' and (message[1] == ':'):
                await ctx.send('im not doing that 😂')
            elif message[0] == '<' and message[1] == '@':
                await ctx.send('im not doing that 😂')
            elif ctx.author.is_on_mobile and len(message) > 8:
                await ctx.send('The output might look a bit weird on your phone! 😅\n Landscape mode might make it look Better')
                msg = pyfiglet.figlet_format(message)
                await ctx.send(f'```css\n{msg}\n```')
            else:
                msg = pyfiglet.figlet_format(message)
                await ctx.send(f'```css\n{msg}\n```')
        else:
            await ctx.send('Whats it you want to asciify?')


    # ASCIIfy: Error handling

    @asciify_message.error
    async def asciify_message_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error


    # Wikipedia support

    @commands.command(name='wikipedia', aliases=['ask', 'whatis', 'wiki'])
    @cooldown(1,2,BucketType.channel)
    async def wiki(self, ctx, *, query=None):
        if query is not None:
            r = wikipedia.page(query)
            embed = discord.Embed(
                title = r.title,
                description = r.summary[0 : 2000],
                colour = 0x808080
            )
            async with ctx.typing():
                await asyncio.sleep(2)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Your query is empty {ctx.author.mention}!\nEnter something!")


    # Wikipedia: Error handling

    @wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, wikipedia.exceptions.DisambiguationError):
            await ctx.send(f'There are many articles that match your query, please be more specific {ctx.author.mention}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error has occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error


    # Howdoi stackoverflow API

    @commands.command(name='howdoi')
    @cooldown(1, 2, BucketType.channel)
    async def howdoi(self, ctx, *, query=None):
        if query is not None:
            parser = howdoi.get_parser()
            arguments = vars(parser.parse_args(query.split(' ')))

            embed = discord.Embed(
                title = f'how to {query}',
                description = howdoi.howdoi(arguments)
            )
            async with ctx.typing():
                await asyncio.sleep(2)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send(f'Your query is empty, please ask a question {ctx.author.mention}')


    # Howdoi: Error Handling

    @howdoi.error
    async def howdoi_error(self, ctx, error):
        await ctx.send(f'An error occured ({error})\nPlease check the console for traceback')
        raise error


    # APOD

    @commands.command(name='apod')
    @cooldown(1,2, BucketType.channel)
    async def apod(self, ctx):

        colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff] 
        

        with open('./NASA_API_TOKEN.0', 'r', encoding='utf-8') as nasa_api_token_file_handle:
            API = nasa_api_token_file_handle.read()

        apod_url = f'https://api.nasa.gov/planetary/apod?api_key={API}'
        data = None

        async with request("GET", apod_url, headers={}) as response:    
            data = await response.json()

        try:
            if len(data["explanation"]) > 2048:
                description = f"{data['explanation'][:2045].strip()}..."
            else:
                description = data["explanation"]
        except KeyError:
            await ctx.send('There is a problem in the content, please try again')

        embed = discord.Embed(
            title=data["title"],
            description=description,
            color=random.choice(colour_choices)
        )
        embed.set_image(url=data["hdurl"])
        embed.set_footer(text=f"by {data['copyright']} ")

        async with ctx.typing():
            await asyncio.sleep(2)
        await ctx.send(embed=embed)


    # APOD: Error handling

    @apod.error
    async def apod_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to CABREX#4141')
            raise error



def setup(bot):
    bot.add_cog(GeneralCog(bot))
