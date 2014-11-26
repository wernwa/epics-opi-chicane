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
import traceback

chicane_type=None





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

        self.start_app_time = time.time()
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
        global chicane_type
        chicane_type = sys.argv[1]
        if chicane_type=='quadruplett':
            lpos = self.lpos_quadruplett
        elif chicane_type=='triplett':
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

        image_disconn = wx.Image('pics/disconnected.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image_green = wx.Image('pics/green-status.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image_gray = wx.Image('pics/gray-status.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        def ps_onoff(event,magnet,button):
            output = magnet.ps.output.get()
            #print magnet.ps.output.pvname, magnet.ps.output.get()
            #print magnet.ps.online.pvname, magnet.ps.online.get()
            if output == 0:
                magnet.ps.output.put(1)
                button.SetBitmapLabel(image_green)
                button.Refresh()
            elif output == 1:
                magnet.ps.output.put(0)
                button.SetBitmapLabel(image_gray)
                button.Refresh()

        def ps_online(magnet,button):
            online = magnet.ps.online.get()
            if online == 0:
                button.SetBitmapLabel(image_disconn)
            elif online == 1:
                output = magnet.ps.output.get()
                if output == 0: button.SetBitmapLabel(image_gray)
                elif output == 1: button.SetBitmapLabel(image_green)
                button.Refresh()

            print magnet.ps.online.pvname


        # quad 1
        self.st_quad1 = wx.StaticText(label="Quadrupol 1\n#.##V \n#.##A\n##°C",  parent=panel,
                pos=wx.Point(lpos['q1']['x'],lpos['q1']['y']))
        self.st_quad1.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 1',mquad1,self.st_quad1))
        self.st_quad1.SetForegroundColour(text_color_quad)
        self.bps_quad1 = wx.BitmapButton(panel, id=-1, bitmap=image_disconn,
                pos=wx.Point(lpos['q1']['x']+20,lpos['q1']['y']+90), size =(image_disconn.GetWidth()+10, image_disconn.GetHeight()+10))
        self.bps_quad1.Bind(wx.EVT_BUTTON, lambda event: ps_onoff(event,mquad1,self.bps_quad1))
        mquad1.ps.online.add_callback(lambda **kw: ps_online(mquad1,self.bps_quad1))
        ps_online(mquad1,self.bps_quad1)

        self.st_selected = self.st_quad1
        self.st_selected.SetFont(self.font_bold)

        # quad 2
        self.st_quad2 = wx.StaticText(label="Quadrupol 2\n#.##V\n#.##A\n##°C",   parent=panel,
                pos=wx.Point(lpos['q2']['x'],lpos['q2']['y']))
        self.st_quad2.Bind(wx.EVT_LEFT_DOWN, lambda event: magnet_selected(event, 'Quadrupol 2',mquad2,self.st_quad2))
        self.st_quad2.SetForegroundColour(text_color_quad)
        self.bps_quad2 = wx.BitmapButton(panel, id=-1, bitmap=image_disconn,
                pos=wx.Point(lpos['q2']['x']+20,lpos['q2']['y']+90), size =(image_disconn.GetWidth()+10, image_disconn.GetHeight()+10))
        self.bps_quad2.Bind(wx.EVT_BUTTON, lambda event: ps_onoff(event,mquad2,self.bps_quad2))
        mquad2.ps.online.add_callback(lambda **kw: ps_online(mquad2,self.bps_quad2))
        ps_online(mquad2,self.bps_quad2)

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
        if chicane_type=='quadruplett':
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

        if chicane_type=='quadruplett':
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

        value = magn_volt_all.get()
        arr = value.tostring().split(' ')
        self.q1_volt=self.get_num_or_dash(arr[0])
        self.q2_volt=self.get_num_or_dash(arr[1])
        self.q3_volt=self.get_num_or_dash(arr[2])
        self.q4_volt=self.get_num_or_dash(arr[3])
        self.q5_volt=self.get_num_or_dash(arr[4])
        self.q6_volt=self.get_num_or_dash(arr[5])
        self.q7_volt=self.get_num_or_dash(arr[6])
        self.d1_volt=self.get_num_or_dash(arr[7])
        self.d2_volt=self.get_num_or_dash(arr[8])

        value = magn_curr_all.get()
        arr = value.tostring().split(' ')
        self.q1_curr=self.get_num_or_dash(arr[0])
        self.q2_curr=self.get_num_or_dash(arr[1])
        self.q3_curr=self.get_num_or_dash(arr[2])
        self.q4_curr=self.get_num_or_dash(arr[3])
        self.q5_curr=self.get_num_or_dash(arr[4])
        self.q6_curr=self.get_num_or_dash(arr[5])
        self.q7_curr=self.get_num_or_dash(arr[6])
        self.d1_curr=self.get_num_or_dash(arr[7])
        self.d2_curr=self.get_num_or_dash(arr[8])


        if self.q1_curr!='##.##': self.q1_k=mquad1.get_k(self.q1_curr)
        else: self.q1_k='##.##'
        if self.q2_curr!='##.##': self.q2_k=mquad2.get_k(self.q2_curr)
        else: self.q2_k='##.##'
        if self.q3_curr!='##.##': self.q3_k=mquad3.get_k(self.q3_curr)
        else: self.q3_k='##.##'
        if self.q4_curr!='##.##': self.q4_k=mquad4.get_k(self.q4_curr)
        else: self.q4_k='##.##'
        if self.q5_curr!='##.##': self.q5_k=mquad5.get_k(self.q5_curr)
        else: self.q5_k='##.##'
        if self.q6_curr!='##.##': self.q6_k=mquad6.get_k(self.q6_curr)
        else: self.q6_k='##.##'
        if self.q7_curr!='##.##': self.q7_k=mquad7.get_k(self.q7_curr)
        else: self.q7_k='##.##'
        if self.d1_curr!='##.##': self.d1_alpha=mdipol1.get_k(self.d1_curr)
        else: self.d1_alpha='##.##'
        if self.d2_curr!='##.##': self.d2_alpha=mdipol2.get_k(self.d2_curr)
        else: self.d2_alpha='##.##'

        value = temp_all.get()
        arr = value.tostring().split(' ')
        self.q1_temp=self.get_num_or_dash(arr[0])
        self.q2_temp=self.get_num_or_dash(arr[1])
        self.q3_temp=self.get_num_or_dash(arr[2])
        self.q4_temp=self.get_num_or_dash(arr[3])
        self.q5_temp=self.get_num_or_dash(arr[4])
        self.q6_temp=self.get_num_or_dash(arr[5])
        self.q7_temp=self.get_num_or_dash(arr[6])
        self.d1_temp=self.get_num_or_dash(arr[7])
        self.d2_temp=self.get_num_or_dash(arr[8])

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
        magn_curr_all.add_callback(self.onPVChanges)
        magn_volt_all.add_callback(self.onPVChanges)


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
            if self.st_arr[i]==None or self.temp_all_arr[i]==None:
                continue
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


        global chicane_type, mquad1, mquad2, mquad3, mquad4, mquad5, mquad6, mquad7, mdipol1, mdipol2
        self.st_quad1.SetLabel("Quadrupol 1\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q1_volt,self.q1_curr,self.q1_k,self.q1_temp))
        self.st_quad2.SetLabel("Quadrupol 2\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q2_volt,self.q2_curr,self.q2_k,self.q2_temp))
        self.st_quad3.SetLabel("Quadrupol 3\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q3_volt,self.q3_curr,self.q3_k,self.q3_temp))
        self.st_quad4.SetLabel("Quadrupol 4\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q4_volt,self.q4_curr,self.q4_k,self.q4_temp))
        self.st_quad5.SetLabel("Quadrupol 5\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q5_volt,self.q5_curr,self.q5_k,self.q5_temp))
        self.st_quad6.SetLabel("Quadrupol 6\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q6_volt,self.q6_curr,self.q6_k,self.q6_temp))
        if chicane_type=='quadruplett':
            self.st_quad7.SetLabel("Quadrupol 7\n%s V \n%s A\n%s [1/m]\n%s °C" %(self.q7_volt,self.q7_curr,self.q7_k,self.q7_temp))
        self.st_dipol1.SetLabel("Dipol 1\n%s V \n%s A\n%s [mrad]\n%s °C" %(self.d1_volt,self.d1_curr,self.d1_alpha,self.d1_temp))
        self.st_dipol2.SetLabel("Dipol 2\n%s V \n%s A\n%s [mrad]\n%s °C" %(self.d2_volt,self.d2_curr,self.d2_alpha,self.d2_temp))



    # for the convertion from pv-array,
    # display a number or if None the dashes
    def get_num_or_dash(self,obj):
        if obj == 'None' or obj == None: return '##.##'
        else:
            try:
                num = float(obj)
            except Exception as e:
                print traceback.format_exc()

            return num



    def onPVChanges(self, pvname=None, value=None, timestamp=None, **kw):

        global mquad1, mquad2, mquad3, mquad4, mquad5, mquad6, mquad7, mdipol1, mdipol2

        marr = [mquad1, mquad2, mquad3, mquad4, mquad5, mquad6, mquad7, mdipol1, mdipol2]
        q_volt_arr = [self.q1_volt, self.q2_volt, self.q3_volt, self.q4_volt, self.q5_volt, self.q6_volt, self.q7_volt,
                    self.d1_volt, self.d2_volt ]

        if 'online' in pvname:
            print pvname

        if pvname==temp_all.pvname:
            arr = value.tostring().split(' ')
            self.temp_all_arr = arr[:self.temp_cnt]
            try:
                self.q1_temp=self.get_num_or_dash(arr[0])
                self.q2_temp=self.get_num_or_dash(arr[1])
                self.q3_temp=self.get_num_or_dash(arr[2])
                self.q4_temp=self.get_num_or_dash(arr[3])
                self.q5_temp=self.get_num_or_dash(arr[4])
                self.q6_temp=self.get_num_or_dash(arr[5])
                self.q7_temp=self.get_num_or_dash(arr[6])
                self.d1_temp=self.get_num_or_dash(arr[7])
                self.d2_temp=self.get_num_or_dash(arr[8])


                # fill in the numpy arrays for StripChart visualisation
                for i in range(0,len(marr)):
                    if arr[i]=='None': continue
                    marr[i].strip_chart_temp.append(float(arr[i]))
                    #print 'start_app_time',type(self.start_app_time)
                    #print 'temp_all',type(temp_all)
                    # strange Error for temp_all.timestamp=NoneType
                    #marr[i].strip_chart_temp_time.append(temp_all.timestamp-self.start_app_time)
                    marr[i].strip_chart_temp_time.append(time.time()-self.start_app_time)


            except Exception as e:
                #print 'temp_all: ',e
                print traceback.format_exc()

        elif pvname==magn_volt_all.pvname:
            #print type(value)
            arr = value.tostring().split(' ')
            #print 'volt arr',arr
            try:
                #for i in range(0,len(q_volt_arr)):
                #    if arr[i] == 'None':
                #        q_volt = q_volt_arr[i]
                #        q_volt = '##.##'
                #        print self.q1_volt
                #    else:
                #        self.q1_volt=float(arr[i])
                self.q1_volt=self.get_num_or_dash(arr[0])
                self.q2_volt=self.get_num_or_dash(arr[1])
                self.q3_volt=self.get_num_or_dash(arr[2])
                self.q4_volt=self.get_num_or_dash(arr[3])
                self.q5_volt=self.get_num_or_dash(arr[4])
                self.q6_volt=self.get_num_or_dash(arr[5])
                self.q7_volt=self.get_num_or_dash(arr[6])
                self.d1_volt=self.get_num_or_dash(arr[7])
                self.d2_volt=self.get_num_or_dash(arr[8])

                # fill in the numpy arrays for StripChart visualisation
                for i in range(0,len(marr)):
                    if arr[i]=='None': continue
                    marr[i].strip_chart_volt.append(arr[i])
                    marr[i].strip_chart_volt_time.append(time.time()-self.start_app_time)

            except Exception as e:
                #print 'volt_all:',e
                print traceback.format_exc()

        elif pvname==magn_curr_all.pvname:
            arr = value.tostring().split(' ')
            #relee=round(float(arr[0]))
            #if relee==relee_plus: sign=1
            #else: sign=-1
            try:
                self.q1_curr=self.get_num_or_dash(arr[0])
                self.q2_curr=self.get_num_or_dash(arr[1])
                self.q3_curr=self.get_num_or_dash(arr[2])
                self.q4_curr=self.get_num_or_dash(arr[3])
                self.q5_curr=self.get_num_or_dash(arr[4])
                self.q6_curr=self.get_num_or_dash(arr[5])
                self.q7_curr=self.get_num_or_dash(arr[6])
                self.d1_curr=self.get_num_or_dash(arr[7])
                self.d2_curr=self.get_num_or_dash(arr[8])

                if self.q1_curr!='##.##': self.q1_k=mquad1.get_k(self.q1_curr)
                else: self.q1_k='##.##'
                if self.q2_curr!='##.##': self.q2_k=mquad2.get_k(self.q2_curr)
                else: self.q2_k='##.##'
                if self.q3_curr!='##.##': self.q3_k=mquad3.get_k(self.q3_curr)
                else: self.q3_k='##.##'
                if self.q4_curr!='##.##': self.q4_k=mquad4.get_k(self.q4_curr)
                else: self.q4_k='##.##'
                if self.q5_curr!='##.##': self.q5_k=mquad5.get_k(self.q5_curr)
                else: self.q5_k='##.##'
                if self.q6_curr!='##.##': self.q6_k=mquad6.get_k(self.q6_curr)
                else: self.q6_k='##.##'
                if self.q7_curr!='##.##': self.q7_k=mquad7.get_k(self.q7_curr)
                else: self.q7_k='##.##'
                if self.d1_curr!='##.##': self.d1_alpha=mdipol1.get_k(self.d1_curr)
                else: self.d1_alpha='##.##'
                if self.d2_curr!='##.##': self.d2_alpha=mdipol2.get_k(self.d2_curr)
                else: self.d2_alpha='##.##'
                #self.q1_k=mquad1.get_k(float(arr[0]))
                #self.q2_k=mquad2.get_k(float(arr[1]))
                #self.q3_k=mquad3.get_k(float(arr[2]))
                #self.q4_k=mquad4.get_k(float(arr[3]))
                #self.q5_k=mquad5.get_k(float(arr[4]))
                #self.q6_k=mquad6.get_k(float(arr[5]))
                #self.q7_k=mquad7.get_k(float(arr[6]))
                #self.d1_alpha=mdipol1.get_k(float(arr[7]))
                #self.d2_alpha=mdipol2.get_k(float(arr[8]))

                # fill in the numpy arrays for StripChart visualisation
                for i in range(0,len(marr)):
                    if arr[i]=='None': continue
                    marr[i].strip_chart_curr.append(float(arr[i]))
                    marr[i].strip_chart_curr_time.append(time.time()-self.start_app_time)

            except Exception as e:
                #print 'temp_all:',e
                print traceback.format_exc()


    # call the main thread throgh messaging for painting the gui
    SomeNewEvent=None
    def call_routine_over_event(self, handler):

        if self.SomeNewEvent==None:
            self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
            self.Bind(self.EVT_SOME_NEW_EVENT, handler)

            # Create the event
            self.evt = self.SomeNewEvent()


        # Post the event
        wx.PostEvent(self, self.evt)


