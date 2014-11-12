
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


from epics import PV
from epics_device import *
from init_vars import *
from PV_CONN import PV_CONN

import re
import numpy

from scipy.interpolate import interp1d


class Magnet:

    data_xlabel=None
    data_ylabel=None


    def __init__(self, ps=None, pv_volt=None, pv_curr=None, pv_temp=None, magn_type='quad'):

        self.ps = ps
        self.pv_temp = pv_temp
        self.pv_volt = pv_volt
        self.pv_curr = pv_curr
        self.magn_type = magn_type
        self.pv_volt_status = PV_CONN(ps.Volt.pvname+':status', auto_monitor=True)
        self.pv_curr_status = PV_CONN(ps.Curr.pvname+':status', auto_monitor=True)

        self.data_xlabel = 'I [A]'

        if magn_type=='quad':
            self.data_ylabel = 'k 1/[m]'
        elif magn_type=='dipol':
            self.data_ylabel = 'angle [mrad]'
        else:
            self.data_ylabel = 'y [??]'

        # Data for StripChart
        self.strip_chart_temp = []
        self.strip_chart_temp_time = []
        self.strip_chart_volt = []
        self.strip_chart_volt_time = []
        self.strip_chart_curr = []
        self.strip_chart_curr_time = []


    def load_data(self,file_name):

        x = self.data_x = [0]
        y = self.data_y = [0]

        # read the data from file
        for line in file(file_name, 'r').xreadlines():
            # split line into an array
            arr = re.findall('\S+',line)
            if len(arr)==0: continue
            # omit comments
            if (len(re.findall('^\s*?#',line))!=0):
                #if self.data_xlabel==None:
                #    self.data_xlabel = arr[0]
                #    self.data_ylabel = arr[1]
                continue
            # fill the x,y arrays
            x.append(float(arr[0]))
            if self.magn_type=='quad':
                # do the umrechnung
                y.append(float(arr[1])*c/E)
            else:
                y.append(float(arr[1]))

        # init splines
        self.k_spline = interp1d(x,y, kind='cubic')
        self.I_spline = interp1d(y,x, kind='cubic')

    def get_k(self,curr):
        k = round(self.k_spline(abs(curr)),3)
        return k

    def get_curr(self,k):
        #print 'k=%f curr exact %f'%(k,self.I_spline(abs(k)))
        curr = round(self.I_spline(abs(k)),3)
        return curr

