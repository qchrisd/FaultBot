"""
This file contains and runs the Discord bot.

Methods include watching for commands and messaging information to users.

Written by Chris Quartararo

"""


# Import packages
import os
from dotenv import load_dotenv  # Package titled python-dotenv
import logging

# Import discord stuff
import discord  # v2.0.0 found at (git+https://github.com/Rapptz/discord.py)
import slash_util  # Requires discord.py 2.0.0+

# Import custom modules
from constants import helpMessage
import CommandFunctions as functions


# Set up logging
logging.basicConfig(filename="FaultBot.log", format="[%(process)d] %(asctime)s - %(message)s", level=logging.INFO)

# Load the environmental variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV')
GUILD = os.getenv('DISCORD_GUILDID_DEV')

# Create the discord bot
bot = slash_util.Bot(command_prefix="/")


# Logging for bot startup functions
@bot.event
async def on_connect():
    """
    Runs when bot is connected to a server.
    """

    logging.info(f'{bot.user} has successfully connected to Discord in server {bot.guilds}.')


@bot.event
async def on_ready():
    """
    Runs when the bot is fully functional and is ready to start being a bot.
    """

    logging.info(f'{bot.user} is ready to recieve commands.')


# Cog for slash_command()s
class cog_commands(slash_util.Cog):

    @slash_util.slash_command(guild_id=GUILD, name="register")
    async def register_fault_username(self, ctx: slash_util.Context, fault_name: str):
        """
        Registers or updates a discord user's name in a JSON for persistent storage.
        """
        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        import json
        try:
            with open("users.json", "r") as file:
                users_json = file.read()
        except FileNotFoundError as e:
            pass
            
        try:
            users_dict = json.loads(users_json)
        except json.decoder.JSONDecodeError as e:
            users_dict = {"guild":{}}
        except UnboundLocalError as e:
            users_dict = {"guild":{}}
        
        new_dict = functions.update_dict(users_dict, guild_id, discord_name, fault_name)

        with open("users.json", "w") as file:
            json_data = json.dumps(new_dict, indent=4)
            file.write(json_data)

        await ctx.send(f"Finished updating fault record")


    @slash_util.slash_command(guild_id=GUILD)
    async def send_test_embed(self, ctx):
        # Creating new test embed
        test = discord.Embed(title='This is the first embed', 
            description='this is the \n multiline description **with markdown**',
            color=discord.Color.purple())

        # Test the footer
        test.set_footer(text='Test for a footer')
        test.set_author(name='FaultBot')
        test.add_field(name='test **field**', value='test **value** \n newline')
        test.add_field(name='test *field* 2', value='value 2')
        test.add_field(name='test field 3', value='value 3', inline=False)

        print(test.to_dict())

        # Test sending the embed
        await ctx.send(embed=test)


    @slash_util.slash_command(guild_id=GUILD, name="match")
    async def match_info(self, ctx):
        test_string = functions.match_info(ctx)
        await ctx.send(test_string)

# Sends hero data to the discord
async def sendHeroes(message, messageParts):

    """Sends the hero usage statistics to the discord channel.
    Currently sorting by "games". Other sort criteria include:
     - wins
     - games
     - kills
     - deaths
     - assists
    """
    # Logging
    # print('Hero data requested')
    logging.info('Hero data requested')

    # Import the proper modules
    import FaultAPI as f
    import FaultFormat as fformat

    # Sets default sortBy criteria
    sortBy = 'games'
    username = str(message.author).split('#')[0]

    # 1 param given, should be a name
    if len(messageParts) == 2:
        # TODO need to add type checking
        if isString(messageParts[1]):
            username = messageParts[1]
        else:
            await message.channel.send("The player name you entered was not a string. Please try again.")
            return
    # 2 params given, should be a name and sort criteria
    elif len(messageParts) > 2:
        if isString(messageParts[1]):
            username = messageParts[1]
        else:
            await message.channel.send("The player name you entered was not a string. Please try again.")
            return
        sortBy = messageParts[2]
    
    # Get Player ID
    player = f.get_id(username)
    # Get the hero data
    heroes = f.get_heroes(player)
    # Sort the hero data
    output = fformat.format_heroes(heroes, sortBy, username)
    # send it to the channel
    await message.channel.send(output)
    return

# Sends match info
# TODO fix the type checking for 3 params
async def sendMatches(message, messageParts):

    # Logging
    logging.info('Match data requested')

    # Initializes the sendback message
    matches = 'No matches found'

    # Import the proper modules
    import FaultAPI as f
    import FaultFormat as fformat

    # No params given
    if len(messageParts) == 1:
        uname_discord = str(message.author).split('#')[0]  # Get username from discord message
        id_fault = f.get_id(uname_discord)  # Get fault ID from the API
        matches = f.get_matches(id_fault, 1)  # Get last match information
    # 1 param given, should be a name
    else:
        # TODO need to add type checking
        if isString(messageParts[1]):
            id_fault = f.get_id(messageParts[1])  # Get fault ID from the API
            matches = f.get_matches(id_fault, 1)  # Get last match information
        else:
            await message.channel.send("The player name you entered was not a string. Please try again.")
            return


    # Creates a discord Embed object from a dictionary to send back ro messager
    formatted_match = fformat.format_matches(matches, id_fault)
    formatted_match['color'] = 0xBF00FF
    embed = discord.Embed.from_dict(formatted_match)

    # Sends the reply to the channel
    await message.channel.send(embed=embed)
    return


# Sends the elo information of the given player
async def send_elo(message, messageParts):

    # Logging
    logging.info('ELO data requested')
    # print('ELO data requested')

    # Import the proper modules
    import FaultAPI as f
    import FaultFormat as fformat
    
    # Message author is the user
    user = str(message.author).split('#')[0]

    # If user is specified in command
    if len(messageParts) >= 2:
        user = messageParts[1]

    # Gets the user ELO information
    id = f.get_id(user)
    player = f.get_elo(id)
    output = fformat.format_elo(player)

    # Send message
    await message.channel.send(output)
    

# Test the embed message functionality of discord
async def send_embed(message, messageParts):
    
    # Creating new test embed
    test = discord.Embed(title='This is the first embed', 
        description='this is the \n multiline description **with markdown**',
        color=discord.Color.purple())

    # Test the footer
    test.set_footer(text='Test for a footer')
    test.set_author(name='FaultBot')
    test.add_field(name='test **field**', value='test **value** \n newline')
    test.add_field(name='test *field* 2', value='value 2')
    test.add_field(name='test field 3', value='value 3', inline=False)

    print(test.to_dict())

    # Test sending the embed
    await message.channel.send(embed=test)

# Add the cog to the bot
bot.add_cog(cog_commands(bot))

# Runs the bot
bot.run(TOKEN)


