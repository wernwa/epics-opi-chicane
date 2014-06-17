#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------

import io
import os
import wx
import wx.lib.newevent
from epics import PV
from Experiment import *
from PowerSupplyControls import PowerSupplyControls
from thread import start_new_thread
import pipes
import tempfile
from random import random
import time


class StripChartMemory:
    time = []
    data = []


    def __init__(self, limit=60):
        self.limit = limit

    def add(self, t,d):
        self.time.append(t)
        self.data.append(d)

        #self.time.insert(0,t)
        #self.data.insert(0,d)

    def delete_data_over_limit(self):
        time_now = time.time()

        for i in range(len(self.time)):
            if self.time[i] < time_now - self.limit:
                del self.time[i:len(self.time)]
                del self.data[i:len(self.data)]
                break


class TabStripChart(wx.Panel):

    use_pipes_for_gnuplot = True

    st_quad1 = None
    b_show = None
    imagewx = None

    chart_data_pipe = 'strip-chart-data'
    chart_image_pipe = 'strip-chart-image'
    chart_gp_pipe = 'strip-chart-gp'
    chart_gp_file = 'strip-chart.gp'

    strip_random = StripChartMemory()
    strip_chart_continue = False

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)




        self.b_show = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Start StripChart")
        self.b_show.Bind(wx.EVT_BUTTON, self.OnStartStop_StripChart)
        panel.SetSizer(hbox)

        # init the pipes for gnuplot

        if self.use_pipes_for_gnuplot:
            os.system('FILE=%s; if [ ! -f $FILE ]; then mkfifo $FILE; fi' %(self.chart_data_pipe))
            os.system('FILE=%s; if [ ! -f $FILE ]; then mkfifo $FILE; fi' %(self.chart_image_pipe))
            os.system('FILE=%s; if [ ! -f $FILE ]; then mkfifo $FILE; fi' %(self.chart_gp_pipe))


        def fill_random_data():
            while True:
                self.strip_random.add(time.time(), (random()+random())*random())
                time.sleep(1+random())
        start_new_thread( fill_random_data ,() )





    # StripChart start stop
    def OnStartStop_StripChart(self, event):
        self.strip_chart_continue = not(self.strip_chart_continue)
        def StripChartLoop():
            while self.strip_chart_continue:
                if self.use_pipes_for_gnuplot:
                    self.UpdateStripChart(event)
                else:
                    self.UpdateStripChart2(event)
                time.sleep(0.5)
        if self.strip_chart_continue == True:
            self.b_show.SetLabel('stop')
            start_new_thread( StripChartLoop,() )
        else:
            self.b_show.SetLabel('start')




    def UpdateStripChart(self, event):

        start_time = time.time()



        def writeGPlotData():
            self.strip_random.delete_data_over_limit()
            data = '# t random\n'
            print 'data count %d'%len(self.strip_random.time)
            for i in range(len(self.strip_random.time)):
                time_now = time.time()
                data += '%0.0f %0.3f\n' %(self.strip_random.time[i]-time_now,self.strip_random.data[i])
            #print data
            with io.open(self.chart_data_pipe, 'w') as f:
                f.write(unicode(data))
                f.close()
        start_new_thread( writeGPlotData ,() )

        with io.open(self.chart_gp_file, 'r') as f:
            gp_commands_str = f.read()
            f.close()

        def startGnuPlot():
            os.system('gnuplot %s' %self.chart_gp_pipe)
        start_new_thread( startGnuPlot ,() )

        ### write gnuplot commands ###
        with io.open(self.chart_gp_pipe,'w') as gp_pipe:
            gp_pipe.write(gp_commands_str)
            gp_pipe.close()


        ## gui changes call from main process
        def last_part_for_event_gui(evt):
            ### read image data produced by gnuplot ###
            with io.open(self.chart_image_pipe, 'rb') as pipe_pipe:
                buff = pipe_pipe.read()
                stream = io.BytesIO(buff)
                image = wx.ImageFromStream(stream).ConvertToBitmap()
                pipe_pipe.close()


            if self.imagewx == None:
                self.imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))
            else:
                self.imagewx.SetBitmap(image)

            diff_time = time.time() - start_time

            print '%0.3fs' %(diff_time)
        self.call_routine_over_event( last_part_for_event_gui )


    def __del__(self):
        ### delete temporary gnuplot files ###
        os.system('FILE=%s; if [ -e $FILE ]; then rm $FILE; fi' %(self.chart_data_pipe))
        os.system('FILE=%s; if [ -e $FILE ]; then rm $FILE; fi' %(self.chart_image_pipe))
        os.system('FILE=%s; if [ -e $FILE ]; then rm $FILE; fi' %(self.chart_gp_pipe))


    # UpdateStripChart without pipes
    def UpdateStripChart2(self, event=None):

        start_time = time.time()


        def writeGPlotData():
            self.strip_random.delete_data_over_limit()
            data = '# t random\n'
            for i in range(len(self.strip_random.time)):
                time_now = time.time()
                data += '%0.0f %0.3f\n' %(self.strip_random.time[i]-time_now,self.strip_random.data[i])
            #print data
            with io.open(self.chart_data_pipe, 'w') as f:
                f.write(unicode(data))
                f.close()
        writeGPlotData()

        os.system('gnuplot %s' %self.chart_gp_file)


        ## gui changes call from main process
        def last_part_for_event_gui(evt):
            image = wx.Image(self.chart_image_pipe).ConvertToBitmap()

            if self.imagewx == None:
                self.imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))
            else:
                self.imagewx.SetBitmap(image)

            diff_time = time.time() - start_time

            print '%0.3fs' %(diff_time)


        self.call_routine_over_event( last_part_for_event_gui )


    SomeNewEvent=None
    def call_routine_over_event(self, handler):

        if self.SomeNewEvent==None:
            self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
            self.Bind(self.EVT_SOME_NEW_EVENT, handler)

            # Create the event
            self.evt = self.SomeNewEvent()

        # Post the event
        wx.PostEvent(self, self.evt)
