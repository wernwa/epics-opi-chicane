
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

        self.getterVolt = PV(getterVoltName, auto_monitor=True )
        self.setterVolt = PV(setterVoltName, auto_monitor=True)
        self.getterAmp = PV(getterAmpName, auto_monitor=True)
        self.setterAmp = PV(setterAmpName, auto_monitor=True)

    def getVolt(self):
        return self.getterVolt.get()

    def getAmpere(self):
        return self.getterAmp.get()


    def putVolt(self, volt):
        self.setterVolt.put(volt)
        self.getterVolt.put(volt)


    def putAmpere(self, ampare):
        self.setterAmp.put(ampare)
        self.getterAmp.put(ampare)

