
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


from epics import PV
from epics_device import *

import re



class Magnet:

    def __init__(self, ps=None, pv_volt=None, pv_curr=None, pv_temp=None):

        self.ps = ps
        self.pv_temp = pv_temp
        self.pv_volt = pv_volt
        self.pv_curr = pv_curr

        self.load_data('data/strength-int.data')


    def load_data(self,file_name):

        x = self.data_x = [0]
        y = self.data_y = [0]

        # read the data from file
        for line in file(file_name, 'r').xreadlines():
            # omit comments
            if (len(re.findall('^\s*?#',line))!=0): continue
            # split line into an array
            arr = re.findall('\S+',line)
            # fill the x,y arrays
            x.append(float(arr[0]))
            y.append(float(arr[1]))



