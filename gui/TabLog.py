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

class TabLog(wx.Panel):

    st_quad1 = None
    b_show = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        panel = self

        hbox = wx.BoxSizer(wx.HORIZONTAL)


        self.b_show = wx.Button(parent=panel, pos=wx.Point(50, 490), label="Load")
        self.b_show.Bind(wx.EVT_BUTTON, self.OnDemag)
        panel.SetSizer(hbox)


    def OnDemag(self, event):
       # def demagThread():
       #     self.b_show.Enable(False)

       #     imageFile = 'pipe-image'
       #     png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
       #     imagewx = wx.StaticBitmap(self, -1, png, (5, 5), (png.GetWidth(), png.GetHeight()))

       #     self.b_show.Enable(True)

       # start_new_thread( demagThread,() )
        t = tempfile.NamedTemporaryFile(mode='r')


        imageFile = 'pics/crop_Zplus_Cat-III_L2.jpg'
        pipe_file_name = 'pipe-image'

        def writePipeThread():
            #buff = None
            #with io.open(imageFile, 'rb') as file:
            #    buff = file.read()
            #    file.close()
            def writeGPlotData():
                data = '# t random\n'
                for i in range(1,10):
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

        #png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imagewx = wx.StaticBitmap(self, -1, image, (5, 5), (image.GetWidth(), image.GetHeight()))


