#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
from epics import PV
from Experiment import *
import time
from init_vars import *

class TabAppProperties(wx.Panel):


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        panel = self


        self.tE = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tE.SetValue("%.0f"%(E/1e+6))

        box = wx.StaticBox(panel, -1, 'Laser Energy')
        boxsizer1 = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        boxsizer1.Add(wx.StaticText(panel, label="Energy"),0,wx.ALL,10)
        boxsizer1.Add(self.tE,0,wx.ALL,10)
        boxsizer1.Add(wx.StaticText(panel, label="MeV"),0,wx.ALL,10)

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(boxsizer1, 0, wx.ALL, 10)

        self.b_apply = wx.Button(panel, label='Apply')
        self.b_apply.Bind(wx.EVT_BUTTON, self.OnApplyButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALL, 10)
        sizer.Add(self.b_apply, 0, wx.ALL, 10)


        panel.SetSizer(sizer)

    def OnApplyButton(self,evt):
        try:
            E = float(self.tE.GetValue())*1e+6
        except:
            print 'error converting the energy text field to float'

        self.window.tabMagnProperties.OnChangeEnergy(E)
        self.window.tabOverview.OnChangeEnergy(E)

        print 'E=%.0f'%E


#    def __del__(self):
#        self.alive=False
#        time.sleep(0.5)



