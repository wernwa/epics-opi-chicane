
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


from epics import PV
from epics_device import *

import re



class Magnet:

    data_xlabel=None
    data_ylabel=None

    def __init__(self, ps=None, pv_volt=None, pv_curr=None, pv_temp=None):

        self.ps = ps
        self.pv_temp = pv_temp
        self.pv_volt = pv_volt
        self.pv_curr = pv_curr



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
                if self.data_xlabel==None:
                    self.data_xlabel = arr[0]
                    self.data_ylabel = arr[1]
                continue
            # fill the x,y arrays
            x.append(float(arr[0]))
            y.append(float(arr[1]))



