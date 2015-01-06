#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
from epics import PV
from Experiment import *
#from PowerSupplyControls import PowerSupplyControls
import time
from init_vars import *

class TabOverview(wx.Panel):


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        chicane_type = sys.argv[1]
        if chicane_type=='quadruplett':
            imageFile = 'pics/quadruplett.png'
        elif chicane_type=='triplett':
            imageFile = 'pics/triplett.png'
        else:
            print 'Err: chicane type not known'
            exit(0)
        image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
        #image = image.Scale(0.5,0.5)
        png = image.ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (0, 0), (png.GetWidth(), png.GetHeight()))
        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        self.font_normal = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.st_variables = wx.StaticText(label="E=%.0f MeV"%(E/1e+6),   parent=panel, pos=wx.Point(300,300))
        self.st_variables.SetFont(self.font_normal)
        #self.b_demag = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Demag")
        #self.b_demag.Bind(wx.EVT_BUTTON, self.OnDemag)
        panel.SetSizer(hbox)

    def OnChangeEnergy(self,energy):
        E=energy
        self.st_variables.SetLabel("E=%.0f MeV"%(E/1e+6))

#    def __del__(self):
#        self.alive=False
#        time.sleep(0.5)



