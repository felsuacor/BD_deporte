import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


import matplotlib.animation as animation

from matplotlib.patches import Arc


def opta_pitch(ax):        
    # OPTA PITCH
    # Pitch Outline & Centre Line
    plt.plot([0,0],[0,100], color="black")
    plt.plot([0,100],[100,100], color="black") #upper line x_start x_end y_start y_end
    plt.plot([100,100],[100,0], color="black")
    plt.plot([100,0],[0,0], color="black")
    plt.plot([50,50],[0,100], color="black")

    # Left Penalty Area
    plt.plot([17,17],[78.9,21.1],color="black")
    plt.plot([0,17],[78.9,78.9],color="black")
    plt.plot([17,0],[21.1,21.1],color="black")

    # Right Penalty Area
    plt.plot([100,83],[78.9,78.9],color="black")
    plt.plot([83,83],[78.9,21.1],color="black")
    plt.plot([83,100],[21.1,21.1],color="black")

    # Left 6-yard Box
    plt.plot([0,5.8],[63.2,63.2],color="black")
    plt.plot([5.8,5.8],[63.2,36.8],color="black")
    plt.plot([5.8,0],[36.8,36.8],color="black")

    # Right 6-yard Box
    plt.plot([100,94.2],[63.2,63.2],color="black")
    plt.plot([94.2,94.2],[63.2,36.8],color="black")
    plt.plot([94.2,100],[36.8,36.8],color="black")

    # Prepare Circles OK
    centreCircle = plt.Circle((50,50),9.15,color="black",fill=False)
    centreSpot = plt.Circle((50,50),0.6,color="black")
    leftPenSpot = plt.Circle((11.5,50),0.6,color="black")
    rightPenSpot = plt.Circle((88.5,50),0.6,color="black")

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs based on penalty Spots
    leftArc = Arc((11.5,50),height=18.3,width=18.3,angle=0,
                theta1=310,theta2=50,color="black")
    rightArc = Arc((88.5,50),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")


    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

file=ET.parse('C:/Users/Felix/Desktop/Máster  BD Deporte/Módulo 7 - Proveedores de Datos Deportivos/f28/f28-23-2019-1074825-eventdetails.xml')

interval_poss = {}

root = file.getroot()

away_team = root.attrib.get("away_team_name")
home_team = root.attrib.get("home_team_name")

for possession_wave in root.findall(".//PossessionWave[@Type='BallPossession']"):
    for interval_length in possession_wave.findall(".//IntervalLength[@Type='5']"):
        for interval in interval_length.findall("Interval"):
            # Create a new team_poss dictionary for each interval
            team_poss = {
                away_team: float(interval.find('Away').text),
                home_team: float(interval.find('Home').text)
            }
            interval_type = interval.attrib.get("Type")
            interval_poss[interval_type] = team_poss

possesion=pd.DataFrame.from_dict(data=interval_poss)

def possesion_evolution(df,animated=True):

    fig, ax = plt.subplots()
    t = possesion.columns.tolist()

    team_0=possesion.index.tolist()[0]
    team_1=possesion.index.tolist()[1]

    l1=possesion.loc[team_0,t]
    l2= possesion.loc[team_1,t]

    opta_pitch(ax)
    ax.get_yaxis().set_visible(False)

    if animated==False:

        rect1 = patches.Rectangle((0, 0), np.mean(l1), 100, linewidth=1, edgecolor='r', facecolor='green', alpha=0.5)
        rect2 = patches.Rectangle((np.mean(l1), 0), np.mean(l2), 100, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.5)

        ax.add_patch(rect1)
        ax.add_patch(rect2)

        text1=ax.text(10,80, f"{team_0}\nmean poss:\n {round(np.mean(l1),2)}%")
        text2=ax.text(80,80, f"{team_1}\nmean poss:\n {round(np.mean(l2),2)}%")

        ax.set( xlim=[0, 100], ylim=[0, 100],xlabel='Possesion')
        ax.legend()
    
    else:
        rect1 = patches.Rectangle((0, 0), l1[0], 100, linewidth=1, edgecolor='r', facecolor='green', alpha=0.5)
        rect2 = patches.Rectangle((l1[0], 0), l2[0], 100, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.5)
        ax.add_patch(rect1)
        ax.add_patch(rect2)

        text1=ax.text(10,80, f"{team_0} poss:\n {l1[0]}%")
        text2=ax.text(80,80, f"{team_1} poss:\n {l1[0]}%")

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
            # update the line2 plot:
            return (rect1, rect2)


        ani = animation.FuncAnimation(fig=fig, func=update, frames=len(t), interval=500, repeat_delay=4000)

    plt.show()

possesion_evolution(possesion)