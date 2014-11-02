"""
This demo demonstrates how to draw a dynamic mpl (matplotlib)
plot in a wxPython application.

It allows "live" plotting as well as manual zooming to specific
regions.

Both X and Y axes allow "auto" or "manual" settings. For Y, auto
mode sets the scaling of the graph to see all the data points.
For X, auto mode makes the graph "follow" the data. Set it X min
to manual 0 to always see the whole data from the beginning.

Note: press Enter in the 'manual' text box to make a new value
affect the plot.

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 31.07.2008
"""
import os
import pprint
import random
import sys
import wx
import time
import thread


# The recommended way to use wx with mpl is with the WXAgg
# backend.
#
import matplotlib
#matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy
import pylab

# Epics imports
from epics import PV
from Experiment import *

class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init

    def next(self):
        self._recalc_data()
        return self.data

    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8:
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta



class BoundControlBox(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a
        manual mode with an associated value.
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.radio_auto = wx.RadioButton(self, -1,
            label="Auto", style=wx.RB_GROUP)
        self.radio_manual = wx.RadioButton(self, -1,
            label="Manual")
        self.manual_text = wx.TextCtrl(self, -1,
            size=(70,-1),
            value=str(initval),
            style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)

        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())

    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()

    def is_auto(self):
        return self.radio_auto.GetValue()

    def manual_value(self):
        return self.value


