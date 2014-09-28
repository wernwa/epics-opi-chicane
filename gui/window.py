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
from TabPowerSupplies import TabPowerSupplies
from TabSchikane import TabSchikane
from TabStripChartGNUPLOT import TabStripChartGNUPLOT
from TabStripChart import TabStripChart
from TabMultipoleCurrent import TabMultipoleCurrent



class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Assign currents to magnetic fields", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Magnets Control GUI", pos=(150,150), size=(800,600))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook

        # add the pages to the notebook with the label to show on the tab
        self.tabShicane = TabSchikane(nb)
        nb.AddPage(self.tabShicane, "Overview")
        nb.AddPage(TabPowerSupplies(nb), "Power Supplies")
            #nb.AddPage(PageThree(nb), "Magnetic Fields")
            #nb.AddPage(TabStripChartGNUPLOT(nb), "StripChartGNUPLOT (old)")
        nb.AddPage(TabMultipoleCurrent(nb), "Multipole Current")
        nb.AddPage(TabStripChart(nb), "StripChart")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)



    def OnClose(self, event):
        #dlg = wx.MessageDialog(self,
        #    "Do you really want to close this application?",
        #    "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        #result = dlg.ShowModal()
        #dlg.Destroy()
        #if result == wx.ID_OK:
        #    self.Destroy()

        # TODO release all PVs from callbacks
        used_pvs = (ps8.Volt,ps8.Curr,t1)
        # Thread noch aktiv, besser destructor!
        self.tabShicane.alive=False

        for pv in used_pvs:
            pv.disconnect()


        self.Destroy()


if __name__ == "__main__":

    #print 'init the devices'
    #init_devices()

    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
