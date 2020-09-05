'''
This program deals with all the formatting of the fault API.

Currently the functionality allows for the following:
- Formatting matches
- Formatting hero stats

To Do:
- Refactor code to by pythonic
- Add type checking and error handling

'''


# Import Fault API for hero and item imports
import FaultAPI as f


# Format and return the matches requested using getMatches()
# Returns a title, description, and footer all as strings
def format_matches(matches, player_id):
    # Checks for empty match record
    if matches == []:
        return('No matches found for that player ID')

    # Gets the match out of the dictionary
    match = matches[0]

    # Gets winning team from the dictionary
    if match['Winner'] == 0:
        winner = 'Team 1'
    else:
        winner = 'Team 2'

    # Creates a dict object to return and adds the title, description, and footer
    output = {}
    output['title'] = "Winners: {0}".format(winner)
    output['description'] = "Length: {0} [ID: {1}]".format(match['TimeLength'], str(match['ID']))
    output['footer'] = ""

    # Creates useful structures for holding data for iterating for each player
    team0 = []
    team1 = []
    AveELO0 = 0
    AveELO1 = 0
    
    # Iterates through players in the match
    for player in match['players']:
        # Gets the player MMR information for the player
        player_elo = f.get_elo(player['PlayerID'])

        # Conditional formatting to make the requester stand out
        if player['PlayerID'] == player_id:
            player_string = '\n - **{0} ({1}: {2} *[{3} change]* ELO, Rank {4})**'.format(f.heroes[player['HeroID']], player['Username'], player_elo['MMR'], player["MMRChange"], player_elo['ranking'])
        else:
            player_string = '\n - **{0}** ({1}: {2} *[{3} change]* ELO, Rank {4})'.format(f.heroes[player['HeroID']], player['Username'], player_elo['MMR'], player["MMRChange"], player_elo['ranking'])
        
        # Sorts players into teams and totals ELO
        if player['Team'] == 0:
            team0.append(player_string)
            AveELO0 += player_elo['MMR']
        else:
            team1.append(player_string)
            AveELO1 += player_elo['MMR']
    
    # Averages ELO across 5 players
    AveELO0 = int(AveELO0/5)
    AveELO1 = int(AveELO1/5)

    # Creates the team titles and content for the output dictionary
    team0_title = '**Team 1** ({0} Average ELO):'.format(AveELO0)
    team0_players = ""
    for player in team0:
        team0_players += player
    team1_title = '\n\n**Team 2** ({0} Average ELO):'.format(AveELO1)
    team1_players = ""
    for player in team1:
        team1_players += player
    
    # Adds the fields to the output dictionary
    output['fields'] = [{'name':team0_title, 'value':team0_players}, {'name':team1_title, 'value':team1_players}]

    # return output string
    return output


# Format player hero preferences
def format_heroes(heroList, sortCriteria, username):
    # TODO add sortCriteria checkign

    # Sort the vi
    heroSorted = sorted(heroList, key=lambda item: item[sortCriteria], reverse=True)

    # output string with the header
    output = "Top Hero Statistics for {0} (Sorted by {1})\n".format(username, sortCriteria)

    # Create each hero line and add it to the output string
    for hero in heroSorted:
        winrate = hero['wins']/hero['games']*100
        totKDA = (hero['kills']+hero['assists'])/hero['deaths']
        heroLine = " - {0} ({1} games): {2:.2f}% ({3:.2f} total KDA)\n".format(hero['hero'], hero['games'], winrate, totKDA)
        output += heroLine

    # Return the dict object
    return output


# Format a player elo for discord
def format_elo(player):

    # Create output string
    output = ""

    # Check if user is bad
    if player == []:
        output = "No player found"
        return output

    # Add player name
    output += "{0}\n".format(player['username'])

    # Add MMR information
    output += "{0} {1} (Rank {2})".format(player['MMR'], player['eloTitle'], player['ranking'])

    return output



