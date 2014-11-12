#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
from epics import PV
from Experiment import *
from PowerSupplyControls import PowerSupplyControls
from thread import start_new_thread
import time
from init_vars import *

class TabAppProperties(wx.Panel):


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(4, 2, 5, 5)


        self.tcV = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tcA = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tck = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)

        self.st_title = wx.StaticText(panel, label="Application Properties")
        font_bold = wx.Font(16, wx.DEFAULT,  wx.NORMAL, wx.BOLD)
        self.st_title.SetFont(font_bold)

        fgs.AddMany([
            (wx.StaticText(panel, label="")), (self.st_title),
            (wx.StaticText(panel, label="Energy")), (self.tcV, 1, wx.EXPAND),
            (wx.StaticText(panel, label="Prop1")), (self.tcA, 1, wx.EXPAND),
            (wx.StaticText(panel, label="Prop2")), (self.tck, 1, wx.EXPAND),
        ])


        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)

#    def __del__(self):
#        self.alive=False
#        time.sleep(0.5)



