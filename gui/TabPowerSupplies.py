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


class TabPowerSupplies(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        #print 'init the devices'
        #init_devices()

        fgs = wx.FlexGridSizer(3, 4, 5, 5)

        ps1 = PowerSupplyControls(ps[1],panel)
        ps2 = PowerSupplyControls(ps[2],panel)
        ps3 = PowerSupplyControls(ps[3],panel)
        ps4 = PowerSupplyControls(ps[4],panel)
        ps5 = PowerSupplyControls(ps[5],panel)
        ps6 = PowerSupplyControls(ps[6],panel)
        ps7 = PowerSupplyControls(ps[7],panel)
        ps8 = PowerSupplyControls(ps[8],panel)
        ps9 = PowerSupplyControls(ps[9],panel)


        fgs.AddMany([
            (wx.StaticText(panel, label="")), (wx.StaticText(panel, label="Volts")),(wx.StaticText(panel, label="Ampere")),(wx.StaticText(panel, label="")),
            (wx.StaticText(panel, label="PS1 Relay:")), (ps1.tcV, 1, wx.EXPAND),(ps1.tcA, 1, wx.EXPAND), (ps1.b),
            (wx.StaticText(panel, label="PS2:")), (ps2.tcV, 1, wx.EXPAND),(ps2.tcA, 1, wx.EXPAND), (ps2.b),
            (wx.StaticText(panel, label="PS3:")), (ps3.tcV, 1, wx.EXPAND),(ps3.tcA, 1, wx.EXPAND), (ps3.b),
            (wx.StaticText(panel, label="PS4:")), (ps4.tcV, 1, wx.EXPAND),(ps4.tcA, 1, wx.EXPAND), (ps4.b),
            (wx.StaticText(panel, label="PS5:")), (ps5.tcV, 1, wx.EXPAND),(ps5.tcA, 1, wx.EXPAND), (ps5.b),
            (wx.StaticText(panel, label="PS6:")), (ps6.tcV, 1, wx.EXPAND),(ps6.tcA, 1, wx.EXPAND), (ps6.b),
            (wx.StaticText(panel, label="PS7:")), (ps7.tcV, 1, wx.EXPAND),(ps7.tcA, 1, wx.EXPAND), (ps7.b),
            (wx.StaticText(panel, label="PS8:")), (ps8.tcV, 1, wx.EXPAND),(ps8.tcA, 1, wx.EXPAND), (ps8.b),
            (wx.StaticText(panel, label="PS9:")), (ps9.tcV, 1, wx.EXPAND),(ps9.tcA, 1, wx.EXPAND), (ps9.b)
        ])

        #fgs.AddGrowableRow(2, 1)
        #fgs.AddGrowableCol(1, 1)


        imageFile = 'pics/crop_Zplus_Cat-III_L2.jpg'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)





