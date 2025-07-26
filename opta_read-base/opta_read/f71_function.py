import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from matplotlib import colormaps as cm
from opta_read.auxiliares.f71_aux_funct import defensive_stats_funct

class F71:

    def __init__(self, path):
        self.path=path
    
    def defensive_stats(self):
        return defensive_stats_funct(path=self.path)

    

    

    