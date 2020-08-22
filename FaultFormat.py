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
# Returns a string
def format_matches(matches):
    # Checks for empty match record
    if matches == []:
        return('No matches found for that player ID')

    # create the output string
    output = ""

    # Iterates through each match
    for i, match in enumerate(matches):
        # Inits some useful vars when formatting
        team0 = []
        team1 = []
        AveELO0 = 0
        AveELO1 = 0

        # Adds the match length and match ID
        output += '\n\nLength: {0} [ID: {1}]\n'.format(match['TimeLength'], str(match['ID']))
        
        # Iterates through players in the match
        for player in match['players']:
            # Gets the player MMR information
            player_elo = f.get_elo(player['PlayerID'])
            # Creates a string to add to the output
            player_string = '\n - {0} ({1}: {2} [{3}] ELO, Rank {4})'.format(f.heroes[player['HeroID']], player['Username'], player_elo['MMR'], player["MMRChange"], player_elo['ranking'])
            # Sorts players into teams and adds ELO
            if player['Team'] == 0:
                team0.append(player_string)
                AveELO0 += player_elo['MMR']
            else:
                team1.append(player_string)
                AveELO1 += player_elo['MMR']
        
        # Averages ELO across 5 players
        AveELO0 = int(AveELO0/5)
        AveELO1 = int(AveELO1/5)

        # Adds the teams to output with headers
        output += 'Team 1 ({0} Average ELO):'.format(AveELO0)
        for player in team0:
            output += player
        output += '\n\nTeam 2 ({0} Average ELO):'.format(AveELO1)
        for player in team1:
            output += player

        # adds a seperator for multiple matches
        if i < len(matches)-1:
            output += '\n\n-------------'
        
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



