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
import threading
import time
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

from init_vars import *

class TabMagnProperties(wx.Panel):


    b_image = None
    b_image_file = "pics/refresh-button2.png"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.parent = parent
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

        self.st_lab_y_achsis = wx.StaticText(panel, label="k mstrength:")

        fgs.AddMany([
            (wx.StaticText(panel, label="")), (self.st_title),(wx.StaticText(panel, label="")),
            (wx.StaticText(panel, label="Volt:")), (self.tcV, 1, wx.EXPAND),(self.bV),
            (wx.StaticText(panel, label="Curr:")), (self.tcA, 1, wx.EXPAND),(self.bA),
            (self.st_lab_y_achsis), (self.tck, 1, wx.EXPAND),(self.bk),
        ])


        """ Set event handlers """
        self.bV.Bind(wx.EVT_BUTTON, self.Refresh,self.bV)
        self.bA.Bind(wx.EVT_BUTTON, self.Refresh,self.bA)
        self.bk.Bind(wx.EVT_BUTTON, self.Refresh,self.bk)
        self.tcV.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tcV)
        self.tcA.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tcA)
        self.tck.Bind(wx.EVT_KEY_DOWN, self.Return_pressed,self.tck)

        self.magn=None


        # plot

        self.figure = Figure()
        self.canvas = FigureCanvas(self,-1,self.figure)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(self.canvas, proportion=2.5, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)

        self.colour_inactive = (90,90,90)
        self.colour_active = (255,255,255)


        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(500)


    def set_background_ctrl(self,evt):

        self.tcV.SetBackgroundColour(self.colour_curr)
        self.tcA.SetBackgroundColour(self.colour_curr)
        self.tck.SetBackgroundColour(self.colour_curr)
        if self.colour_curr == self.colour_inactive:
            self.tcV.Enable(False)
            self.tcA.Enable(False)
            self.tck.Enable(False)
        else:
            self.tcV.Enable(True)
            self.tcA.Enable(True)
            self.tck.Enable(True)

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):
        if value==1: stat='BUSY'
        else:   stat='IDLE'
        #print 'pvname %s value %s'%(pvname,stat)


        if value==1:
            self.colour_curr = self.colour_inactive
            self.call_routine_over_event(self.set_background_ctrl)
        else:
            self.colour_curr = self.colour_active
            self.call_routine_over_event(self.set_background_ctrl)


    def magnet_selected(self, event, title, magn):

        if self.magn!=None:
            #self.magn.pv_volt_status.remove_callback(self.onPVChanges)
            self.magn.pv_volt_status.callbacks = {}
            #self.magn.pv_curr_status.remove_callback(self.onPVChanges)
            self.magn.pv_curr_status.callbacks = {}

        self.magn = magn
        magn.pv_volt_status.add_callback(self.onPVChanges)
        magn.pv_curr_status.add_callback(self.onPVChanges)


        #start = time.time()
        if magn.pv_volt_status.conn!=False:
            if magn.pv_volt_status.value==1 or magn.pv_curr_status.value==1:
                self.colour_curr = self.colour_inactive
                #self.call_routine_over_event(self.set_background_ctrl)
            else:
                self.colour_curr = self.colour_active
        else: self.colour_curr = self.colour_inactive
        self.call_routine_over_event(self.set_background_ctrl)
        #print time.time()-start


        self.st_title.SetLabel(title+'\n')
        if magn.pv_volt_status.conn==True:
            volt = magn.pv_volt.get()
            if volt==None: volt=0
            self.tcV.SetValue('%.3f'%abs(volt))
            curr = magn.pv_curr.get()
            if curr==None: curr=0
            self.tcA.SetValue('%.3f'%abs(curr))
            self.tck.SetValue('%.3f'%self.magn.get_k(curr))
            if 'Quadrupol' in title: self.st_lab_y_achsis.SetLabel('k')
            elif 'Dipol' in title: self.st_lab_y_achsis.SetLabel('alpha')

            self.plot()




    def Return_pressed(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            control = e.GetEventObject()
            if control == self.tcV:
                value = round(float(self.tcV.GetValue()),3)
                #control.Enable(False)
                #control.SetBackgroundcolour((50,50,50))
                thread=threading.Thread(target=self.magn.ps.setVolt,args=(value,))
                thread.start()
                #sleep(2)
                #control.SetBackgroundcolour((255,255,255))
                #control.Enable(True)
            elif control == self.tcA:
                value = round(float(self.tcA.GetValue()),3)
                self.magn.ps.setCurr(value)
            elif control == self.tck:
                k = float(self.tck.GetValue())
                #print 'curr %f'%self.magn.get_curr(k)
                self.magn.ps.setCurr(self.magn.get_curr(k))
        e.Skip()


    def Refresh(self, e):
        if self.magn.pv_volt.conn == False: return

        control = e.GetEventObject()
        if control == self.bV:
            self.tcV.SetValue('%.3f'%abs(self.magn.pv_volt.get()))
        elif control == self.bA:
            self.tcA.SetValue('%.3f'%abs(self.magn.pv_curr.get()))
        elif control == self.bk:
            curr = float(self.tcA.GetValue())
            self.tck.SetValue('%.3f'%abs(self.magn.get_k(curr)))
            #print 'curr %f'%self.magn.get_k(curr)

    def OnChangeEnergy(self,energy):
        global E
        E=energy


    def on_redraw_timer(self, event):

        tab_i = self.parent.GetSelection()
        if self.parent.GetPageText(tab_i)=='Magnet Properties':
            self.plot()


    def plot(self):


        if self.magn==None: return

        x=self.magn.data_x
        y=self.magn.data_y


        # calc k from g
        #if self.magn.magn_type=='quad':
        g=y
        y=[]
        for i in range(0,len(g)): y.append(g[i]*c/E)

        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_xlabel(self.magn.data_xlabel)
        #if self.magn.magn_type=='quad':
        #    self.axes.set_ylabel(self.magn.data_ylabel+", E=%.0f MeV"%(E/1e+6))
        #else: self.axes.set_ylabel(self.magn.data_ylabel)
        self.axes.set_ylabel(self.magn.data_ylabel+", E=%.0f MeV"%(E/1e+6))
        self.axes.plot(x,y, marker='o', linestyle='--', color='r')

        # spline the data
        spline = interp1d(x, y, kind='cubic')
        xnew = numpy.linspace(x[0], x[len(x)-1], len(x)*10)

        self.axes.plot(xnew,spline(xnew), linestyle='-', color='g')

        # set the ylim from 0
        ylim = self.axes.get_ylim()
        self.axes.set_ylim((0,ylim[1]))

        # plot the current k position as vertical line
        if self.magn.pv_curr.conn == True:
            curr = self.magn.pv_curr.get()
            if curr==None: return
            curr = abs(curr)
            #k = self.magn.get_k(curr) + 10
            self.axes.plot((curr,curr),(0,ylim[1]), 'k-')

        #def myfkt(evt):
        #    self.canvas.draw()


        #self.call_routine_over_event(myfkt)

        self.canvas.draw()



    SomeNewEvent=None
    def call_routine_over_event(self, handler):

        #print 'call_routine_over_event'
        if self.SomeNewEvent==None:
            self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
            self.Bind(self.EVT_SOME_NEW_EVENT, handler)

            # Create the event
            self.evt = self.SomeNewEvent()


        # Post the event
        wx.PostEvent(self, self.evt)
