
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

