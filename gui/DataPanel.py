#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


import wx
import wx.lib.newevent
from epics import PV
from Experiment import *
from PowerSupplyControls import PowerSupplyControls
from thread import start_new_thread
import time

shicane_type=None

class DataPanel(wx.Panel):

    q1_volt='##.##'
    q2_volt='##.##'
    q3_volt='##.##'
    q4_volt='##.##'
    q5_volt='##.##'
    q6_volt='##.##'
    q7_volt='##.##'
    d1_volt='##.##'
    d2_volt='##.##'

    q1_curr='##.##'
    q2_curr='##.##'
    q3_curr='##.##'
    q4_curr='##.##'
    q5_curr='##.##'
    q6_curr='##.##'
    q7_curr='##.##'
    d1_curr='##.##'
    d2_curr='##.##'

    q1_temp='##.##'
    q2_temp='##.##'
    q3_temp='##.##'
    q4_temp='##.##'
    q5_temp='##.##'
    q6_temp='##.##'
    q7_temp='##.##'
    d1_temp='##.##'
    d2_temp='##.##'

    st_quad1 = None
    b_demag = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        #panel2 = wx.Panel(self,-1, style=wx.SUNKEN_BORDER)

        panel = self

        #hbox = wx.BoxSizer(wx.HORIZONTAL)


        ##imageFile = 'pics/schikane_alpha.png'
        #imageFile = 'pics/Quadruplett_2_pos_scaled.png'
        #image = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
        ##image = image.Scale(0.5,0.5)
        #png = image.ConvertToBitmap()
        #imagewx = wx.StaticBitmap(self, -1, png, (5, 5), (png.GetWidth(), png.GetHeight()))
        #hbox.Add(imagewx, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        dy=10
        qy=20

        self.lpos_triplett = {
            'q1': {'x':50,'y':qy},
            'q2': {'x':150,'y':qy},
            'q3': {'x':250,'y':qy},
            'd1': {'x':350,'y':dy},
            'q4': {'x':450,'y':qy},
            'q5': {'x':550,'y':qy},
            'q6': {'x':650,'y':qy},
            'd2': {'x':750,'y':dy},
            'q7': {'x':850,'y':qy},
        }
        self.lpos_quadruplett = {
            'q1': {'x':50,'y':qy},
            'q2': {'x':150,'y':qy},
            'q3': {'x':250,'y':qy},
            'q4': {'x':350,'y':qy},
            'd1': {'x':450,'y':dy},
            'q5': {'x':550,'y':qy},
            'q6': {'x':650,'y':qy},
            'q7': {'x':750,'y':qy},
            'd2': {'x':850,'y':dy},
        }
        global shicane_type
        shicane_type = sys.argv[1]
        if shicane_type=='quadruplett':
            lpos = self.lpos_quadruplett
        elif shicane_type=='triplett':
            lpos = self.lpos_triplett
        else:
            print 'TODO'
            exit(0)

        text_color_quad = (50,30,30)
        text_color_dipol = (10,10,120)

        self.text_color_normal = (50,30,30)
        self.text_color_heigh = (200,30,30)
        self.text_color_hihi = (255,30,30)


        self.font_bold = wx.Font(10, wx.DEFAULT,  wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        def magnet_selected(event,title,magn,st):
            parent.nb.SetSelection(1)
            #print 'notebook tab 1 selection %s'%title
            #st = event.GetEventObject()
            if self.st_selected != None:
                self.st_selected.SetFont(self.font_normal)
            st.SetFont(self.font_bold)
            self.st_selected = st
            parent.tabMagnProperties.magnet_selected(event,title,magn)

        self.st_quad1 = wx.StaticText(label="Quadrupol 1\n#.##V \n#.##A\n##°C",  parent=panel,
                pos=wx.Point(lpos['q1']['x'],lpos['q1']['y']))
        self.st_quad1.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 1',mquad1,self.st_quad1))
        self.st_quad1.SetForegroundColour(text_color_quad)
        #self.st_quad1.SetBackgroundColour((255,0,0))

        self.st_selected = self.st_quad1
        self.st_selected.SetFont(self.font_bold)

        self.st_quad2 = wx.StaticText(label="Quadrupol 2\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q2']['x'],lpos['q2']['y']))
        self.st_quad2.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 2',mquad2,self.st_quad2))
        self.st_quad2.SetForegroundColour(text_color_quad)

        self.st_quad3 = wx.StaticText(label="Quadrupol 3\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q3']['x'],lpos['q3']['y']))
        self.st_quad3.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 3',mquad3,self.st_quad3))
        self.st_quad3.SetForegroundColour(text_color_quad)

        self.st_quad4 = wx.StaticText(label="Quadrupol 4\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q4']['x'],lpos['q4']['y']))
        self.st_quad4.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 4',mquad4,self.st_quad4))
        self.st_quad4.SetForegroundColour(text_color_quad)

        self.st_quad5 = wx.StaticText(label="Quadrupol 5\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q5']['x'],lpos['q5']['y']))
        self.st_quad5.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 5',mquad5,self.st_quad5))
        self.st_quad5.SetForegroundColour(text_color_quad)

        self.st_quad6 = wx.StaticText(label="Quadrupol 6\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q6']['x'],lpos['q6']['y']))
        self.st_quad6.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 6',mquad6,self.st_quad6))
        self.st_quad6.SetForegroundColour(text_color_quad)

        self.st_quad7=None
        if shicane_type=='quadruplett':
            self.st_quad7 = wx.StaticText(label="Quadrupol 7\n#.##V \n#.##A\n##°C",  parent=panel,
                pos=wx.Point(lpos['q7']['x'],lpos['q7']['y']))
            self.st_quad7.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 7',mquad7,self.st_quad7))
            self.st_quad7.SetForegroundColour(text_color_quad)

        self.st_dipol1 = wx.StaticText(label="Dipol      \n#.##V \n#.##A\n##°C", parent=panel,
                pos=wx.Point(lpos['d1']['x'],lpos['d1']['y']))
        self.st_dipol1.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Dipol 1',mdipol1,self.st_dipol1))
        self.st_dipol1.SetForegroundColour(text_color_dipol)

        self.st_dipol2 = wx.StaticText(label="Dipol 2    \n#.##V\n#.##A\n##°C",  parent=panel,
                pos=wx.Point(lpos['d2']['x'],lpos['d2']['y']))
        self.st_dipol2.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Dipol 2',mdipol2,self.st_dipol2))
        self.st_dipol2.SetForegroundColour(text_color_dipol)

        self.st_arr = [self.st_quad1, self.st_quad2, self.st_quad3, self.st_quad4, self.st_quad5, self.st_quad6, self.st_quad7, self.st_dipol1, self.st_dipol2]

        if shicane_type=='quadruplett':
            self.st_text_color_arr = [text_color_quad, text_color_quad, text_color_quad, text_color_quad,
                            text_color_dipol,
                            text_color_quad, text_color_quad, text_color_quad,
                            text_color_dipol]
        else:
            self.st_text_color_arr = [text_color_quad, text_color_quad, text_color_quad, text_color_quad,
                        text_color_dipol,
                        text_color_quad, text_color_quad, text_color_quad,
                        text_color_dipol]

        #self.b_demag = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Demag")
        #self.b_demag.Bind(wx.EVT_BUTTON, self.OnDemag)
        #panel.SetSizer(hbox)

        #q1_volt.add_callback(self.onPVChanges)
        #q1_curr.add_callback(self.onPVChanges)
        #q1_temp.add_callback(self.onPVChanges)

        #q2_volt.add_callback(self.onPVChanges)
        #q2_curr.add_callback(self.onPVChanges)
        #q2_temp.add_callback(self.onPVChanges)

        #q3_volt.add_callback(self.onPVChanges)
        #q3_curr.add_callback(self.onPVChanges)
        #q3_temp.add_callback(self.onPVChanges)

        #q4_volt.add_callback(self.onPVChanges)
        #q4_curr.add_callback(self.onPVChanges)
        #q4_temp.add_callback(self.onPVChanges)

        #q5_volt.add_callback(self.onPVChanges)
        #q5_curr.add_callback(self.onPVChanges)
        #q5_temp.add_callback(self.onPVChanges)

        #q6_volt.add_callback(self.onPVChanges)
        #q6_curr.add_callback(self.onPVChanges)
        #q6_temp.add_callback(self.onPVChanges)

        #q7_volt.add_callback(self.onPVChanges)
        #q7_curr.add_callback(self.onPVChanges)
        #q7_temp.add_callback(self.onPVChanges)

        #d1_volt.add_callback(self.onPVChanges)
        #d1_curr.add_callback(self.onPVChanges)
        #d1_temp.add_callback(self.onPVChanges)

        #d2_volt.add_callback(self.onPVChanges)
        #d2_curr.add_callback(self.onPVChanges)
        #d2_temp.add_callback(self.onPVChanges)

        self.q1_volt=q1_volt.get()
        self.q2_volt=q2_volt.get()
        self.q3_volt=q3_volt.get()
        self.q4_volt=q4_volt.get()
        self.q5_volt=q5_volt.get()
        self.q6_volt=q6_volt.get()
        self.q7_volt=q7_volt.get()
        self.d1_volt=d1_volt.get()
        self.d2_volt=d2_volt.get()

        self.q1_curr=q1_curr.get()
        self.q2_curr=q2_curr.get()
        self.q3_curr=q3_curr.get()
        self.q4_curr=q4_curr.get()
        self.q5_curr=q5_curr.get()
        self.q6_curr=q6_curr.get()
        self.q7_curr=q7_curr.get()
        self.d1_curr=d1_curr.get()
        self.d2_curr=d2_curr.get()

        self.q1_temp=q1_temp.get()
        self.q2_temp=q2_temp.get()
        self.q3_temp=q3_temp.get()
        self.q4_temp=q4_temp.get()
        self.q5_temp=q5_temp.get()
        self.q6_temp=q6_temp.get()
        self.q7_temp=q7_temp.get()
        self.d1_temp=d1_temp.get()
        self.d2_temp=d2_temp.get()

        self.q1_k=0
        self.q2_k=0
        self.q3_k=0
        self.q4_k=0
        self.q5_k=0
        self.q6_k=0
        self.q7_k=0
        self.d1_alpha=0
        self.d2_alpha=0


        self.temp_all_arr = [self.q1_temp,self.q3_temp,self.q3_temp,self.q4_temp,self.q5_temp,self.q6_temp,self.q7_temp,self.d1_temp,self.d2_temp]
        self.temp_heigh = 70
        self.temp_hihi = 95
        self.temp_cnt = 9


        # refresh labels
        self.alive=True
        def refresh_labels():
            # TODO Thread beim beenden beenden
            while self.alive:
                #self.call_routine_over_event( self.changeLables )
                self.call_routine_over_event( self.labels_update )
                time.sleep(0.5)
        start_new_thread(refresh_labels,())

        time.sleep(0.1)
        temp_all.add_callback(self.onPVChanges)
        ps_curr_all.add_callback(self.onPVChanges)
        ps_volt_all.add_callback(self.onPVChanges)


    def __del__(self):
        self.alive=False
        time.sleep(0.5)

    def OnDemag(self, event):
        def demagThread():
            self.b_demag.Enable(False)
            demag()
            self.b_demag.Enable(True)

        start_new_thread( demagThread,() )

    def pv_get_str(self, pv):
        #print 'DataPanel.pv_get_str ',pv
        value = pv.get()
        str_val = '##.###'
        if value!=None:
            str_val = '%.3f'%value
        return str_val




    def labels_update(self,evt):

        # test for heigh temperature
        for i in range(0,self.temp_cnt):
            if self.st_arr[i]==None: continue
            t = float(self.temp_all_arr[i])
            if t < self.temp_heigh:
                self.st_arr[i].SetForegroundColour(self.text_color_normal)
            if self.temp_heigh <= t and t < self.temp_hihi:
                #print self.st_arr[i]
                self.st_arr[i].SetForegroundColour(self.text_color_heigh)
                #print 'temperature heigh %0.3f q%d'%(t,(i+1))
            elif t >= self.temp_hihi:
                #print 'temperature too heigh for q%d, please start demag!!!'%(i+1)
                self.st_arr[i].SetForegroundColour(self.text_color_hihi)


        global shicane_type, mquad1, mquad2, mquad3, mquad4, mquad5, mquad6, mquad7, mdipol1, mdipol2
        self.st_quad1.SetLabel("Quadrupol 1\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q1_volt,self.q1_curr,self.q1_temp,self.q1_k))
        self.st_quad2.SetLabel("Quadrupol 2\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q2_volt,self.q2_curr,self.q2_temp,self.q2_k))
        self.st_quad3.SetLabel("Quadrupol 3\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q3_volt,self.q3_curr,self.q3_temp,self.q3_k))
        self.st_quad4.SetLabel("Quadrupol 4\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q4_volt,self.q4_curr,self.q4_temp,self.q4_k))
        self.st_quad5.SetLabel("Quadrupol 5\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q5_volt,self.q5_curr,self.q5_temp,self.q5_k))
        self.st_quad6.SetLabel("Quadrupol 6\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q6_volt,self.q6_curr,self.q6_temp,self.q6_k))
        if shicane_type=='quadruplett':
            self.st_quad7.SetLabel("Quadrupol 7\n%s V \n%s A\n%s °C\n%.2f [1/m]" %(self.q7_volt,self.q7_curr,self.q7_temp,self.q7_k))
        self.st_dipol1.SetLabel("Dipol 1\n%s V \n%s A\n%s °C\n%.2f [mrad]" %(self.d1_volt,self.d1_curr,self.d1_temp,self.d1_alpha))
        self.st_dipol2.SetLabel("Dipol 2\n%s V \n%s A\n%s °C\n%.2f [mrad]" %(self.d2_volt,self.d2_curr,self.d2_temp,self.d2_alpha))





#    curr_pvname_changed = None
#    def changeLables_depr(self,evt):
#        pvname = self.curr_pvname_changed
#
#        #global quad1, quad2, quad3, quad4, quad5, quad6, quad7, dipol1, dipol2
#
#        #print pvname
#        if pvname == q1_volt.pvname  or pvname == q1_curr.pvname or pvname == q1_temp.pvname:
#            self.st_quad1.SetLabel("Quadrupol 1\n%s V \n%s A\n%s °C" %(self.pv_get_str(q1_volt),
#                                                                        self.pv_get_str(q1_volt),
#                                                                        self.pv_get_str(q1_temp)
#                                                                            ))
#        elif pvname == q2_volt.pvname  or pvname == q2_curr.pvname or pvname == q2_temp.pvname:
#            self.st_quad2.SetLabel("Quadrupol 2\n%s V \n%s A\n%s °C" %(self.pv_get_str(q2_volt),
#                                                                        self.pv_get_str(q2_volt),
#                                                                        self.pv_get_str(q2_temp)
#                                                                            ))
#        elif pvname == q3_volt.pvname  or pvname == q3_curr.pvname or pvname == q3_temp.pvname:
#            self.st_quad3.SetLabel("Quadrupol 3\n%s V \n%s A\n%s °C" %(self.pv_get_str(q3_volt),
#                                                                        self.pv_get_str(q3_volt),
#                                                                        self.pv_get_str(q3_temp)
#                                                                            ))
#        elif pvname == q4_volt.pvname  or pvname == q4_curr.pvname or pvname == q4_temp.pvname:
#            self.st_quad4.SetLabel("Quadrupol 4\n%s V \n%s A\n%s °C" %(self.pv_get_str(q4_volt),
#                                                                        self.pv_get_str(q4_volt),
#                                                                        self.pv_get_str(q4_temp)
#                                                                            ))
#        elif pvname == q5_volt.pvname  or pvname == q5_curr.pvname or pvname == q5_temp.pvname:
#            self.st_quad5.SetLabel("Quadrupol 5\n%s V \n%s A\n%s °C" %(self.pv_get_str(q5_volt),
#                                                                        self.pv_get_str(q5_volt),
#                                                                        self.pv_get_str(q5_temp)
#                                                                            ))
#        elif pvname == q6_volt.pvname  or pvname == q6_curr.pvname or pvname == q6_temp.pvname:
#            self.st_quad6.SetLabel("Quadrupol 6\n%s V \n%s A\n%s °C" %(self.pv_get_str(q6_volt),
#                                                                        self.pv_get_str(q6_volt),
#                                                                        self.pv_get_str(q6_temp)
#                                                                            ))
#        elif pvname == q7_volt.pvname  or pvname == q7_curr.pvname or pvname == q7_temp.pvname:
#            self.st_quad7.SetLabel("Quadrupol 7\n%s V \n%s A\n%s °C" %(self.pv_get_str(q7_volt),
#                                                                        self.pv_get_str(q7_volt),
#                                                                        self.pv_get_str(q7_temp)
#                                                                            ))
#        elif pvname == d1_volt.pvname  or pvname == d1_curr.pvname or pvname == d1_temp.pvname:
#            self.st_dipol1.SetLabel("Dipol 1\n%s V \n%s A\n%s °C" %(self.pv_get_str(d1_volt),
#                                                                        self.pv_get_str(d1_volt),
#                                                                        self.pv_get_str(d1_temp)
#                                                                            ))
#        elif pvname == d2_volt.pvname  or pvname == d2_curr.pvname or pvname == d2_temp.pvname:
#            self.st_dipol2.SetLabel("Dipol 2\n%s V \n%s A\n%s °C" %(self.pv_get_str(d2_volt),
#                                                                        self.pv_get_str(d2_volt),
#                                                                        self.pv_get_str(d2_temp)
#                                                                            ))
#                #print 't1 changed %f'%value

    def onPVChanges(self, pvname=None, value=None, char_value=None, **kw):

        global mquad1, mquad2, mquad3, mquad4, mquad5, mquad6, mquad7, mdipol1, mdipol2

        relee_plus=0
        relee_minus=24
        sign=None

        if pvname==temp_all.pvname:
            arr = value.tostring().split(' ')
            self.temp_all_arr = arr[:self.temp_cnt]
            try:
                self.q1_temp=arr[0]
                self.q2_temp=arr[1]
                self.q3_temp=arr[2]
                self.q4_temp=arr[3]
                self.q5_temp=arr[4]
                self.q6_temp=arr[5]
                self.q7_temp=arr[6]
                self.d1_temp=arr[7]
                self.d2_temp=arr[8]

            except Exception as e:
                print 'temp_all: ',e

        elif pvname==ps_volt_all.pvname:
            #print type(value)
            arr = value.tostring().split(' ')
            relee=round(float(arr[0]))
            if relee==relee_plus: sign=1
            else: sign=-1
            try:
                self.q1_volt=sign*float(arr[1])
                self.q2_volt=sign*float(arr[2])
                self.q3_volt=sign*float(arr[3])
                self.q4_volt=sign*float(arr[4])
                self.q5_volt=sign*float(arr[5])
                self.q6_volt=sign*float(arr[6])
                self.q7_volt=sign*float(arr[7])
                self.d1_volt=sign*float(arr[8])
                self.d2_volt=sign*float(arr[9])
            except Exception as e:
                print 'volt_all:',e

        elif pvname==ps_curr_all.pvname:
            arr = value.tostring().split(' ')
            relee=round(float(arr[0]))
            if relee==relee_plus: sign=1
            else: sign=-1
            try:
                self.q1_curr=sign*float(arr[1])
                self.q2_curr=sign*float(arr[2])
                self.q3_curr=sign*float(arr[3])
                self.q4_curr=sign*float(arr[4])
                self.q5_curr=sign*float(arr[5])
                self.q6_curr=sign*float(arr[6])
                self.q7_curr=sign*float(arr[7])
                self.d1_curr=sign*float(arr[8])
                self.d2_curr=sign*float(arr[9])

                self.q1_k=mquad1.get_k(float(arr[1]))
                self.q2_k=mquad2.get_k(float(arr[2]))
                self.q3_k=mquad3.get_k(float(arr[3]))
                self.q4_k=mquad4.get_k(float(arr[4]))
                self.q5_k=mquad5.get_k(float(arr[5]))
                self.q6_k=mquad6.get_k(float(arr[6]))
                self.q7_k=mquad7.get_k(float(arr[7]))
                self.d1_alpha=mdipol1.get_k(float(arr[8]))
                self.d2_alpha=mdipol2.get_k(float(arr[9]))
            except Exception as e:
                print 'temp_all:',e

    SomeNewEvent=None
    def call_routine_over_event(self, handler):

        if self.SomeNewEvent==None:
            self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
            self.Bind(self.EVT_SOME_NEW_EVENT, handler)

            # Create the event
            self.evt = self.SomeNewEvent()


        # Post the event
        wx.PostEvent(self, self.evt)


