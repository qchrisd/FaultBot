"""
Contains the functions called by the FaultBot.

Written by Chris Quartararo

"""

def register_fault_username(ctx):
    pass

def match_info(ctx):
    """
    Gets match information for the given user.
    Returns an embedded message to be sent by the FaultBot.
    """
    
    msg_author = ctx.author
    return f"Found user {msg_author}"