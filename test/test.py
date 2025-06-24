import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import matplotlib.animation as animation


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

    if animated==False:

        rect = patches.Rectangle((0, 0), l1, 50, linewidth=1, edgecolor='r', facecolor='none')
        line1=ax.add_patch(rect)
        # line1 = ax.plot(t, l1, label=team_0)[0]
        # line2 = ax.plot(t, l2, label=team_1)[0]
        ax.set( xlim=[0, len(t)], ylim=[0, 100],xlabel='Interval time (mins)', ylabel='Possesion')
        ax.legend()
    
    else:
        rect1 = patches.Rectangle((0, 0), l1[0], 50, linewidth=1, edgecolor='r', facecolor='green', alpha=0.5)
        rect2 = patches.Rectangle((l1[0], 0), l2[0], 50, linewidth=1, edgecolor='b', facecolor='blue', alpha=0.5)
        ax.add_patch(rect1)
        ax.add_patch(rect2)

        # line1 = ax.plot(t[0], l1[0], label=team_0)[0]
        # line2 = ax.plot(t[0], l2[0], label=team_1)[0]
        ax.set( xlim=[0, 100], ylim=[0, 100],xlabel='Interval time (mins)', ylabel='Possesion')
        ax.legend()

        def update(frame):
            # for each frame, update the data stored on each artist.
            # update the line1 plot:
            # line1.set_xdata(t[:frame])
            new_width1 = l1[frame]  # animate between 1 and 3
            rect1.set_width(new_width1)
            new_width2 = l2[frame]  # animate between 1 and 3
            rect2.set_x(l1[frame])
            rect2.set_width(new_width2)
            # update the line2 plot:
            # line2.set_xdata(t[:frame])
            # line2.set_ydata(l2[:frame])
            return (rect1, rect2)


        ani = animation.FuncAnimation(fig=fig, func=update, frames=len(t), interval=500, repeat_delay=4000)

    plt.show()

possesion_evolution(possesion)