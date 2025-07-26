import xml.etree.ElementTree as ET
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler


    
def players_stats_funct(path):
    '''
    Function that returns season stats of all players of a team
    '''
    players_dict={}
    player_stats={}
    file=ET.parse(path)

    root=file.getroot()
    for player in root.findall(".//Player"):
        first_name=player.attrib.get("first_name")
        last_name=player.attrib.get("last_name")
        full_name=first_name + " " + last_name
        for stat in player:
            attribute=stat.attrib.get("name")
            value=stat.text
            player_stats[attribute] = float(value) 
        
        players_dict[full_name]=player_stats
        player_stats={}
    
    players_stats=pd.DataFrame.from_dict(data=players_dict, orient="index")

    def plot_compare_players(players, stats, color_player_1, color_player_2):
        return compare_players(players_stats, players, stats, color_player_1, color_player_2)
    player_stats.plot_compare_players=plot_compare_players

    return players_stats

def compare_players(df, players, stats, color_player_1, color_player_2):

    '''
    Function that returns a spider-plot comparing two players in the stats we select.
    We decide to normalize dataframe columns so that the comparison is clear

    Input:
    * df: dataframe with all players stats
    * players: list of players (max length 2) to compare
    * stats: list of stats to compare

    '''

    df=df[stats]
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)


    df1=df_normalized.loc[players[0],stats]
    df2=df_normalized.loc[players[1],stats]

    categories=stats
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
            r=df1.tolist(),
            theta=categories,
            fill='toself',
            marker_color=color_player_1,
            marker_line_color=color_player_1,
            opacity=0.5,
            name=players[0]
    ))
    fig.add_trace(go.Scatterpolar(
            r=df2.tolist(),
            theta=categories,
            marker_color=color_player_2,
            marker_line_color=color_player_2,
            fill='toself',
            opacity=0.5,
            name=players[1]
    ))

    fig.update_layout(
        polar=dict(
        radialaxis=dict(
            visible=True
        ))
    )

    fig.show()