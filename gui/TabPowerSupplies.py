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

        global ps, relee, ps1, ps2, ps3, ps4, ps5, ps6, ps7, ps8, ps9, ps10

        ps1c = PowerSupplyControls(ps1,panel)
        ps2c = PowerSupplyControls(ps2,panel)
        ps3c = PowerSupplyControls(ps3,panel)
        ps4c = PowerSupplyControls(ps4,panel)
        ps5c = PowerSupplyControls(ps5,panel)
        ps6c = PowerSupplyControls(ps6,panel)
        ps7c = PowerSupplyControls(ps7,panel)
        ps8c = PowerSupplyControls(ps8,panel)
        ps9c = PowerSupplyControls(ps9,panel)


        fgs.AddMany([
            (wx.StaticText(panel, label="")), (wx.StaticText(panel, label="Volts")),(wx.StaticText(panel, label="Ampere")),(wx.StaticText(panel, label="")),
            (wx.StaticText(panel, label="PS1 Relay:")), (ps1c.tcV, 1, wx.EXPAND),(ps1c.tcA, 1, wx.EXPAND), (ps1c.b),
            (wx.StaticText(panel, label="PS2:")), (ps2c.tcV, 1, wx.EXPAND),(ps2c.tcA, 1, wx.EXPAND), (ps2c.b),
            (wx.StaticText(panel, label="PS3:")), (ps3c.tcV, 1, wx.EXPAND),(ps3c.tcA, 1, wx.EXPAND), (ps3c.b),
            (wx.StaticText(panel, label="PS4:")), (ps4c.tcV, 1, wx.EXPAND),(ps4c.tcA, 1, wx.EXPAND), (ps4c.b),
            (wx.StaticText(panel, label="PS5:")), (ps5c.tcV, 1, wx.EXPAND),(ps5c.tcA, 1, wx.EXPAND), (ps5c.b),
            (wx.StaticText(panel, label="PS6:")), (ps6c.tcV, 1, wx.EXPAND),(ps6c.tcA, 1, wx.EXPAND), (ps6c.b),
            (wx.StaticText(panel, label="PS7:")), (ps7c.tcV, 1, wx.EXPAND),(ps7c.tcA, 1, wx.EXPAND), (ps7c.b),
            (wx.StaticText(panel, label="PS8:")), (ps8c.tcV, 1, wx.EXPAND),(ps8c.tcA, 1, wx.EXPAND), (ps8c.b),
            (wx.StaticText(panel, label="PS9:")), (ps9c.tcV, 1, wx.EXPAND),(ps9c.tcA, 1, wx.EXPAND), (ps9c.b)
        ])

        #fgs.AddGrowableRow(2, 1)
        #fgs.AddGrowableCol(1, 1)


        imageFile = 'pics/crop_Zplus_Cat-III_L2.jpg'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)





