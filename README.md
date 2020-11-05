# Rexbot
[![License Badge](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](CHANGELOG)

A discord bot coded in `Python` for moderation and some fun.  
The bot's default command prefix is `r$`.  
discord.py version : `1.5.1`

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

You would also need a few files to run: 

- `token.0` - Contains the bot token.
- `NASA_API_TOKEN.0` - For the Nasa Api [key](https://api.nasa.gov/ "Get your api key here"), the `apod` command requires it.
- `mongodbclient.0` - A file that contains the url to connect to your [MongoDB](https://mongodb.com "MongoDB") cluster.  

NOTE: The files are CASE SENSITIVE, please make sure the files are named exactly as given above and put them in the same folder as the 
`bot.py` file, i.e. in the `Rexbot/` deirectory. You can also replace **ONLY** the `token.0` and `mongodbclient.0` with environment variables, but as `REXBOT_TOKEN` and `DATABASE_CLIENT_URL` respectively.  


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

|        Commmand         |                                 Description                                 |
|:-----------------------:|:---------------------------------------------------------------------------:|
| `8ball`                 | Gives a yes, no or a maybe to a question asked, completely random but fun ;)| 
| `meme`                  | Sends you a beautifully crafted meme.                                       |
| `dog, doggo , pupper`   | Gets you a cute pupper using internet magic.                                |
| `cat, kitty`            | Gets you an adorable kitty picture from the internet.                       |
| `fact, facts`           | Gets you a random animal fact of your choice, if it exists.                 |
| `asciify`               | ASCIIfies your message.                                                     |
| `apod`                  | Gets you an Astronomy Picture of the Day.                                   |
| `joke`                  | A random joke.                                                              |
| `pjoke`                 | Gets you a programming specific joke.                                       |
| `quotes`                | A random quote.                                                             |



### Moderation commands

|        Commands             |                                         Description                                                |
|:---------------------------:|:--------------------------------------------------------------------------------------------------:|
| `kick`                      | Kicks the mentioned user from the guild.                                                           |
| `multikick`                 | Kicks Multiple people out of the guild.                                                            |
| `ban, hardban`              | Bans the infracted user from the guild, **with purging the member's messages**.                    |
| `softban`                   | Bans the infracted user from the guild, **without purging the member's messages**.                 |
| `multiban`                  | Bans multiple users out of the guild.                                                              |
| `unban`                     | Unbans the user from the guild.                                                                    |
| `warn`                      | Warns the user.                                                                                    |
| `warns, warnings`           | Display the warnings of the user mentioned.                                                        |
| `clearwarns`                | Clears the infractions of the mentioned user.                                                      |
| `setwarnthresh(old)`        | Sets the warning threshold for the server, beyond which the member gets banned                     |
| `(clear/del)warnthresh(old)`| Clears the warning threshold of the server                                                         |
| `mute`                      | Mutes the mentioned user.                                                                          |
| `unmute`                    | Unmutes the mentioned user, if muted.                                                              |
| `clear, remove, purge`      | Clears messages from the channel where the command has been used.                                  |
| `addrole`                   | adds the role to the user, if present in the guild (**CASE SENSITIVE**)                            |
| `removerole, purgerole`     | Removes the role from the user, if present in the guild and if the user has it (**CASE SENSITIVE**)|



### Utility commands

|            Commands               |                                          Description                                           |
|:---------------------------------:|:----------------------------------------------------------------------------------------------:|
| `avatar, av`                      | Shows the avatar of the user mentioned.                                                        |
| `userinfo, ui`                    | Gives the info of the user entered.                                                            |
| `serverinfo, si`                  | Gives the info of the server.                                                                  |
| `servercount, sc`                 | Shows you how many servers the bot is in and total number of members in those servers combined.|
| `wikipedia,  wiki, ask, whatis`   | Gets you information from the wiki.                                                            |
| `howdoi`                          | Information from stackoverflow.                                                                |
| `cipher, morse`                   | Converts a string to morse code.                                                               |
| `base64`                          | Encodes your message to base64.                                                                |
| `dbase64`                         | Decodes your base64 encoded message.                                                           |
| `prefix`                          | Changes prefix for that server.                                                                |



### Support commands

|       Commands        |                          Description                                  |
|:---------------------:|:---------------------------------------------------------------------:|
| `bug, bugs`           | Report any bugs found in the bot, You can also direct message the bot.|
| `invite`              | Sends an embeded invite link for the bot.                             |
| `source, sourcecode`  | Sends you a link the redirects you to this github page.               |
| `supportserver, ss`   | Gets the link to the support server so you can ask doubts there.      |



### Want to add my bot to your discord server?

Use this [link](https://discord.com/api/oauth2/authorize?client_id=732538419787595846&permissions=8&scope=bot "Invite me to your server!") to invite rexbot to your server!  

For any bugs, please use the `bug` command and I will try to fix it or raise an issue, if I have the time ':)   

Join the [discord server](https://discord.gg/Gcv69JM "<CyberSpace> Hacking & Coding") for support and other stuff.


### License

[Rexbot](https://github.com/0xcabrex/Rexbot) is licensed under the MIT License as stated in the [LICENSE file](LICENSE)