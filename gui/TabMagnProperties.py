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
import math


import numpy
import matplotlib

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
#import matplotlib.pyplot as plt

#import numpy as np

from scipy.interpolate import interp1d
import re


class TabMagnProperties(wx.Panel):


    b_image = None
    b_image_file = "pics/refresh-button2.png"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        #print 'init the devices'
        #init_devices()

        fgs = wx.FlexGridSizer(4, 3, 5, 5)


        global ps, relee, ps1, ps2, ps3, ps4, ps5, ps6, ps7, ps8, ps9, ps10

        b_image = wx.Image(self.b_image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.bV = wx.BitmapButton(panel, id=-1, bitmap=b_image,
                pos=(0, 0), size = (b_image.GetWidth()+10, b_image.GetHeight()+10))
        self.bA = wx.BitmapButton(panel, id=-1, bitmap=b_image,
                pos=(0, 0), size = (b_image.GetWidth()+10, b_image.GetHeight()+10))
        self.bk = wx.BitmapButton(panel, id=-1, bitmap=b_image,
                pos=(0, 0), size = (b_image.GetWidth()+10, b_image.GetHeight()+10))

        self.tcV = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tcA = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tck = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)

        self.st_title = wx.StaticText(panel, label="")
        font_bold = wx.Font(16, wx.DEFAULT,  wx.NORMAL, wx.BOLD)
        self.st_title.SetFont(font_bold)



        fgs.AddMany([
            (wx.StaticText(panel, label="")), (self.st_title),(wx.StaticText(panel, label="")),
            (wx.StaticText(panel, label="Volt:")), (self.tcV, 1, wx.EXPAND),(self.bV),
            (wx.StaticText(panel, label="Curr:")), (self.tcA, 1, wx.EXPAND),(self.bA),
            (wx.StaticText(panel, label="k mstrength:")), (self.tck, 1, wx.EXPAND),(self.bk),
        ])


        """ Set event handlers """
        self.bV.Bind(wx.EVT_BUTTON, self.Refresh,self.bV)
        self.bA.Bind(wx.EVT_BUTTON, self.Refresh,self.bA)
        self.bk.Bind(wx.EVT_BUTTON, self.Refresh,self.bk)
        self.tcV.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tcV)
        self.tcA.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tcA)
        self.tck.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tck)




        # plot
#        self.figure = plt.figure()
#
#        self.canvas = FigureCanvas(self,-1, self.figure)
#        #self.toolbar = NavigationToolbar(self.canvas)
#        #self.toolbar.Hide()
#
#        x = self.I_arr = [0]
#        y = self.k_arr= [0]
#
#
#        # read the data from file
#        for line in file('data/strength-int.data', 'r').xreadlines():
#            # omit comments
#            if (len(re.findall('^\s*?#',line))!=0): continue
#            # split line into an array
#            arr = re.findall('\S+',line)
#            # fill the x,y arrays
#            x.append(float(arr[0]))
#            y.append(float(arr[1]))
#
#
#
#        # spline the data
#        self.spline = interp1d(x, y, kind='cubic')
#        self.xnew = np.linspace(x[0], x[len(x)-1], len(x)*10)
#
#
#

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self,-1,self.figure)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(self.canvas, proportion=3, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)

    def magnet_selected(self, event, title, magn):
        self.st_title.SetLabel(title+'\n')
        self.magn = magn
        self.tcV.SetValue('%.3f'%magn.pv_volt.get())
        self.tcA.SetValue('%.3f'%magn.pv_curr.get())
        self.tck.SetValue('TODO')
        self.plot()




    def Return_pressed(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            value = round(float(self.tcV.GetValue()),3)
            control = e.GetEventObject()
            if control == self.tcV:
                self.magn.ps.setVolt(value)
            elif control == self.tcA:
                self.magn.ps.setCurr(value)
            elif control == self.tck:
                print 'k TODO'
        e.Skip()


    def Refresh(self, e):
        control = e.GetEventObject()
        if control == self.bV:
            self.tcV.SetValue('%.3f'%self.magn.pv_volt.get())
        elif control == self.bA:
            self.tcA.SetValue('%.3f'%self.magn.pv_curr.get())
        elif control == self.bk:
            self.tck.SetValue('refresh TODO')

    def plot(self):
#        ax = self.figure.add_subplot(111)
#        ax.hold(False)
#        #ax.plot(data, '*-')
#
#        ax.set_xlabel(r'current I [A]')
#        #ax.set_ylabel(r'multipole strength k [$\frac{1}{\mbox{m}}$]')
#        #ax.plot(self.I_arr,self.k_arr, marker='o', linestyle='--', color='r',label='quad multipole m')
#        #ax.plot(self.xnew,self.spline(self.xnew), linestyle='-', color='g',label='spline')
#        ax.plot(self.I_arr,self.k_arr, 'or--',self.xnew,self.spline(self.xnew),'g-')
#
#        self.canvas.draw()

#        # spline the data
#        self.spline = interp1d(x, y, kind='cubic')
#        self.xnew = np.linspace(x[0], x[len(x)-1], len(x)*10)

        self.axes.set_xlabel('x label')
        self.axes.set_ylabel('y label')
        #t = numpy.arange(0.0,10,1.0)
        #s = [0,1,0,1,0,2,1,2,1,0]
        #self.y_max = 1.0
        self.axes.plot(self.magn.data_x,self.magn.data_y)


