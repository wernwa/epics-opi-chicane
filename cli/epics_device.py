
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   <<project>>
#
#-------------------------------------------------------------------------------
from epics import PV




class PowerSupply:
    getterVolt = None
    setterVolt = None
    getterAmp = None
    setterAmp = None

    def __init__(self, getterVoltName, setterVoltName,
                        getterAmpName, setterAmpName):

        self.getterVolt = PV(getterVoltName)
        self.setterVolt = PV(setterVoltName)
        self.getterAmp = PV(getterAmpName)
        self.setterAmp = PV(setterAmpName)


