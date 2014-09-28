
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------
from epics import PV
from PV_CONN import PV_CONN




class PowerSupply:

    def __init__(self, VoltName, CurrName):

        self.Volt = PV_CONN(VoltName, auto_monitor=True)
        self.Curr = PV_CONN(CurrName, auto_monitor=True)

    def getVolt(self):
        return self.Volt.get()

    def getCurr(self):
        return self.Curr.get()


    def setVolt(self, volt):
        self.Volt.put(volt)


    def setCurr(self, ampare):
        self.Curr.put(ampare)

