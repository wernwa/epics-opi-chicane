#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
from epics import PV
from PowerSupplyControls import PowerSupplyControls


class TabSchikane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        imageFile = 'pics/schikane_alpha.png'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (5, 5), (png.GetWidth(), png.GetHeight()))

        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        static_text = wx.StaticText(label="Dipol      \n1.4V \n1.2A\n300K", parent=panel,pos=wx.Point(50, 400))
        static_text = wx.StaticText(label="Quadrupol 1\n5.3V \n1.4A\n300K", parent=panel,pos=wx.Point(150, 400))
        static_text = wx.StaticText(label="Quadrupol 2\n3.74V\n1.3A\n300K", parent=panel,pos=wx.Point(250, 400))
        static_text = wx.StaticText(label="Quadrupol 3\n2.29V\n2.2A\n300K", parent=panel,pos=wx.Point(350, 400))
        static_text = wx.StaticText(label="Quadrupol 4\n4.51V\n1.0A\n300K", parent=panel,pos=wx.Point(470, 400))
        static_text = wx.StaticText(label="Quadrupol 5\n0.51V\n2.7A\n300K", parent=panel,pos=wx.Point(570, 400))
        static_text = wx.StaticText(label="Dipol 2    \n8.89V\n4.3A\n300K", parent=panel,pos=wx.Point(680, 400))
        static_text = wx.StaticText(label="Quadrupol 6\n2.43V\n1.3A\n300K", parent=panel,pos=wx.Point(780, 400))
        static_text = wx.StaticText(label="Quadrupol 7\n2.80V\n1.4A\n300K", parent=panel,pos=wx.Point(880, 400))
        static_text = wx.StaticText(label="Undulator  \n2.80V\n1.4A\n300K", parent=panel,pos=wx.Point(1100, 400))

        panel.SetSizer(hbox)





