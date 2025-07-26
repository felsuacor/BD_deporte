import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from matplotlib import colormaps as cm
from opta_read.opta_pitch import *

    
def defensive_stats_funct(path):
    '''
    Function that returns defensive stats of a match
    '''
    file=ET.parse(path)
    # Initialize data containers
    data = []

    # Iterate through XML tree
    for game in file.getroot():
        home_team = game.attrib.get("home_team_name")
        away_team = game.attrib.get("away_team_name")

        for team in game:
            team_name = home_team if team.attrib.get("Side") == "Home" else away_team

            for player in team:
                player_name = player.attrib.get("player_name")

                for stat in player:
                    stat_name = stat.tag
                    coords = [[point.attrib.get("x"), point.attrib.get("y")] for point in stat]

                    num_events = len(coords) if stat_name != "DefensiveCoverage" else None

                    data.append([team_name, player_name, stat_name, num_events, coords])

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "Team", "Player", "Defensive Stat", "Number of Defensive Actions", "Coords of Defensive Actions"
    ])

    def plot_defensive_coverages(team, players=None):
        '''
        Function that represents defensive coverage areas for single team or for a list of players

        '''

        # Filter dataframe by team selected and defensive coverage actions
        filtered_df=df[(df["Team"]==team) & (df["Defensive Stat"]=="DefensiveCoverage")]
        filtered_df=filtered_df[["Player","Coords of Defensive Actions"]]
        if players != None: 
            filtered_df=filtered_df[filtered_df["Player"].isin(players)]
        filtered_df.reset_index(inplace=True, drop=True)

        # Generate a color map based on number of records of filtered df

        colors = cm['tab10'].resampled(len(filtered_df))

        fig, ax = plt.subplots()

        # Add opta pitch
        opta_pitch(ax)

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Plot defensive coverage polygons
        for i in range(len(filtered_df)):
            rect1 = patches.Polygon(filtered_df.iloc[i,1], label=filtered_df.iloc[i,0], linewidth=1,edgecolor=colors(i), facecolor=colors(i), alpha=0.5)

            ax.add_patch(rect1)

        if players==None:
            plt.title(f"Defensive coverage of {team}'s players")
        else:
            plt.title(f"Defensive coverage of {' & '.join(players)}")

        ax.legend()
        plt.show()
    df.plot_defensive_coverages=plot_defensive_coverages

    return df




    