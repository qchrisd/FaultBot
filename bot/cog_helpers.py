"""
Contains the functions called by the FaultBot.

Written by Chris Quartararo

"""

import bot.logger as log


def create_fault_username_dict(discord_name, fault_name):

    new_fault_name = {discord_name:fault_name}

    return new_fault_name


def update_dict(users_dict, guild_id, discord_name, fault_name):
    """
    Updates a dictionary with either a new entry for a user.
    Returns a dictionary
    """

    if guild_id not in users_dict["guild"].keys():
        users_dict["guild"][guild_id] = {}

    users_dict["guild"][guild_id][discord_name] = fault_name

    return users_dict


def remove_from_dict(users_dict, guild_id, discord_name):
    """
    Removes a discord user from the users.json dictionary.
    """
    
    if guild_id not in users_dict["guild"].keys():
        log.error("Guild not found when trying to remove user.")
        return
    
    user = users_dict["guild"][guild_id].pop(discord_name, -1)

    if user == -1:
        log.error(f"KeyError when looking for the user in {guild_id}.")
    
    return users_dict


def match_info(ctx):
    """
    Gets match information for the given user.
    Returns an embedded message to be sent by the FaultBot.
    """
    
    msg_author = ctx.author
    return f"Found user {msg_author}"