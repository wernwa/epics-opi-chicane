#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------
import sys
sys.path.insert(0, './cli')
import Experiment
import wx
from epics import PV




class PowerSupplyControls:

    """ epics variables  """
    ps = None # The Powersupply

    """ text inputs for Volt and Ampare values """
    tcV = None
    tcA = None

    """ refresh button vars """
    b = None
    b_image = None
    b_image_file = "pics/refresh-button2.png"

    def __init__(self, powersupply, panel):

        self.ps = powersupply



        self.tcV = wx.TextCtrl(panel,-1, "",style=wx.TE_PROCESS_ENTER)
        self.tcA = wx.TextCtrl(panel)

        """ load the refresh-image-icon only once (<Class>.<var> <-- static class variable)  """
        if PowerSupplyControls.b_image == None:
            PowerSupplyControls.b_image = wx.Image(self.b_image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        self.b = wx.BitmapButton(panel, id=-1, bitmap=PowerSupplyControls.b_image,
                pos=(0, 0), size = (PowerSupplyControls.b_image.GetWidth()+10, PowerSupplyControls.b_image.GetHeight()+10))
        #self.b = wx.Button(panel, label='refresh')

        if self.ps == None:
            return

        """ Set event handlers """
        self.b.Bind(wx.EVT_BUTTON, self.Refresh)
        self.tcV.Bind(wx.EVT_KEY_DOWN, self.Return_pressed)

        self.ps.getterVolt.add_callback(Experiment.onChanges)

    def onChanges(self, pvname=None, value=None, char_value=None, **kw):
        print 'PV Changed! ', pvname, char_value

    def Return_pressed(self, e):
        keycode = e.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER:
            value = float(self.tcV.GetValue())
            self.ps.setterVolt.put(value)
            print 'setting  %f' %value
            ''' actualize the getter pv (not needed if SCAN eq periodic)  '''
            self.ps.getterVolt.put(value)
        e.Skip()


    def Refresh(self, e):
        #dlg = wx.MessageDialog(self,
        #    "you pressed the REFRESH button, he he",
        #    "Confirm REFRESH", wx.OK)

        #result = dlg.ShowModal()
        #dlg.Destroy()

        self.tcV.SetValue("%.3f" %self.ps.getterVolt.put(0))


