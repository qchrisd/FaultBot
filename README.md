# FaultBot
This is the FaultBot for discord created for lovers of Fault.

The bot pulls information from the PlayFault.com API to deliver match and player information with ease.

This bot utilizes slash commands. To see the available commands, type `/` into the message field and select the FaultBot icon.

## Command List
 - `/register`: Save or change your Fault username so it is easy for the bot to find your information. You do no need to save your username, you will be able to specify a user in the other commands instead.
 - `/unregister`: Deletes your any saved Fault username if you don't want the bot to remember you.
 - `/show_username`: Displays the username FaultBot has saved for you.
 - `/elo`: Displays MMR information. You can use the command by itself to use a saved Fault username or specify a Fault username with the `fault_name` parameter.
 - `/match`: Display the most recent match information. You can use the command by itself to use your saved Fault username or specify a Fault username with the `fault_name` parameter. This command also has the parameters `match_id` and `number` which currently do nothing. They may be utilized in the future.

## Roadmap
This bot utilizes the `discord.py` package to handle bot creation and connection and the `slash_util` extension to handle creating and registering slash commands. These two packages are currently under heavy development so the main goal in the immediate timeframe is to maintain and refactor this bot to keep up with those two packages. 

Below are the list of long term goals for this package.
 - Clean the packages to not include vestigial files from v0.1.
 - Add a help command.
 - Make the `/match` team embeds prettier and more informative.
 - Add functionality to `/match` to specify a number of matches to return.
 - Add a slash command to display player hero information. This may include player win statistics or that may be another command.
 - Add a slash command to display the leaderboard.
 - Add a slash command to display hero information. This may include both the description/stats of the hero and play stats for the hero or that may be two commands.
 - Refactor dictionary keys and .env variables to be imported from the `constants.py` file.


# Fault API
These are the API calls that I have found through website inspection and asking the developers.
  - Get all hero performance and pick rates 
    - https://api.playfault.com/getStatsPerHero *can append /`Rank` to filter for Bronze, Silver, etc...
  - Search for a user 
    - https://api.playfault.com/searchUsers/`fault_username`
  - Search the leaderboards for a user by name
    - https://api.playfault.com/getTopPlayers/50/`User Name`
  - Get info for a specific hero by name
    - https://api.playfault.com/heroData/`Hero Name`
  - Items
    - https://api.playfault.com/items
  - Aspects
    - https://api.playfault.com/aspects
  - Search match history by player ID and number of matches
    - https://api.playfault.com/getMatches/`player ID`/`number of matches`)
  - Gets match data by match id
    - https://api.playfault.com/getMatchData/`match_id`
  - Gets the hero performance for a player ID
    - https://api.playfault.com/getPlayerHeroStats/`player ID`
  - Get the MMR information by player ID
    - https://api.playfault.com/getEloData/`player ID`
  - Get the icon for a hero ability
    - https://api.playfault.com/imagecdn/abilities/`hero`/`ability`.png
  - Get the image for an item
    - https://api.playfault.com/imagecdn/items/`item_id`.jpg
  - Get hero portraits by hero ID
    - https://api.playfault.com/imagecdn/portraits/`Hero ID`.jpg
  - Get URL for player avatar by player ID
    - https://api.playfault.com/userAvatar/`player ID`) *avatarURI holds the link to the avatar
  - Get an avatar by image ID
    - https://api.playfault.com/imagecdn/avatars/`Image ID`.jpg)


# File Descriptions
- `/bot` houses the files for the bot.
  - `fault_bot.py` is the discord bot
  - `cogs.py` holds the slash commands for the bot
  - `cog_helpers.py` has pure functions to format information for the slash commands
  - `logger.py` is a helper to set up the logging package in a predictable way
- `/tests` holds unit tests for the package
- `.env` holds private environment variables that are needed to register slash commands and connect to the server as FaultBot
- `constants.py` will eventually be used to hold API dictionary keys and other things that will be utilized mutlitple times throughout the package. Hopefully this will be much easier to maintain as the API is updated and bugs are found.
- `fault_api.py` interfaces with the PlayFault.com API to provide information for the rest of the bot.
- `requirements.txt` holds the requirements and makes installing on other devices easy.
- `FaultFormat.py` has methods from the v0.1 version and will be removed at a later date.