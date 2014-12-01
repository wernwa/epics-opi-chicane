import os
import pprint
import random
import sys
import wx
import time
import thread
import traceback

# The recommended way to use wx with mpl is with the WXAgg
# backend.
#
import matplotlib
#matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy
import pylab

# Epics imports
from epics import PV
from Experiment import *

from TabStripChart import TabStripChart



class TabStripChartTemp(TabStripChart):

    def __init__(self,parent):
        self.parent = parent

        self.tab_name = 'Temperature'
        self.x_label = 'time in seconds'
        self.y_label = 'temperature in degree'

        # define the xy lists
        # reference list for adjusting the xy-axis
        self.x_list_ref = mquad1.strip_chart_temp_time
        self.y_list_ref = mquad1.strip_chart_temp


        self.pvListNames =[q1_temp.pvname,
                      q2_temp.pvname,
                      q3_temp.pvname,
                      q4_temp.pvname,
                      q5_temp.pvname,
                      q6_temp.pvname,
                      q7_temp.pvname,
                      d1_temp.pvname,
                      d2_temp.pvname,
                    ]
        self.ListNames_to_x_values = {
            q1_temp.pvname : mquad1.strip_chart_temp_time,
            q2_temp.pvname : mquad2.strip_chart_temp_time,
            q3_temp.pvname : mquad3.strip_chart_temp_time,
            q4_temp.pvname : mquad4.strip_chart_temp_time,
            q5_temp.pvname : mquad5.strip_chart_temp_time,
            q6_temp.pvname : mquad6.strip_chart_temp_time,
            q7_temp.pvname : mquad7.strip_chart_temp_time,
            d1_temp.pvname : mdipol1.strip_chart_temp_time,
            d2_temp.pvname : mdipol2.strip_chart_temp_time,
        }
        self.ListNames_to_y_values = {
            q1_temp.pvname : mquad1.strip_chart_temp,
            q2_temp.pvname : mquad2.strip_chart_temp,
            q3_temp.pvname : mquad3.strip_chart_temp,
            q4_temp.pvname : mquad4.strip_chart_temp,
            q5_temp.pvname : mquad5.strip_chart_temp,
            q6_temp.pvname : mquad6.strip_chart_temp,
            q7_temp.pvname : mquad7.strip_chart_temp,
            d1_temp.pvname : mdipol1.strip_chart_temp,
            d2_temp.pvname : mdipol2.strip_chart_temp,
        }
        self.ListNames_to_color = {
            q1_temp.pvname : (1,0,0),
            q2_temp.pvname : (1,0.5,0),
            q3_temp.pvname : (1,0,0.5),
            q4_temp.pvname : (0,1,0),
            q5_temp.pvname : (0.5,1,0),
            q6_temp.pvname : (0,1,0.5),
            q7_temp.pvname : (0,0,1),
            d1_temp.pvname : (0.5,0,1),
            d2_temp.pvname : (0,0.5,1),
        }


        TabStripChart.__init__(self, parent)
