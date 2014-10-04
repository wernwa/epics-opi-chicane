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
import math

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



        imageFile = 'pics/crop_Zplus_Cat-III_L2.jpg'
        png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        panel.SetSizer(hbox)


    def magnet_selected(self, event, title, magn):
        self.st_title.SetLabel(title+'\n')
        self.magn = magn




    def Return_pressed(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            #value = math.fabs(float(self.tcV.GetValue()))
            value = round(float(self.tcV.GetValue()),3)
            #self.ps.setterVolt.put(value)
            #print 'setting  %f' %value
            #''' actualize the getter pv (not needed if SCAN eq periodic)  '''
            #self.ps.getterVolt.put(value)
            #global ps2
            #ps2.setVolt(value)
            control = e.GetEventObject()
            if control == self.tcV:
                self.magn.ps.setVolt(value)
            elif control == self.tcA:
                self.magn.ps.setCurr(value)
            elif control == self.tck:
                print 'k TODO'
        e.Skip()


    def Refresh(self, e):
        #dlg = wx.MessageDialog(self,
        #    "you pressed the REFRESH button, he he",
        #    "Confirm REFRESH", wx.OK)

        #result = dlg.ShowModal()
        #dlg.Destroy()

        #self.tcV.SetValue("%.3f" %self.ps.getterVolt.put(0))
        print 'refresh, Bingo',e.GetEventObject()

