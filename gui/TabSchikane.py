#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
from epics import PV
from Experiment import *
from PowerSupplyControls import PowerSupplyControls
from thread import start_new_thread

class TabSchikane(wx.Panel):

    st_quad1 = None
    b_demag = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        imageFile = 'pics/schikane_alpha.png'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (5, 5), (png.GetWidth(), png.GetHeight()))

        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        static_text = wx.StaticText(label="Dipol      \n#.##V \n#.##A\n###K", parent=panel,pos=wx.Point(50, 400))
        self.st_quad1 = wx.StaticText(label="Quadrupol 1\n#.##V \n#.##A\n###K", parent=panel,pos=wx.Point(150, 400))
        static_text = wx.StaticText(label="Quadrupol 2\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(250, 400))
        static_text = wx.StaticText(label="Quadrupol 3\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(350, 400))
        static_text = wx.StaticText(label="Quadrupol 4\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(470, 400))
        static_text = wx.StaticText(label="Quadrupol 5\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(570, 400))
        static_text = wx.StaticText(label="Dipol 2    \n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(680, 400))
        static_text = wx.StaticText(label="Quadrupol 6\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(780, 400))
        static_text = wx.StaticText(label="Quadrupol 7\n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(880, 400))
        static_text = wx.StaticText(label="Undulator  \n#.##V\n#.##A\n###K", parent=panel,pos=wx.Point(1100, 400))

        self.b_demag = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Demag")
        self.b_demag.Bind(wx.EVT_BUTTON, self.OnDemag)
        panel.SetSizer(hbox)

        ps[8].getterVolt.add_callback(self.onPVChanges)

    def OnDemag(self, event):
        def demagThread():
            self.b_demag.Enable(False)
            demag()
            self.b_demag.Enable(True)

        start_new_thread( demagThread,() )

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):
        #print 'PV Changed! %s %0.3f' %(pvname, value)
        if pvname == 'zpslan08-GetVoltage':
            self.st_quad1.SetLabel("Quadrupol 1\n%.3fV \n%.3fA\n###K" %(value,magn[1].powersupply.getAmpare()))

        if pvname == 'zpslan08-GetAmpare':
            self.st_quad1.SetLabel("Quadrupol 1\n%.3fV \n%.3fA\n###K" %(magn[1].powersupply.getVolt(),value))


