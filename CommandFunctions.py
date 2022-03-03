"""
Contains the functions called by the FaultBot.

Written by Chris Quartararo

"""

def create_fault_username_dict(discord_name, fault_name):

    new_fault_name = {discord_name:fault_name}

    return new_fault_name


def add_to_json(ctx, new_fault_name):
    pass


def match_info(ctx):
    """
    Gets match information for the given user.
    Returns an embedded message to be sent by the FaultBot.
    """
    
    msg_author = ctx.author
    return f"Found user {msg_author}"