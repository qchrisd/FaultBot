''' 
Fault Public API
Written by: Chris Quartararo

This file is a list of all the fault website API links for reference.
When imported it will return dictionaries of these useful things.

The current functionality allows for the following methods:
- Getting a player ID by username
- Get the previous matches of a player
- Get the hero performance data for a player
- Get the MMR/ELO information for a player
- Get item list

To Do:
- hero win statistics and pick rates
- Document aspect labels

'''

# Import dependencies
import urllib3
import json

# create urllib3 pool manager for requests
http = urllib3.PoolManager()


# Gets the list of items from the website
# Returns a dict
def get_items():
    """Gets the list of items from the website."""

    # Gets information from the website
    items_link = "https://api.playfault.com/items"
    items_json = http.request('GET', items_link).data
    try:
        items = json.loads(items_json)
    except:
        items = json.loads(items_json.decode('utf8'))

    return items


# Gets player ID from a username
# Returns an int
def get_id(user):
    """ Returns a player ID from a username. Returns -1 if the username is not found."""
    
    # Get the player ID JSON from the website
    page_link = 'https://api.playfault.com/getTopPlayers/50/{0}'.format(user)
    page_json = http.request("GET", page_link).data
    try:
        page_dict = json.loads(page_json)
    except:
        page_dict = json.loads(page_json.decode('utf8'))
    # Attemt to get the ID from the json
    try:
        id = page_dict['players'][0]['id']
    except:
        id = -1
    
    return(id)


# Gets match data in the format https://api.playfault.com/getMatches/<player ID>/<number of matches>
# Returns a list of dicts
def get_matches(id, n):
    """Gets match data for N matches for a given player ID. Returns a blank list if player ID not found."""
    
    # Check if the ID is good
    if id == -1:
        return []

    # Get the match info from the website
    page_link = 'https://api.playfault.com/getMatches/{0}/{1}'.format(id, n)
    page_json = http.request("GET", page_link).data
    try:
        page_dict = json.loads(page_json)['matches']
    except:
        page_dict = json.loads(page_json.decode('utf8'))['matches']
    
    return page_dict


# Gets player hero data in the format https://api.playfault.com/getPlayerHeroStats/<player ID>
# Returns a list of dicts
def get_heroes(id):
    """Gets hero statistics for a specified player ID. Returns a blank list if player ID is not found."""

    # Check that the ID is good
    if id == -1:
        return []
    
    # Collect info from Fault website and convert json to dict
    page_link = 'https://api.playfault.com/getPlayerHeroStats/{0}'.format(id)
    page_json = http.request("GET", page_link).data
    try:
        page_dict = json.loads(page_json)['heroes']
    except:
        page_dict = json.loads(page_json.decode('utf8'))['heroes']
    
    # Flatten dict into a list of dicts, one for each hero
    hero_dict = []
    for key, value in page_dict.items():
        # Cast key to int because json hero keys arrive as str
        try:
            hName = heroes[int(key)] if int(key) in heroes else 'Not Found'
        except ValueError:
            hName = 'Hero key invalid'
        value['hero'] = hName
        hero_dict.append(value)
    
    return hero_dict


# Gets ELO data of a player in the format https://api.playfault.com/getEloData/<player ID>
# Returns a dict
def get_elo(playerID):
    """Gets the MMR and ELO information for an ID. Returns a blank list if the player ID is not found.
    
    Returns a dict with the following:
    - id (str)
    - username (str)
    - eloTitle (str)
    - MMR (float)
    - ranking (int)
    """
    
    # Check if the player ID is good
    if playerID == -1:
        return []

    # Gets the information from the website
    page_link = 'https://api.playfault.com/getEloData/{0}'.format(playerID)
    page_json = http.request("GET", page_link).data
    try:
        page_dict = json.loads(page_json)
    except:
        page_dict = json.loads(page_json.decode('utf8'))

    return page_dict


# Gets the stats per hero in the format https://api.playfault.com/getStatsPerHero
# Returns a JSON object with the HeroID as the key
def get_hero_stats():

    """Gets hero statistics and creates a dictionary of heroes for use elsewhere"""

    # Get the hero dictionary from the API as a JSON object
    page_link = 'https://api.playfault.com/getStatsPerHero'
    page_json = http.request("GET", page_link).data
    # Parse the json string into a dictionary
    try:
        page_dict = json.loads(page_json)
    except:
        page_dict = json.loads(page_json.decode('utf8'))
    
    # Return the dictionary
    return page_dict['heroes']


# Collects the list of heroes with integer Hero IDs and string names
# This will allow for a simple restart when new heroes are added to the game
hero_stats = get_hero_stats()
heroes = {}
for key, val in hero_stats.items():
    heroes[val["Id"]] = key