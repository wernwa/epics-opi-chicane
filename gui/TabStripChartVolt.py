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



class TabStripChartVolt(TabStripChart):

    def __init__(self,parent):
        self.parent = parent

        self.tab_name = 'Voltage'
        self.x_label = 'time in seconds'
        self.y_label = 'voltage in Volt'

        # define the xy lists
        # reference list for adjusting the xy-axis
        self.x_list_ref = mquad1.strip_chart_volt_time
        self.y_list_ref = mquad1.strip_chart_volt



        self.pvListNames =[q1_volt.pvname,
                      q2_volt.pvname,
                      q3_volt.pvname,
                      q4_volt.pvname,
                      q5_volt.pvname,
                      q6_volt.pvname,
                      q7_volt.pvname,
                      d1_volt.pvname,
                      d2_volt.pvname,
                    ]
        self.ListNames_to_x_values = {
            q1_volt.pvname : mquad1.strip_chart_volt_time,
            q2_volt.pvname : mquad2.strip_chart_volt_time,
            q3_volt.pvname : mquad3.strip_chart_volt_time,
            q4_volt.pvname : mquad4.strip_chart_volt_time,
            q5_volt.pvname : mquad5.strip_chart_volt_time,
            q6_volt.pvname : mquad6.strip_chart_volt_time,
            q7_volt.pvname : mquad7.strip_chart_volt_time,
            d1_volt.pvname : mdipol1.strip_chart_volt_time,
            d2_volt.pvname : mdipol2.strip_chart_volt_time,
        }
        self.ListNames_to_y_values = {
            q1_volt.pvname : mquad1.strip_chart_volt,
            q2_volt.pvname : mquad2.strip_chart_volt,
            q3_volt.pvname : mquad3.strip_chart_volt,
            q4_volt.pvname : mquad4.strip_chart_volt,
            q5_volt.pvname : mquad5.strip_chart_volt,
            q6_volt.pvname : mquad6.strip_chart_volt,
            q7_volt.pvname : mquad7.strip_chart_volt,
            d1_volt.pvname : mdipol1.strip_chart_volt,
            d2_volt.pvname : mdipol2.strip_chart_volt,
        }
        self.ListNames_to_color = {
            q1_volt.pvname : (1,0,0),
            q2_volt.pvname : (1,0.5,0),
            q3_volt.pvname : (1,0,0.5),
            q4_volt.pvname : (0,1,0),
            q5_volt.pvname : (0.5,1,0),
            q6_volt.pvname : (0,1,0.5),
            q7_volt.pvname : (0,0,1),
            d1_volt.pvname : (0.5,0,1),
            d2_volt.pvname : (0,0.5,1),
        }

        TabStripChart.__init__(self, parent)

