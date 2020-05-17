# BloodBowl Manager Bot

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes, also the steps to configure to your discord application bot.

## Prerequisites
To build the project it is necessary to have installed the following Python packages:

https://pypi.org/project/discord.py/
```
pip install discord.py
```
https://pypi.org/project/python-dotenv/
```
pip install python-dotenv
```

Also is needed create a application and a bot on Discord. You can do it [here](https://discord.com/developers/applications). For more information about how to create a bot on discord, you can check the [this guide](https://discordpy.readthedocs.io/en/latest/discord.html).

## Configuration
The first thing you should do is copy this file to a new file called .env. You can do it just using the following command:
```
cp .env.sample .env
# OR 
cp .\.env.simple .\.env
```
As you can check on .env file, the following configuration file has been defined:
```
# ------------------------------------------------------------------------------#
#----------------------------Blood Bowl Manager Bot-----------------------------#
# ------------------------------------------------------------------------------#



#-----------------------------Discord Configuration-----------------------------#
DISCORD_TOKEN={DISCORD_TOKEN}
DISCORD_PREFIX=bb2!

#-----------------------------SQLite Configuration------------------------------#
SQLITE_CONNECTION = 'SQLite_BotData.db'

#----------------------------GoblinSpy Configuration----------------------------#
SPYURLBASE = http://www.mordrek.com/goblinSpy/Overview/
```
Once .env file is created, set your bot's token (only on .env file, not in .env.simple file), which you can find in the Bots section of your application settings at https://discord.com/developers/ applications. Remember that you should **NOT** share the bot token with anyone.

## Setup
Execute the script ```setupDB.py``` in order to create the database with the empty tables

## Run
Just execute BloodBowlManager.py on python 3 and wait for the _bot up!_ message. If you dont know how to execute it, just put the following command on the terminal:
```
python3 .\BloodBowlManager.py
```
Invite your bot to your Discord Server and use the bot commands to get the Blood Bowl league data.

## Commands
Currently, the following commands has been implemented:
* **bb2!help** -> Shows bot info with the commands
* **bb2!config** -> Configure a tournament on your Discord Server. Add the tournament name and the league name on quotes as parameters.
     - Example: bb2!config "Liga Salty" "Salty Cup Covid-19"
* **bb2!reset** -> Reset the current league configuration.
* **bb2!teams** -> Shows the current teams of the tournament
* **bb2!round** -> Shows matches from the current round. You can add the round number as parameter to show other round.
     - Example: bb2!round 3


## Developed by
* [Paula (Latra) Gallucci Zurita](https://github.com/latra)
* [Mikel (Mikel) Ocejo](https://github.com/mikel-ocejo)

## Thanks to
* [Andreas (Mordrek) Harrison](https://github.com/mordrek) for [GoblinSpy](http://www.mordrek.com/goblinSpy)
