# Rexbot
[![License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](CHANGELOG)

A discord bot coded in `Python` for moderation and some fun.  
The bot's command prefix is `r$`.  
discord.py version : `1.4.2`

## Downloading

```
git clone https://github.com/0xcabrex/Rexbot
cd Rexbot/
chmod +x bot.py
```

## Requirements

```
cd Rexbot/
sudo pip3 install -r requirements.txt
```
OR
```
cd Rexbot/
sudo python3 -m pip install -r requirements.txt
```

## Running the bot

```
cd Rexbot/
./bot.py
```
OR
```
cd Rexbot/
python3 bot.py
```


## Supported commands

### Fun commands

- `8ball` - Gives a yes, no or a maybe to a question asked, completely random but fun ;) 
- `meme` - Sends you a beautifully crafted meme
- `dog | doggo | pupper` - Gets you a cute pupper using internet magic
- `cat | kitty` - Gets you an adorable kitty picture from the internet
- `asciify` - ASCIIfies your message.
- `wikipedia | wiki | ask | whatis` - Gets you information from the wiki
- `howdoi` - Information from stackoverflow

### Moderation commands

- `kick` - Kicks the mentioned user from the guild
- `multikick` - Kicks Multiple people out of the guild
- `ban | hardban` - Bans the infracted user from the guild, **with purging the member's messages**
- `softban` - Bans the infracted user from the guild, **without purging the member's messages**
- `multiban` - Bans multiple users out of the guild
- `unban` - Unbans the user from the guild
- `mute` - Mutes the mentioned user 
- `unmute` - unmutes the mentioned user, if muted
- `clear | remove | purge` - Clears messages from the channel where the command has been used
- `addrole` - adds the role to the user, if present in the guild (**CASE SENSITIVE**)
- `removerole | purgerole` - Removes the role from the user, if present in the guild and if the user has it (**CASE SENSITIVE**)

### Utility commands

- `avatar | av` - Shows the avatar of the user mentioned
- `userinfo | ui` - Gives the info of the user entered
- `serverinfo | si` - Gives the info of the server
- `servercount | sc` - Shows you how many servers the bot is in and total number of members in those servers combined


### Want to add my bot to your discord server?

Use this [link](https://discord.com/api/oauth2/authorize?client_id=732538419787595846&permissions=8&scope=bot) to invite rexbot to your server!  



For any bugs, please report to me and I will try to fix it, if I have time ':)


### License

[Rexbot](https://github.com/0xcabrex/Rexbot) are licensed under the MIT License as stated in the [LICENSE file](LICENSE)