class TabStripChartCurr(wx.Panel):
    """ The main frame of the application
    """
    title = 'Demo: dynamic matplotlib graph'
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        #self.datagen = DataGen()
        #self.data = [self.datagen.next()]
        ## init two test PV variables ##
        #self.strip_chart02 = StripChartMemory(q1_temp)
        #self.strip_chart02 = StripChartMemory(t1)
        self.paused = True

        #self.create_menu()
        #self.create_status_bar()
        self.create_main_panel()


        self.update_axes=False
        self.alive=True
        self.axes_lock = thread.allocate_lock()


        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(500)

        thread.start_new_thread(self.on_update_axes,())

    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        #self = wx.Panel(self)

        self.init_plot()
        self.canvas = FigCanvas(self, -1, self.fig)

        self.xmin_control = BoundControlBox(self, -1, "X min", 0)
        self.xmax_control = BoundControlBox(self, -1, "X max", 50)
        self.ymin_control = BoundControlBox(self, -1, "Y min", 0)
        self.ymax_control = BoundControlBox(self, -1, "Y max", 100)

        self.pause_button = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)

        self.cb_grid = wx.CheckBox(self, -1,
            "Show Grid",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(True)

        self.cb_xlab = wx.CheckBox(self, -1,
            "Show X labels",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)
        self.cb_xlab.SetValue(True)

        self.pvListNames =[q1_curr.pvname,
                      q2_curr.pvname,
                      q3_curr.pvname,
                      q4_curr.pvname,
                      q5_curr.pvname,
                      q6_curr.pvname,
                      q7_curr.pvname,
                      d1_curr.pvname,
                      d2_curr.pvname,
                    ]
        self.ListNames_to_magn = {
            q1_curr.pvname : mquad1,
            q2_curr.pvname : mquad2,
            q3_curr.pvname : mquad3,
            q4_curr.pvname : mquad4,
            q5_curr.pvname : mquad5,
            q6_curr.pvname : mquad6,
            q7_curr.pvname : mquad7,
            d1_curr.pvname : mdipol1,
            d2_curr.pvname : mdipol2,
        }
        self.ListNames_to_color = {
            q1_curr.pvname : (1,0,0),
            q2_curr.pvname : (1,0.5,0),
            q3_curr.pvname : (1,0,0.5),
            q4_curr.pvname : (0,1,0),
            q5_curr.pvname : (0.5,1,0),
            q6_curr.pvname : (0,1,0.5),
            q7_curr.pvname : (0,0,1),
            d1_curr.pvname : (0.5,0,1),
            d2_curr.pvname : (0,0.5,1),
        }
        self.lb = wx.CheckListBox(self, -1, wx.DefaultPosition, (150,600), self.pvListNames)

        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtCheckListBox, self.lb)


        self.hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox0.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.hbox0.Add(self.lb ,0, flag=wx.RIGHT | wx.TOP)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_grid, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_xlab, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.xmin_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.xmax_control, border=5, flag=wx.ALL)
        self.hbox2.AddSpacer(24)
        self.hbox2.Add(self.ymin_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.ymax_control, border=5, flag=wx.ALL)


        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.hbox0, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.xmin = 0
        self.max_datapoints_plot = 1024
        #self.max_datapoints_plot = 200

    def EvtCheckListBox(self, evt):
        #print "The current selections are: "+str(self.lb.GetChecked())
        #for i in self.lb.GetChecked():
        #    print self.pvListNames[i]
        evt.Skip()

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Current', size=12)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference
        # to the plotted line series
        #
        #self.plot_data = self.axes.plot(
        #    self.strip_chart02.data,
        #    linewidth=1,
        #    color=(1, 1, 0),
        #    )[0]


    def draw_plot(self):
        """ Redraws the plot
        """
        # when xmin is on auto, it "follows" xmax to produce a
        # sliding window effect. therefore, xmin is assigned after
        # xmax.
        #
        if self.xmax_control.is_auto():
            #xmax = len(mquad1.strip_chart_temp) if len(mquad1.strip_chart_temp) > 50 else 50
            xmax = mquad1.strip_chart_curr_time[-1] if mquad1.strip_chart_curr_time[-1] > 50 else 50
        else:
            xmax = int(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin = xmax - 50
        else:
            xmin = int(self.xmin_control.manual_value())
        self.xmin = xmin
        self.xmax = xmax

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        #
        # note that it's easy to change this scheme to the
        # minimal/maximal value in the current display, and not
        # the whole data set.
        #
        if self.ymin_control.is_auto():
            #ymin = round(min(mquad1.strip_chart_temp), 0) - 1
            ymin = mquad1.strip_chart_curr[-1] - 50
        else:
            ymin = int(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            #ymax = round(max(mquad1.strip_chart_temp), 0) + 1
            ymax = mquad1.strip_chart_curr[-1]
        else:
            ymax = int(self.ymax_control.manual_value())
            self.axes.set_ybound(lower=ymin, upper=ymax)

        self.axes.set_xbound(lower=xmin, upper=xmax)

        # anecdote: axes.grid assumes b=True if any other flag is
        # given even if b is set to False.
        # so just passing the flag into the first statement won't
        # work.
        #
        if self.cb_grid.IsChecked():
            self.axes.grid(True, color='gray')
        else:
            self.axes.grid(False)

        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly
        # iterate, and setp already handles this.
        #
        pylab.setp(self.axes.get_xticklabels(),
            visible=self.cb_xlab.IsChecked())

        # assighn to epics records
        #self.plot_data.set_xdata(np.arange(len(self.data)))
        #self.plot_data.set_ydata(np.array(self.data))
        #self.plot_data.set_xdata(np.arange(len(self.strip_chart02.time)))
        #self.plot_data.set_ydata(np.array(self.strip_chart02.data))

        self.update_axes=True
        self.axes_lock.acquire()
        self.canvas.draw()
        self.axes_lock.release()

    def on_update_axes(self):
        while self.alive:
            while self.update_axes:
                self.axes_lock.acquire()
                self.axes.cla()
                self.axes.set_xlabel('time in seconds', fontsize = 9)
                self.axes.set_ylabel('Current in Ampere', fontsize = 9)

                for pv_i in self.lb.GetChecked():
                    list_name =  self.pvListNames[pv_i]
                    magn = self.ListNames_to_magn[list_name]
                    color = self.ListNames_to_color[list_name]

                    # find the x boundaries
                    xmin_i = 0
                    for i in xrange(0,len(magn.strip_chart_curr_time)):
                        if self.xmin<=magn.strip_chart_curr_time[i]:
                            xmin_i = i
                            break
                    xmax_i = len(magn.strip_chart_curr_time)-1
                    for i in xrange(len(magn.strip_chart_curr_time)-1,0,-1):
                        if self.xmax==magn.strip_chart_curr_time[i]:
                            xmax_i = i
                            break


                    if xmax_i-xmin_i < self.max_datapoints_plot:
                        part_arr_x = magn.strip_chart_curr_time[xmin_i:xmax_i]
                        part_arr_y = magn.strip_chart_curr[xmin_i:xmax_i]
                    else:
                        l = float(xmax_i-xmin_i)
                        x_arr=[]
                        y_arr=[]
                        step = int(round(l/float(self.max_datapoints_plot)))
                        #print 'reduzed axes',xmin_i,xmax_i,step
                        for i in range(xmin_i,xmax_i+1,step):
                            #ii = int(round(i*step))
                            x_arr.append(magn.strip_chart_curr_time[i])
                            y_arr.append(magn.strip_chart_curr[i])
                        if l%step!=0:
                            x_arr.append(magn.strip_chart_curr_time[-1])
                            y_arr.append(magn.strip_chart_curr[-1])
                        part_arr_x = x_arr
                        part_arr_y = y_arr


                    arr_x = numpy.array(part_arr_x)
                    arr_y = numpy.array(part_arr_y)

                    self.axes.plot(arr_x, arr_y, linewidth=1, color=color)



                self.update_axes=False
                self.axes_lock.release()
            time.sleep(.1)


    def on_pause_button(self, event):
        self.paused = not self.paused

    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)

    def on_cb_grid(self, event):
        self.draw_plot()

    def on_cb_xlab(self, event):
        self.draw_plot()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        #
        tab_i = self.parent.GetSelection()
        if not self.paused and self.parent.GetPageText(tab_i)=='Current':
            self.draw_plot()

    def on_exit(self, event):
        self.Destroy()

    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER,
            self.on_flash_status_off,
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)

    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')

    def __del__(self):
        self.paused=True
        self.alive=False
