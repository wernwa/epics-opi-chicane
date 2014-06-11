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

class TabLog(wx.Panel):

    st_quad1 = None
    b_show = None
    imagewx = None


    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        self.b_show = wx.Button(parent=panel, pos=wx.Point(50, 490), label="LoadStat")
        self.b_show.Bind(wx.EVT_BUTTON, self.OnLoadStat2)
        panel.SetSizer(hbox)


    def OnLoadStat2(self, event):

        start_time = time.time()

        data = '# t random\n'
        for i in range(1,100):
            data += '%i %0.3f\n' %(i,random())
            with io.open('random.dat', 'w') as f:
                f.write(unicode(data))
                f.close()
        os.system('gnuplot random.gp')


        image = wx.Image('random.png').ConvertToBitmap()

        if self.imagewx == None:
            self.imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))
        else:
            self.imagewx.SetBitmap(image)

        diff_time = time.time() - start_time

        print '%0.3fs' %(diff_time)




    def OnLoadStat(self, event):

        start_time = time.time()

        t = tempfile.NamedTemporaryFile(mode='r')

        pipe_file_name = 'pipe-image'

        def writePipeThread():
            def writeGPlotData():
                data = '# t random\n'
                for i in range(1,100):
                    data += '%i %0.3f\n' %(i,random())
                with io.open('pipe-data', 'w') as f:
                    f.write(unicode(data))
                    f.close()
            start_new_thread( writeGPlotData ,() )
            os.system('gnuplot pipe-image.gp')
        start_new_thread( writePipeThread,() )


        png = None
        with io.open(pipe_file_name, 'rb') as pipe_file:
            buff = pipe_file.read()
            stream = io.BytesIO(buff)
            image = wx.ImageFromStream(stream).ConvertToBitmap()
            pipe_file.close()

        if self.imagewx == None:
            self.imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))
        else:
            self.imagewx.SetBitmap(image)

        diff_time = time.time() - start_time

        print '%0.3fs' %(diff_time)


