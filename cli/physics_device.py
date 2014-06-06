
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------


from epics import PV
from epics_device import *




class Magnet:
    powersupply = None
    themp = None
    posX = None

    def __init__(self, powersupply):

        self.powersupply = powersupply

