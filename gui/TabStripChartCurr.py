# -*- coding: utf-8 -*-
#
#   Strip chart for displaying the current over time
#       This class is derived from TabStripChart.py
#
#   author: Watler Werner
#   email: wernwa@gmail.com
#
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



class TabStripChartCurr(TabStripChart):

    def __init__(self,parent):
        self.parent = parent

        self.tab_name = 'Current'
        self.x_label = 'time in seconds'
        self.y_label = 'current in Ampere'

        # define the xy lists
        # reference list for adjusting the xy-axis
        self.x_list_ref = mquad1.strip_chart_curr_time
        self.y_list_ref = mquad1.strip_chart_curr


        self.pvListNames =[q1_curr.pvname,
                      q2_curr.pvname,
                      q3_curr.pvname,
                      q4_curr.pvname,
                      q5_curr.pvname,
                      q6_curr.pvname,
                      q7_curr.pvname,
                      d1_curr.pvname,
                      d2_curr.pvname,
                    ]
        self.ListNames_to_x_values = {
            q1_curr.pvname : mquad1.strip_chart_curr_time,
            q2_curr.pvname : mquad2.strip_chart_curr_time,
            q3_curr.pvname : mquad3.strip_chart_curr_time,
            q4_curr.pvname : mquad4.strip_chart_curr_time,
            q5_curr.pvname : mquad5.strip_chart_curr_time,
            q6_curr.pvname : mquad6.strip_chart_curr_time,
            q7_curr.pvname : mquad7.strip_chart_curr_time,
            d1_curr.pvname : mdipol1.strip_chart_curr_time,
            d2_curr.pvname : mdipol2.strip_chart_curr_time,
        }
        self.ListNames_to_y_values = {
            q1_curr.pvname : mquad1.strip_chart_curr,
            q2_curr.pvname : mquad2.strip_chart_curr,
            q3_curr.pvname : mquad3.strip_chart_curr,
            q4_curr.pvname : mquad4.strip_chart_curr,
            q5_curr.pvname : mquad5.strip_chart_curr,
            q6_curr.pvname : mquad6.strip_chart_curr,
            q7_curr.pvname : mquad7.strip_chart_curr,
            d1_curr.pvname : mdipol1.strip_chart_curr,
            d2_curr.pvname : mdipol2.strip_chart_curr,
        }
        self.ListNames_to_color = {
            q1_curr.pvname : (1,0,0),
            q2_curr.pvname : (1,0.5,0),
            q3_curr.pvname : (1,0,0.5),
            q4_curr.pvname : (0,1,0),
            q5_curr.pvname : (0.5,1,0),
            q6_curr.pvname : (0,1,0.5),
            q7_curr.pvname : (0,0,1),
            d1_curr.pvname : (0.5,0,1),
            d2_curr.pvname : (0,0.5,1),
        }

        TabStripChart.__init__(self, parent)

