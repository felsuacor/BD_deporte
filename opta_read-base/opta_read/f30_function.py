import xml.etree.ElementTree as ET
import pandas as pd
from opta_read.auxiliares.f30_aux_funct import players_stats_funct

class F30:

    def __init__(self, path):
        self.path=path
    
    def team_stats(self):
        '''
        Function that returns season stats of a team
        '''
        file=ET.parse(self.path)
        team_dict={}
        for team in file.getroot():
            for stat in team:
                attribute=stat.attrib.get("name")
                value=stat.text
                team_dict[attribute]=[value]
        del team_dict[None]

        team_stats=pd.DataFrame.from_dict(data=team_dict, orient="index", columns=[team.attrib.get("name")])

        return team_stats

    def players_stats(self):
        return players_stats_funct(self.path)
    
