import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from matplotlib import colormaps as cm
from opta_read.auxiliares.defensive_stats import *

class F71_test:

    def __init__(self, path):
        self.path=path
    
    def defensive_stats_aux(self):
        return defensive_stats_funct(path=self.path)
        # return df.get_dataframe()
        
        # self.defensive_stats.plot_defensive_actions=self.plot_defensive_actions

    

    

    