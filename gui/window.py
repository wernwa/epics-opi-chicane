#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------



import sys, os
sys.path.insert(0, './cli')
from Experiment import *

import wx
from TabMagnProperties import TabMagnProperties
from TabOverview import TabOverview
from TabStripChartTemp import TabStripChartTemp
from TabStripChartVolt import TabStripChartVolt
from TabStripChartCurr import TabStripChartCurr
from TabAppProperties import TabAppProperties
from DataPanel import DataPanel

import thread

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "Assign currents to magnetic fields", (60,60))


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="chicane interface", pos=(10,10), size=(1200,800))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()

        menu = wx.Menu()
        m_handle = menu.Append(wx.NewId(), "Save current/voltage As...\tAlt-S", "save current/voltage *.py")
        self.Bind(wx.EVT_MENU, self.OnSaveCurrVoltFile, m_handle)
        m_handle = menu.Append(wx.NewId(), "&Load current/voltage *.py file\tAlt-L", "load a *.py file")
        self.Bind(wx.EVT_MENU, self.OnLoadFile, m_handle)
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")

        menu = wx.Menu()
        self.menu_magn = menu.Append(wx.NewId(), "&cycle all magnets\tAlt-d", "demag all magnets")
        self.Bind(wx.EVT_MENU, self.OnDemag, self.menu_magn)
        menuBar.Append(menu, "&Magnets")

        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        self.nb = nb = wx.Notebook(p)

        # create the page windows as children of the notebook

        # add the pages to the notebook with the label to show on the tab
        self.tabOverview = TabOverview(nb)
        self.tabOverview.window = self
        self.nb.AddPage(self.tabOverview, "Overview")

        self.tabMagnProperties = TabMagnProperties(nb)
        self.tabMagnProperties.window = self
        self.nb.AddPage(self.tabMagnProperties, "Magnet Properties")

        self.tabStripChartTemp = TabStripChartTemp(nb)
        self.tabStripChartTemp.window = self
        nb.AddPage(self.tabStripChartTemp, "Temperature")

        self.tabStripChartVolt = TabStripChartVolt(nb)
        self.tabStripChartVolt.window = self
        nb.AddPage(self.tabStripChartVolt, "Voltage")

        self.tabStripChartCurr = TabStripChartCurr(nb)
        self.tabStripChartCurr.window = self
        nb.AddPage(self.tabStripChartCurr, "Current")

        self.tabAppProperties = TabAppProperties(nb)
        self.tabAppProperties.window = self
        nb.AddPage(self.tabAppProperties, "Application Properties")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        self.dataPanel = DataPanel(self)
        #panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)

        #panel2.SetBackgroundColour("RED")


        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(p, 4, wx.EXPAND)
        box.Add(self.dataPanel, 1, wx.EXPAND)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()


    def OnSaveCurrVoltFile(self, event):
        openFileDialog = wx.FileDialog(self, message="save current/voltage", defaultDir=os.getcwd(),
                                     wildcard="Python files (*.py)|*.py", style=wx.SAVE)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        pyfile = openFileDialog.GetPath()

        def str_helper(string,pv):
            val = pv.get()
            if val==None:
                return '#'+string%0
            else:
                return string%val


        fh = open(pyfile,'w+')

        fh.write(str_helper( 'mquad1.ps.Volt.put(%.3f)\n', mquad1.ps.Volt))
        fh.write(str_helper( 'mquad2.ps.Volt.put(%.3f)\n', mquad2.ps.Volt))
        fh.write(str_helper( 'mquad3.ps.Volt.put(%.3f)\n', mquad3.ps.Volt))
        fh.write(str_helper( 'mquad4.ps.Volt.put(%.3f)\n', mquad4.ps.Volt))
        fh.write(str_helper( 'mquad5.ps.Volt.put(%.3f)\n', mquad5.ps.Volt))
        fh.write(str_helper( 'mquad6.ps.Volt.put(%.3f)\n', mquad6.ps.Volt))
        fh.write(str_helper( 'mquad7.ps.Volt.put(%.3f)\n', mquad7.ps.Volt))
        fh.write(str_helper('mdipol1.ps.Volt.put(%.3f)\n',mdipol1.ps.Volt))
        fh.write(str_helper('mdipol2.ps.Volt.put(%.3f)\n',mdipol2.ps.Volt))

        fh.write(str_helper('mquad1.ps.Curr.put(%.3f)\n',mquad1.ps.Curr))
        fh.write(str_helper('mquad2.ps.Curr.put(%.3f)\n',mquad2.ps.Curr))
        fh.write(str_helper('mquad3.ps.Curr.put(%.3f)\n',mquad3.ps.Curr))
        fh.write(str_helper('mquad4.ps.Curr.put(%.3f)\n',mquad4.ps.Curr))
        fh.write(str_helper('mquad5.ps.Curr.put(%.3f)\n',mquad5.ps.Curr))
        fh.write(str_helper('mquad6.ps.Curr.put(%.3f)\n',mquad6.ps.Curr))
        fh.write(str_helper('mquad7.ps.Curr.put(%.3f)\n',mquad7.ps.Curr))
        fh.write(str_helper('mdipol1.ps.Curr.put(%.3f)\n',mdipol1.ps.Curr))
        fh.write(str_helper('mdipol2.ps.Curr.put(%.3f)\n',mdipol2.ps.Curr))

        fh.close()

        openFileDialog.Destroy()


    def OnLoadFile(self, event):
        openFileDialog = wx.FileDialog(self, message="load python file", defaultDir=os.getcwd(),
                                     wildcard="Python files (*.py)|*.py", style=wx.OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        pyfile = openFileDialog.GetPath()

        execfile(pyfile)

        openFileDialog.Destroy()

    def OnSaveAs(self, event):
        saveFileDialog = wx.FileDialog(self, "Save XYZ file", "", "",
                    "XYZ files (*.xyz)|*.xyz", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        print 'TODO'

    def OnDemag(self, event):

        def demagThread():
            #self.b_demag.Enable(False)
            self.menu_magn.Enable(False)
            demag()
            self.menu_magn.Enable(True)
            #self.b_demag.Enable(True)


        dlg = wx.MessageDialog(self, 'Do you realy want to start cycling all magnets?', 'Cycling',
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
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

        used_pvs = [temp_all,magn_volt_all,magn_curr_all]
        for pv in used_pvs:
            pv.disconnect()

        # Thread noch aktiv, besser destructor!
        #self.tabShicane.alive=False
        self.tabStripChartTemp.__del__()
        self.tabStripChartVolt.__del__()
        self.tabStripChartCurr.__del__()
        self.dataPanel.__del__()



        self.Destroy()


if __name__ == "__main__":

    #print 'init the devices'
    #init_devices()


    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
