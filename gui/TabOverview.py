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

class TabOverview(wx.Panel):


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        shicane_type = sys.argv[1]
        if shicane_type=='quadruplett':
            imageFile = 'pics/quadruplett.png'
        elif shicane_type=='triplett':
            imageFile = 'pics/triplett.png'
        else:
            print 'Err: shicane type not known'
            exit(0)
        image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
        #image = image.Scale(0.5,0.5)
        png = image.ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (0, 0), (png.GetWidth(), png.GetHeight()))
        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        #self.b_demag = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Demag")
        #self.b_demag.Bind(wx.EVT_BUTTON, self.OnDemag)
        panel.SetSizer(hbox)


#    def __del__(self):
#        self.alive=False
#        time.sleep(0.5)



