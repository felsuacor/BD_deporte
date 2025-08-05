import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Literal

from opta_read.auxiliares.opta_pitch import *
import matplotlib.animation as animation

def possesion(path,possesion_type:Literal["BallPossession","Territorial","TerritorialThird"], interval_length):
    if possesion_type not in ["BallPossession","Territorial","TerritorialThird"]:
        raise ValueError(f"possesion_type must be equal to one of BallPossession, Territorial or TerritorialThird")

    if interval_length not in [5,15,45]:
        raise ValueError(f"interval_length must be equal to one of 5, 15 or 45")


    file=ET.parse(path)
    interval_poss = {}

    root = file.getroot()

    away_team = root.attrib.get("away_team_name")
    home_team = root.attrib.get("home_team_name")

    for possession_wave in root.findall(f".//PossessionWave[@Type='{possesion_type}']"):
        for interval_length in possession_wave.findall(f".//IntervalLength[@Type='{interval_length}']"):
            for interval in interval_length.findall("Interval"):
                # Create a new team_poss dictionary for each interval
                if possesion_type != "TerritorialThird":
                    team_poss = {
                        away_team: float(interval.find('Away').text),
                        home_team: float(interval.find('Home').text)
                    }
                else:
                    team_poss = {
                        away_team: float(interval.find('Away').text),
                        home_team: float(interval.find('Home').text),
                        'middle': float(interval.find('Middle').text)
                    }
                interval_type = interval.attrib.get("Type")
                interval_poss[interval_type] = team_poss

    poss=pd.DataFrame.from_dict(data=interval_poss)

    def plot_pitch_possesion_evolution(color_team1="green", color_team2="blue", animated=True):
        return pitch_possesion_evolution(poss, color_team1="green", color_team2="blue", animated=True)
    
    def plot_line_possesion_evolution():
        return line_possesion_evolution(poss)

    poss.plot_pitch_possesion_evolution=plot_pitch_possesion_evolution
    poss.plot_line_possesion_evolution=plot_line_possesion_evolution
    return poss

def pitch_possesion_evolution(df, color_team1="green", color_team2="blue", animated=True):
    '''
    Function that represents possesion evolution in a Opta Pitch.
    If animated=True, it will show how possesion develops over the time intervals of the match
    If animated=False, it will show mean possesion of the match
    '''

    fig, ax = plt.subplots()
    t = df.columns.tolist()

    team_0=df.index.tolist()[0]
    team_1=df.index.tolist()[1]

    l1=df.loc[team_0,t]
    l2= df.loc[team_1,t]

    if "middle" in df.index.tolist():
        l3=df.loc["middle",t]

    opta_pitch(ax)

    ax.get_yaxis().set_visible(False)

    if animated==False:

        rect1 = patches.Rectangle((0, 0), np.mean(l1), 100, linewidth=1, edgecolor=color_team1, facecolor=color_team1, alpha=0.5)
        rect2 = patches.Rectangle((np.mean(l1), 0), np.mean(l2), 100, linewidth=1, edgecolor=color_team2, facecolor=color_team2, alpha=0.5)

        ax.add_patch(rect1)
        ax.add_patch(rect2)

        text1=ax.text(10,80, f"{team_0}\nmean poss:\n {round(np.mean(l1),2)}%")
        text2=ax.text(80,80, f"{team_1}\nmean poss:\n {round(np.mean(l2),2)}%")

        if "middle" in df.index.tolist():
            text3=ax.text(52,80, f"Middle\nmean poss:\n {round(np.mean(l3),2)}%")

        plt.title("Mean possesion of the match")

        ax.set( xlim=[0, 100], ylim=[0, 100],xlabel='Possesion')
        ax.legend()
    
    else:
        rect1 = patches.Rectangle((0, 0), l1[0], 100, linewidth=1, edgecolor=color_team1, facecolor=color_team1, alpha=0.5)
        rect2 = patches.Rectangle((l1[0], 0), l2[0], 100, linewidth=1, edgecolor=color_team2, facecolor=color_team2, alpha=0.5)
        ax.add_patch(rect1)
        ax.add_patch(rect2)

        text1=ax.text(10,80, f"{team_0} poss:\n {l1[0]}%")
        text2=ax.text(80,80, f"{team_1} poss:\n {l1[0]}%")

        if "middle" in df.index.tolist():
            text3=ax.text(52,80, f"Middle poss:\n {l3[0]}%")

        plt.title(f"Possesion in interval time {t[0]}")

        ax.set( xlim=[0, 100], ylim=[0, 100],xlabel='Possesion')
        ax.legend()

        def update(frame):
            # for each frame, update the data stored on each artist.
            # update the line1 plot:
            new_width1 = l1[frame]  # animate between 1 and 3
            rect1.set_width(new_width1)
            text1.set_text(f"{team_0} poss:\n {l1[frame]}%")

            new_width2 = l2[frame]  # animate between 1 and 3
            rect2.set_x(l1[frame])
            rect2.set_width(new_width2)
            text2.set_text(f"{team_1} poss:\n {l2[frame]}%")

            if "middle" in df.index.tolist():
                text3.set_text(f"Middle poss:\n {l3[frame]}%")

            plt.title(f"Possesion in interval time {t[frame]} minutes")
            # update the line2 plot:
            return (rect1, rect2)


        ani = animation.FuncAnimation(fig=fig, func=update, frames=len(t), interval=2000, repeat_delay=4000)

    plt.show()

def line_possesion_evolution(df):
    '''
    Function that represents possesion evolution in a line plot
    '''
    fig, ax = plt.subplots()
    t = df.columns.tolist()

    team_0=df.index.tolist()[0]
    team_1=df.index.tolist()[1]

    l1=df.loc[team_0,t]
    l2= df.loc[team_1,t]
    if "middle" in df.index.tolist():
        l3=df.loc["middle",t]
        
    ax.plot(t, l1, label=team_0)[0]
    ax.plot(t, l2, label=team_1)[0]
    if "middle" in df.index.tolist():
        ax.plot(t, l3, label="middle")[0]
    ax.set( xlim=[0, len(t)], ylim=[0, 100],xlabel='Interval time (mins)', ylabel='Possesion (%)')
    ax.legend()
    
    
    plt.show()