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



class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Assign currents to magnetic fields", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Magnets Control GUI", pos=(150,150), size=(800,600))
        #self.Bind(wx.EVT_CLOSE, self.OnClose)

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
        page1 = TabSchikane(nb)
        page2 = TabPowerSupplies(nb)
        page3 = PageThree(nb)
        page4 = TabStripChartGNUPLOT(nb)
        page5 = TabStripChart(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Overview")


        nb.AddPage(page2, "Power Supplies")
        nb.AddPage(page3, "Magnetic Fields")
        nb.AddPage(page4, "StripChartGNUPLOT (old)")
        nb.AddPage(page5, "StripChart")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)



    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()


if __name__ == "__main__":

    print 'init the devices'
    init_devices()

    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
