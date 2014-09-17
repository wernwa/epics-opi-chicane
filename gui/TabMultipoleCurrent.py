#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import sys
sys.path.insert(0, './cli')
from Experiment import *
import wx
from epics import PV
from PowerSupplyControls import PowerSupplyControls


from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt

#import pylab as pl
import math
import numpy as np
from scipy.interpolate import interp1d
import re


class TabMultipoleCurrent(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


        self.figure = plt.figure()

        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()

        x = self.I_arr = [0]
        y = self.k_arr= [0]


        # read the data from file
        for line in file('data/strength-int.data', 'r').xreadlines():
            # omit comments
            if (len(re.findall('^\s*?#',line))!=0): continue
            # split line into an array
            arr = re.findall('\S+',line)
            # fill the x,y arrays
            x.append(float(arr[0]))
            y.append(float(arr[1]))



        # spline the data
        self.spline = interp1d(x, y, kind='cubic')
        self.xnew = np.linspace(x[0], x[len(x)-1], len(x)*10)

        self.plot()

#        panel = self
#
#        hbox = wx.BoxSizer(wx.HORIZONTAL)
#
#        #print 'init the devices'
#        #init_devices()
#
#        fgs = wx.FlexGridSizer(3, 4, 5, 5)
#
#        #fgs.AddGrowableRow(2, 1)
#        #fgs.AddGrowableCol(1, 1)
#
#
#        imageFile = 'pics/crop_Zplus_Cat-III_L2.jpg'
#        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
#        imagewx = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
#
#        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
#        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
#
#        panel.SetSizer(hbox)




    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        #ax.plot(data, '*-')

        ax.set_xlabel(r'current I [A]')
        ax.set_ylabel(r'multipole strength k [$\frac{1}{\mbox{m}}$]')
        #ax.plot(self.I_arr,self.k_arr, marker='o', linestyle='--', color='r',label='quad multipole m')
        #ax.plot(self.xnew,self.spline(self.xnew), linestyle='-', color='g',label='spline')
        ax.plot(self.I_arr,self.k_arr, 'or--',self.xnew,self.spline(self.xnew),'g-')

        self.canvas.draw()

