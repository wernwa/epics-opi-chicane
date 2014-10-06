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
from TabMagnProperties import TabMagnProperties
from TabOverview import TabOverview
#from TabStripChartGNUPLOT import TabStripChartGNUPLOT
from TabStripChart import TabStripChart
#from TabMultipoleCurrent import TabMultipoleCurrent
from DataPanel import DataPanel

import thread

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Assign currents to magnetic fields", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="shicane interface", pos=(10,10), size=(1000,800))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()

        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")

        menu = wx.Menu()
        m_magn = menu.Append(wx.NewId(), "&demag\tAlt-d", "demag all magnets")
        self.Bind(wx.EVT_MENU, self.OnDemag, m_magn)
        menuBar.Append(menu, "&Magnets")

        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        self.nb = nb = wx.Notebook(p)

        # create the page windows as children of the notebook

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(TabOverview(nb), "Overview")
        self.tabMagnProperties = TabMagnProperties(nb)
        self.nb.AddPage(self.tabMagnProperties, "Magnet Properties")
        #self.nb.AddPage(TabMultipoleCurrent(nb), "Multipole Current")
        #nb.AddPage(TabStripChart(nb), "StripChart")
            #nb.AddPage(PageThree(nb), "Magnetic Fields")
            #nb.AddPage(TabStripChartGNUPLOT(nb), "StripChartGNUPLOT (old)")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.dataPanel = DataPanel(self)
        #panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)

        #panel2.SetBackgroundColour("RED")


        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(p, 5, wx.EXPAND)
        box.Add(self.dataPanel, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()

    def OnDemag(self, event):
        def demagThread():
            #self.b_demag.Enable(False)
            demag()
            #self.b_demag.Enable(True)

        thread.start_new_thread( demagThread,() )

    def OnClose(self, event):
        #dlg = wx.MessageDialog(self,
        #    "Do you really want to close this application?",
        #    "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        #result = dlg.ShowModal()
        #dlg.Destroy()
        #if result == wx.ID_OK:
        #    self.Destroy()

        # TODO release all PVs from callbacks
        global quad1, quad2, quad3, quad4, quad5, quad6, quad7, dipol1, dipol2
        global temp_all
        magnets = [quad1, quad2, quad3, quad4, quad5, quad6, quad7, dipol1, dipol2]


        for m in magnets:
            for pv_str in m:
                m[pv_str].disconnect()

        used_pvs = [temp_all,ps_volt_all,ps_curr_all]
        for pv in used_pvs:
            pv.disconnect()

        # Thread noch aktiv, besser destructor!
        #self.tabShicane.alive=False
        self.dataPanel.__del__()



        self.Destroy()


if __name__ == "__main__":

    #print 'init the devices'
    #init_devices()


    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
