
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


from epics import PV
from epics_device import *




class Magnet:

    def __init__(self, ps=None, pv_volt=None, pv_curr=None, pv_temp=None):

        self.ps = ps
        self.pv_temp = pv_temp
        self.pv_volt = pv_volt
        self.pv_curr = pv_curr

