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

        self.st_dipol1 = wx.StaticText(label="Dipol      \n#.##V \n#.##A\n##°C", parent=panel,pos=wx.Point(50, 400))
        self.st_quad1 = wx.StaticText(label="Quadrupol 1\n#.##V \n#.##A\n##°C", parent=panel,pos=wx.Point(150, 400))
        self.st_quad2 = wx.StaticText(label="Quadrupol 2\n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(250, 400))
        self.st_quad3 = wx.StaticText(label="Quadrupol 3\n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(350, 400))
        self.st_quad4 = wx.StaticText(label="Quadrupol 4\n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(470, 400))
        self.st_quad5 = wx.StaticText(label="Quadrupol 5\n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(570, 400))
        self.st_dipol2 = wx.StaticText(label="Dipol 2    \n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(680, 400))
        self.st_quad6 = wx.StaticText(label="Quadrupol 6\n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(780, 400))
        self.st_quad7 = wx.StaticText(label="Quadrupol 7\n#.##V \n#.##A\n##°C", parent=panel,pos=wx.Point(880, 400))
        static_text = wx.StaticText(label="Undulator  \n#.##V\n#.##A\n##°C", parent=panel,pos=wx.Point(1100, 400))

        self.b_demag = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Demag")
        self.b_demag.Bind(wx.EVT_BUTTON, self.OnDemag)
        panel.SetSizer(hbox)

        q1_volt.add_callback(self.onPVChanges)
        q1_curr.add_callback(self.onPVChanges)
        q1_temp.add_callback(self.onPVChanges)

        q2_volt.add_callback(self.onPVChanges)
        q2_curr.add_callback(self.onPVChanges)
        q2_temp.add_callback(self.onPVChanges)

        q3_volt.add_callback(self.onPVChanges)
        q3_curr.add_callback(self.onPVChanges)
        q3_temp.add_callback(self.onPVChanges)

        q4_volt.add_callback(self.onPVChanges)
        q4_curr.add_callback(self.onPVChanges)
        q4_temp.add_callback(self.onPVChanges)

        q5_volt.add_callback(self.onPVChanges)
        q5_curr.add_callback(self.onPVChanges)
        q5_temp.add_callback(self.onPVChanges)

        q6_volt.add_callback(self.onPVChanges)
        q6_curr.add_callback(self.onPVChanges)
        q6_temp.add_callback(self.onPVChanges)

        q7_volt.add_callback(self.onPVChanges)
        q7_curr.add_callback(self.onPVChanges)
        q7_temp.add_callback(self.onPVChanges)

        d1_volt.add_callback(self.onPVChanges)
        d1_curr.add_callback(self.onPVChanges)
        d1_temp.add_callback(self.onPVChanges)

        d2_volt.add_callback(self.onPVChanges)
        d2_curr.add_callback(self.onPVChanges)
        d2_temp.add_callback(self.onPVChanges)


        # refresh labels
        self.alive=True
        def refresh_labels():
            # TODO Thread beim beenden beenden
            while self.alive:
                self.call_routine_over_event( self.changeLables )
                time.sleep(3)
        start_new_thread(refresh_labels,())


    def OnDemag(self, event):
        def demagThread():
            self.b_demag.Enable(False)
            demag()
            self.b_demag.Enable(True)

        start_new_thread( demagThread,() )

    def pv_get_str(self, pv):
        #print 'TabSchikane.pv_get_str ',pv
        value = pv.get()
        str_val = '##.###'
        if value!=None:
            str_val = '%.3f'%value
        return str_val

    curr_pvname_changed = None
    def changeLables(self,evt):
        pvname = self.curr_pvname_changed

        #global quad1, quad2, quad3, quad4, quad5, quad6, quad7, dipol1, dipol2

        #print pvname
        if pvname == q1_volt.pvname  or pvname == q1_curr.pvname or pvname == q1_temp.pvname:
            self.st_quad1.SetLabel("Quadrupol 1\n%s V \n%s A\n%s °C" %(self.pv_get_str(q1_volt),
                                                                        self.pv_get_str(q1_volt),
                                                                        self.pv_get_str(q1_temp)
                                                                            ))
        elif pvname == q2_volt.pvname  or pvname == q2_curr.pvname or pvname == q2_temp.pvname:
            self.st_quad2.SetLabel("Quadrupol 2\n%s V \n%s A\n%s °C" %(self.pv_get_str(q2_volt),
                                                                        self.pv_get_str(q2_volt),
                                                                        self.pv_get_str(q2_temp)
                                                                            ))
        elif pvname == q3_volt.pvname  or pvname == q3_curr.pvname or pvname == q3_temp.pvname:
            self.st_quad3.SetLabel("Quadrupol 3\n%s V \n%s A\n%s °C" %(self.pv_get_str(q3_volt),
                                                                        self.pv_get_str(q3_volt),
                                                                        self.pv_get_str(q3_temp)
                                                                            ))
        elif pvname == q4_volt.pvname  or pvname == q4_curr.pvname or pvname == q4_temp.pvname:
            self.st_quad4.SetLabel("Quadrupol 4\n%s V \n%s A\n%s °C" %(self.pv_get_str(q4_volt),
                                                                        self.pv_get_str(q4_volt),
                                                                        self.pv_get_str(q4_temp)
                                                                            ))
        elif pvname == q5_volt.pvname  or pvname == q5_curr.pvname or pvname == q5_temp.pvname:
            self.st_quad5.SetLabel("Quadrupol 5\n%s V \n%s A\n%s °C" %(self.pv_get_str(q5_volt),
                                                                        self.pv_get_str(q5_volt),
                                                                        self.pv_get_str(q5_temp)
                                                                            ))
        elif pvname == q6_volt.pvname  or pvname == q6_curr.pvname or pvname == q6_temp.pvname:
            self.st_quad6.SetLabel("Quadrupol 6\n%s V \n%s A\n%s °C" %(self.pv_get_str(q6_volt),
                                                                        self.pv_get_str(q6_volt),
                                                                        self.pv_get_str(q6_temp)
                                                                            ))
        elif pvname == q7_volt.pvname  or pvname == q7_curr.pvname or pvname == q7_temp.pvname:
            self.st_quad7.SetLabel("Quadrupol 7\n%s V \n%s A\n%s °C" %(self.pv_get_str(q7_volt),
                                                                        self.pv_get_str(q7_volt),
                                                                        self.pv_get_str(q7_temp)
                                                                            ))
        elif pvname == d1_volt.pvname  or pvname == d1_curr.pvname or pvname == d1_temp.pvname:
            self.st_dipol1.SetLabel("Dipol 1\n%s V \n%s A\n%s °C" %(self.pv_get_str(d1_volt),
                                                                        self.pv_get_str(d1_volt),
                                                                        self.pv_get_str(d1_temp)
                                                                            ))
        elif pvname == d2_volt.pvname  or pvname == d2_curr.pvname or pvname == d2_temp.pvname:
            self.st_dipol2.SetLabel("Dipol 2\n%s V \n%s A\n%s °C" %(self.pv_get_str(d2_volt),
                                                                        self.pv_get_str(d2_volt),
                                                                        self.pv_get_str(d2_temp)
                                                                            ))
                #print 't1 changed %f'%value

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):

        #print '%s changed %f'%(pvname,value)

        self.curr_pvname_changed=pvname
        self.call_routine_over_event( self.changeLables )


    SomeNewEvent=None
    def call_routine_over_event(self, handler):

        if self.SomeNewEvent==None:
            self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
            self.Bind(self.EVT_SOME_NEW_EVENT, handler)

            # Create the event
            self.evt = self.SomeNewEvent()


        # Post the event
        wx.PostEvent(self, self.evt)


