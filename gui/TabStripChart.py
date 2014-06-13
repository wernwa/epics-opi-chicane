#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------

import io
import os
import wx
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

    #def __init__(self):
    #    time

    def add(self, t,d):
        self.time.insert(0,t)
        self.data.insert(0,d)


class TabStripChart(wx.Panel):

    st_quad1 = None
    b_show = None
    imagewx = None

    chart_data_pipe = 'strip-chart-data'
    chart_image_pipe = 'strip-chart-image'
    chart_gp_pipe = 'strip-chart-gp'
    chart_gp_file = 'strip-chart.gp'

    strip_random = StripChartMemory()

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        self.b_show = wx.Button(parent=panel, pos=wx.Point(50, 490), label="LoadStat")
        self.b_show.Bind(wx.EVT_BUTTON, self.OnLoadStat)
        panel.SetSizer(hbox)

        # init the pipes for gnuplot
        os.system('mkfifo %s' %self.chart_data_pipe)
        os.system('mkfifo %s' %self.chart_image_pipe)
        os.system('mkfifo %s' %self.chart_gp_pipe)

        def fill_random_data():
            while True:
                self.strip_random.add(time.time(), random())
                time.sleep(1+random())
        start_new_thread( fill_random_data ,() )


#    def OnLoadStat2(self, event):
#
#        start_time = time.time()
#
#        data = '# t random\n'
#        for i in range(1,100):
#            data += '%i %0.3f\n' %(i,random())
#            with io.open('random.dat', 'w') as f:
#                f.write(unicode(data))
#                f.close()
#        os.system('gnuplot random.gp')
#
#
#        image = wx.Image('random.png').ConvertToBitmap()
#
#        if self.imagewx == None:
#            self.imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))
#        else:
#            self.imagewx.SetBitmap(image)
#
#        diff_time = time.time() - start_time
#
#        print '%0.3fs' %(diff_time)




    def OnLoadStat(self, event):

        start_time = time.time()

        #t = tempfile.NamedTemporaryFile(mode='r')


        def writePipeThread():
            def writeGPlotData():
                data = '# t random\n'
                for i in range(len(self.strip_random.time)):
                    time_now = time.time()
                    data += '%0.0f %0.3f\n' %(self.strip_random.time[i]-time_now,self.strip_random.data[i])
                print data
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


        start_new_thread( writePipeThread,() )


        #png = None
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


    def __del__(self):
        os.system('rm %s' %self.chart_data_pipe)
        os.system('rm %s' %self.chart_image_pipe)
        os.system('rm %s' %self.chart_gp_pipe)

